import { API_URL } from '$lib/constants'
import type { GameInfoContext } from '$lib/gameInfoContext.svelte'
import { packAllUnitIds, packUnitId } from '$lib/utils/networkUtils'
import { alphabetical, range } from 'radash'
import { getContext, setContext } from 'svelte'
import type { SearchContextValue } from '../searchContext.svelte'
import { assert, compressGzip, iterBatches, iterCombinations } from '../utils/miscUtils'
import {
    ACTIVE_SEARCH_COLUMNS,
    type ActiveSearchColumn,
    type ActiveSearchData,
    type PackedId,
} from './activeSearchConstants'

export interface ActiveSearchContext {
    value: null | {
        id: string
        params: SearchContextValue
        data: {
            values: Record<PackedId, number> // id -> avg dps
            sortedValues: Record<string, Array<{ id: PackedId; sortValue: number }>>
            sortedFilteredValues: Array<ActiveSearchData>
        }
        done: boolean
    }
    columns: Array<ActiveSearchColumn>
    sortColumn: null | string
    columnFilters: Record<string, string>
    set: (params: SearchContextValue) => void
}

const CONTEXT_KEY = 'active_search'

export function setActiveSearchContext(info: GameInfoContext): ActiveSearchContext {
    const ctx = $state<ActiveSearchContext>({
        value: null,
        columns: ACTIVE_SEARCH_COLUMNS,
        sortColumn: null,
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
            data: { values: {}, sortedValues: {}, sortedFilteredValues: [] },
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

    async function fetchData(value: ActiveSearchContext['value'] & { id: string }) {
        const comboIter = new ComboIter(value.params, 1000, info)
        const batchSize = 10 // 1000

        for (const batch of iterBatches(comboIter, batchSize)) {
            const packed = batch.map((x) => packUnitId(info, x.unitId, x.stars, x.items, x.traits))
            const allPacked = packAllUnitIds(packed)
            const asGzip = await compressGzip(allPacked)
            const resp = await fetch(API_URL + '/simulate', {
                method: 'POST',
                body: asGzip,
                headers: {
                    'content-type': 'application/octet-stream',
                },
            })
            const data = await resp.json()

            const isCancelled = ctx?.value?.id !== value.id
            if (isCancelled) return

            console.log(data)
        }
    }

    function resetColumnFilters() {
        for (const col of ctx.columns) {
            if (col.filter) {
                ctx.columnFilters[col.id] = ''
            }
        }
    }
}

export function getActiveSearchContext(): ActiveSearchContext {
    return getContext(CONTEXT_KEY)
}

class ComboIter {
    constructor(
        public params: SearchContextValue,
        public batchSize: number,
        public infoCtx: GameInfoContext,
    ) {
        assert(params.units.size > 0)
        assert(params.minStars < params.maxStars)
    }

    *[Symbol.iterator]() {
        const units = alphabetical([...this.params.units], (x) => x)
        const stars = range(this.params.minStars, this.params.maxStars)
        const items = alphabetical(['__BLANK__', ...this.params.items], (x) => x)

        for (const unitId of units) {
            const traitBps = this.infoCtx.units[unitId].info.traits.map((traitId) => {
                const trait = this.infoCtx.traits[traitId]
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
