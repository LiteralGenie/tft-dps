import { API_URL } from '$lib/constants'
import type { GameInfoContext, GameInfoValue } from '$lib/gameInfoContext.svelte'
import { packAllUnitIds, packSimId } from '$lib/utils/networkUtils'
import { alphabetical, range, sum } from 'radash'
import { getContext, setContext } from 'svelte'
import type { SearchContextValue } from '../searchContext.svelte'
import {
    assert,
    compressGzip,
    iterBatches,
    iterCombinations,
    nCr,
    OrderedValueMap,
    product,
} from '../utils/miscUtils'
import {
    ACTIVE_SEARCH_COLUMNS,
    type ActiveSearchColumn,
    type ActiveSearchData,
    type PackedId,
} from './activeSearchConstants'

export interface ActiveSearchContext {
    value: null | ActiveSearchContextValue
    columns: Array<ActiveSearchColumn>
    sortColumn: null | string
    defaultSortColumn: string
    columnFilters: Record<string, string>
    pageIdx: number
    pageSize: number
    set: (params: SearchContextValue) => void
    setFilter: (colId: string, filter: string) => void
}

export interface ActiveSearchContextValue {
    id: string
    params: SearchContextValue
    data: {
        values: Map<PackedId, ActiveSearchData> // id -> avg dps
        sortedValues: Record<string, OrderedValueMap>
        sortedFilteredIds: Array<PackedId>
    }
    progress: {
        count: number
        total: number
        start: number
        end: number | null
    }
}
const CONTEXT_KEY = 'active_search'

export function setActiveSearchContext(infoCtx: GameInfoContext): ActiveSearchContext {
    const ctx = $state<ActiveSearchContext>({
        value: null,
        columns: ACTIVE_SEARCH_COLUMNS,
        sortColumn: null,
        defaultSortColumn: 'dps',
        columnFilters: {},
        pageIdx: 0,
        pageSize: 20,
        set,
        setFilter,
    })
    setContext(CONTEXT_KEY, ctx)

    resetColumnFilters()

    return ctx

    function set(params: SearchContextValue) {
        ctx.value = {
            id: String(Date.now()),
            params,
            data: { values: new Map(), sortedValues: {}, sortedFilteredIds: [] },
            progress: {
                count: 0,
                total: 0,
                start: Date.now(),
                end: null,
            },
        }

        for (const col of ctx.columns) {
            if (col.sort) {
                ctx.value.data.sortedValues[col.id] = new OrderedValueMap({ order: col.sort.order })
            }
        }

        ctx.pageIdx = 0

        resetColumnFilters()
        fetchData(ctx.value)
    }

    async function fetchData(ctxVal: ActiveSearchContextValue) {
        const comboIter = new ComboIter(ctxVal.params, infoCtx.value)
        const batchSize = 100

        ctxVal.progress.total = comboIter.total

        for (const batch of iterBatches(comboIter, batchSize)) {
            const packed = batch.map((x) =>
                packSimId(infoCtx.value, x.unitId, x.stars, x.items, x.traits),
            )
            const allPacked = packAllUnitIds(packed)
            const asGzip = await compressGzip(allPacked)
            const resp = await fetch(API_URL + '/simulate', {
                method: 'POST',
                body: asGzip,
                headers: {
                    'content-type': 'application/octet-stream',
                },
            })
            const data: number[] = await resp.json()

            for (let idx = 0; idx < batch.length; idx++) {
                const packedId = packed[idx]
                insertData(ctxVal, {
                    id: packedId,
                    dps: data[idx],
                })
            }
            applyFilters(ctxVal)

            ctxVal.progress.count += batch.length

            const isCancelled = ctx.value?.id !== ctxVal.id
            if (isCancelled) {
                console.log('fetch cancelled')
                return
            }
        }

        ctxVal.progress.end = Date.now()
    }

    function resetColumnFilters() {
        for (const col of ctx.columns) {
            if (col.filter) {
                ctx.columnFilters[col.id] = ''
            }
        }

        if (ctx.value) {
            applyFilters(ctx.value)
        }
    }

    function insertData(ctxVal: ActiveSearchContextValue, data: ActiveSearchData) {
        ctxVal.data.values.set(data.id, data)

        for (const col of ctx.columns) {
            if (!col.sort) {
                continue
            }

            const v = col.sort.getValue(data, infoCtx.value)
            const vs = ctxVal.data.sortedValues[col.id]
            vs.set(data.id, v)
        }
    }

    function applyFilters(ctxVal: ActiveSearchContextValue) {
        const sortedValues = ctxVal.data.sortedValues[ctx.sortColumn ?? ctx.defaultSortColumn]
        const ids = sortedValues.keys()

        const toRemove = new Set()
        for (const [colId, text] of Object.entries(ctx.columnFilters)) {
            if (!text.length) continue

            const colFilter = ctx.columns.find((c) => c.id === colId)!.filter!
            const clauses = colFilter.prepare(text, infoCtx.value)
            if (!clauses.length) continue

            for (const id of ids) {
                if (toRemove.has(id)) continue

                const d = ctxVal.data.values.get(id)!

                const matchesAnyClause = clauses.some((cl) =>
                    colFilter.isMatch(d, infoCtx.value, cl),
                )
                if (!matchesAnyClause) {
                    toRemove.add(id)
                }
            }
        }

        const sortedFilteredIds = []
        for (const id of ids) {
            if (toRemove.has(id)) continue
            sortedFilteredIds.push(id)
        }

        ctxVal.data.sortedFilteredIds = sortedFilteredIds
    }

    function setFilter(colId: string, filter: string) {
        assert(colId in ctx.columnFilters)

        ctx.columnFilters[colId] = filter
        if (ctx.value) applyFilters(ctx.value)
    }
}

export function getActiveSearchContext(): ActiveSearchContext {
    return getContext(CONTEXT_KEY)
}

class ComboIter {
    total: number

    constructor(
        public params: SearchContextValue,
        public info: GameInfoValue,
    ) {
        assert(params.units.size > 0)
        assert(params.minStars <= params.maxStars)

        this.total = this.count()
    }

    *[Symbol.iterator]() {
        const units = alphabetical([...this.params.units], (x) => x)
        const stars = [...range(this.params.minStars, this.params.maxStars)]
        const items = alphabetical(['__BLANK__', ...this.params.items], (x) => x)

        for (const unitId of units) {
            const traitBps = this.info.units[unitId].info.traits.map((traitId) => {
                const trait = this.info.traits[traitId]
                const bps = new Set(
                    trait.tiers
                        .filter(
                            (tier) => tier.rarity === 'unique' || this.params.traits[tier.rarity],
                        )
                        .map((tier) => tier.breakpoint),
                )
                if (!trait.has_bp_1 && this.params.traits['inactive']) {
                    bps.add(1)
                }
                return [...bps].map((bp) => [traitId, bp] as [string, number])
            })

            for (const star of stars) {
                for (let idxItem1 = 0; idxItem1 < items.length; idxItem1++) {
                    const item1 = items[idxItem1]

                    for (let idxItem2 = idxItem1; idxItem2 < items.length; idxItem2++) {
                        const item2 = items[idxItem2]

                        for (let idxItem3 = idxItem2; idxItem3 < items.length; idxItem3++) {
                            const item3 = items[idxItem3]

                            const its: string[] = []
                            if (item1 !== '__BLANK__') its.push(item1)
                            if (item2 !== '__BLANK__') its.push(item2)
                            if (item3 !== '__BLANK__') its.push(item3)

                            for (const bps of iterCombinations(...traitBps)) {
                                yield {
                                    unitId,
                                    stars: star,
                                    items: its,
                                    traits: Object.fromEntries(bps as any),
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    private count(): number {
        const stars = [...range(this.params.minStars, this.params.maxStars)]

        const numItems = this.params.items.size
        const numItemCombos = 1 + numItems + nCr(numItems + 1, 2) + nCr(numItems + 2, 3)

        const numUnitTraitCombos = sum(
            [...this.params.units].flatMap((unitId) => {
                const unit = this.info.units[unitId]

                const tiersPerTrait = unit.info.traits
                    .map((traitId) => this.info.traits[traitId])
                    .map((trait) =>
                        trait.tiers.filter(
                            (tier) => tier.rarity === 'unique' || this.params.traits[tier.rarity],
                        ),
                    )
                    .map((validTiers) => {
                        const bps = new Set(validTiers.map((tier) => tier.breakpoint))
                        bps.add(1)
                        return bps.size
                    })

                return product(tiersPerTrait)
            }),
        )

        console.log(
            stars.length * numItemCombos * numUnitTraitCombos,
            stars.length,
            numItemCombos,
            numUnitTraitCombos,
        )
        return stars.length * numItemCombos * numUnitTraitCombos
    }
}
