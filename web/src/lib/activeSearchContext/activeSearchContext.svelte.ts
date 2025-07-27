import { alphabetical, range } from 'radash'
import { getContext, setContext } from 'svelte'
import type { SearchContext } from '../searchContext.svelte'
import { assert } from '../utils/miscUtils'
import {
    ACTIVE_SEARCH_COLUMNS,
    type ActiveSearchColumn,
    type ActiveSearchData,
    type PackedId,
} from './activeSearchConstants'

export interface ActiveSearchContext {
    value: null | {
        id: string
        params: SearchContext
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
    set: (params: SearchContext) => void
}

const CONTEXT_KEY = 'active_search'

export function setActiveSearchContext(): ActiveSearchContext {
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

    function set(params: SearchContext) {
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
    }

    function fetchData() {
        // const comboIter =
        // for (const combo of iterCombos()) {
        // }
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
        public params: SearchContext,
        batchSize: number,
    ) {
        assert(params.units.size > 0)
        assert(params.minStars < params.maxStars)
    }

    *[Symbol.iterator]() {
        const units = alphabetical([...this.params.units], (x) => x)
        const stars = range(this.params.minStars, this.params.maxStars)
        const items = alphabetical(['__BLANK__', ...this.params.items], (x) => x)

        // const traitGroups = []
        // const traitCombos = combos(traitGroups)

        for (const unit of units) {
            for (const star of stars) {
                // @todo: traits

                for (let idxItem1 = 0; idxItem1 < items.length; idxItem1++) {
                    const item1 = items[idxItem1]

                    for (let idxItem2 = idxItem1; idxItem2 < items.length; idxItem2++) {
                        const item2 = items[idxItem2]

                        for (let idxItem3 = idxItem2; idxItem3 < items.length; idxItem3++) {
                            const item3 = items[idxItem3]

                            if (item1 !== '__BLANK__') items.push(item1)
                            if (item2 !== '__BLANK__') items.push(item2)
                            if (item3 !== '__BLANK__') items.push(item3)

                            yield {
                                unit,
                                star,
                                items,
                            }
                        }
                    }
                }
            }
        }
    }
}
