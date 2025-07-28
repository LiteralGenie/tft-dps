import { API_URL } from '$lib/constants'
import type { GameInfoContext, GameInfoValue } from '$lib/gameInfoContext.svelte'
import { packAllUnitIds, packSimId } from '$lib/utils/networkUtils'
import { alphabetical, range } from 'radash'
import { getContext, setContext } from 'svelte'
import type { SearchContextValue } from '../searchContext.svelte'
import {
    assert,
    compressGzip,
    enumerate,
    getSortedInsertionIndex,
    iterBatches,
    iterCombinations,
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
    set: (params: SearchContextValue) => void
}

export interface ActiveSearchContextValue {
    id: string
    params: SearchContextValue
    data: {
        values: Map<PackedId, ActiveSearchData> // id -> avg dps
        sortedValues: Record<string, Array<{ id: PackedId; sortValue: number }>>
        sortedFilteredIds: Array<PackedId>
    }
    done: boolean
}
const CONTEXT_KEY = 'active_search'

export function setActiveSearchContext(infoCtx: GameInfoContext): ActiveSearchContext {
    const ctx = $state<ActiveSearchContext>({
        value: null,
        columns: ACTIVE_SEARCH_COLUMNS,
        sortColumn: null,
        defaultSortColumn: 'dps',
        columnFilters: {},
        set,
    })
    setContext(CONTEXT_KEY, ctx)

    resetColumnFilters()

    return ctx

    function set(params: SearchContextValue) {
        ctx.value = {
            id: String(Date.now()),
            params,
            data: { values: new Map(), sortedValues: {}, sortedFilteredIds: [] },
            done: false,
        }

        for (const col of ctx.columns) {
            if (col.getSortValue) {
                ctx.value.data.sortedValues[col.id] = []
            }
        }

        resetColumnFilters()
        fetchData(ctx.value)
    }

    async function fetchData(ctxVal: ActiveSearchContextValue) {
        const comboIter = new ComboIter(ctxVal.params, 1000, infoCtx.value)
        const batchSize = 1000

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

            const isCancelled = ctx?.value?.id !== ctxVal.id
            if (isCancelled) return
        }
    }

    function resetColumnFilters() {
        for (const col of ctx.columns) {
            if (col.filter) {
                ctx.columnFilters[col.id] = ''
            }
        }
    }

    function insertData(ctxVal: ActiveSearchContextValue, data: ActiveSearchData) {
        ctxVal.data.values.set(data.id, data)

        for (const col of ctx.columns) {
            if (!col.getSortValue) {
                continue
            }

            const v = col.getSortValue(data, infoCtx.value)
            const vs = ctxVal.data.sortedValues[col.id]
            const idx = getSortedInsertionIndex(vs, v, (x) => x.sortValue)
            vs.splice(idx, 0, { id: data.id, sortValue: v })
            ctxVal.data.sortedValues[col.id] = ctxVal.data.sortedValues[col.id]
        }
    }

    function applyFilters(ctxVal: ActiveSearchContextValue) {
        const sortedValues = ctxVal.data.sortedValues[ctx.sortColumn ?? ctx.defaultSortColumn]

        const toRemove = new Set()
        for (const [colId, text] of Object.entries(ctx.columnFilters)) {
            if (!text.length) continue

            const colFilter = ctx.columns.find((c) => c.id === colId)!.filter!
            const clauses = colFilter.prepare(text)
            if (!clauses.length) continue

            for (const [idx, sv] of enumerate(sortedValues)) {
                if (toRemove.has(idx)) continue

                const d = ctxVal.data.values.get(sv.id)!

                const matchesAnyClause = clauses.some((cl) =>
                    colFilter.isMatch(d, infoCtx.value, cl),
                )
                if (!matchesAnyClause) {
                    toRemove.add(idx)
                }
            }
        }

        ctxVal.data.sortedFilteredIds = sortedValues
            .filter((_, idx) => !toRemove.has(idx))
            .map((sv) => sv.id)
    }
}

export function getActiveSearchContext(): ActiveSearchContext {
    return getContext(CONTEXT_KEY)
}

class ComboIter {
    constructor(
        public params: SearchContextValue,
        public batchSize: number,
        public info: GameInfoValue,
    ) {
        assert(params.units.size > 0)
        assert(params.minStars < params.maxStars)
    }

    *[Symbol.iterator]() {
        const units = alphabetical([...this.params.units], (x) => x)
        const stars = [...range(this.params.minStars, this.params.maxStars)]
        const items = alphabetical(['__BLANK__', ...this.params.items], (x) => x)

        for (const unitId of units) {
            const traitBps = this.info.units[unitId].info.traits.map((traitId) => {
                const trait = this.info.traits[traitId]
                const bps = trait.tiers
                    .filter((tier) => tier.rarity === 'unique' || this.params.traits[tier.rarity])
                    .map((tier) => tier.breakpoint)
                return [0, ...bps].map((bp) => [traitId, bp] as [string, number])
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

                            for (const bps of iterCombinations(traitBps)) {
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
}
