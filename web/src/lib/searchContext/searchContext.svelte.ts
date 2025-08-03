import type { GameInfoContext } from '$lib/gameInfoContext.svelte'
import { isEqual } from 'radash'
import { getContext, setContext } from 'svelte'
import { SvelteSet } from 'svelte/reactivity'
import { hasSetDiff } from '../utils/miscUtils'
import { DEFAULT_SEARCH_CONTEXT, EMPTY_SEARCH_CONTEXT } from './searchContextConstants'

export type SearchContext = {
    value: SearchContextValue
    lastValue: null | SearchContextValue
    reset: () => void
    hasChanges: () => boolean
    toUrl: (v: SearchContextValue) => URLSearchParams
    fromUrl: (p: URLSearchParams) => Partial<SearchContextValue>
}

export type SearchContextValue = {
    period: number

    units: SvelteSet<string>
    stars: {
        1: boolean
        2: boolean
        3: boolean
    }

    items: SvelteSet<string>
    onlyItemRecs: boolean

    traits: {
        inactive: boolean
        bronze: boolean
        silver: boolean
        gold: boolean
        prismatic: boolean
    }
}

const CONTEXT_KEY = 'search_context'

export function setSearchContext(info: GameInfoContext): SearchContext {
    const ctx = $state<SearchContext>({
        value: DEFAULT_SEARCH_CONTEXT(),
        lastValue: null,
        reset,
        hasChanges,
        toUrl,
        fromUrl,
    })
    setContext(CONTEXT_KEY, ctx)
    return ctx

    function reset() {
        ctx.value = DEFAULT_SEARCH_CONTEXT()
    }

    function hasChanges(): boolean {
        if (ctx.lastValue === null) return true

        const a = ctx.lastValue
        const b = ctx.value

        return checkPeriod() || checkUnits() || checkStars() || checkItems() || checkTraits()

        function checkPeriod() {
            return a.period !== b.period
        }

        function checkUnits() {
            return hasSetDiff(a.units, b.units)
        }

        function checkStars() {
            return !isEqual($state.snapshot(a.stars), $state.snapshot(b.stars))
        }

        function checkItems() {
            if (b.onlyItemRecs) {
                return !a.onlyItemRecs
            } else {
                return hasSetDiff(a.items, b.items)
            }
        }

        function checkTraits() {
            return !isEqual($state.snapshot(a.traits), $state.snapshot(b.traits))
        }
    }

    function toUrl(ctxVal: SearchContextValue): URLSearchParams {
        const params = new URLSearchParams()

        params.set('t', String(ctxVal.period))

        const units = [...ctxVal.units]
            .map((unitId) => info.value.units[unitId])
            .map((unit) => unit.index)
        for (const idx of units) {
            params.append('units', String(idx))
        }

        if (ctxVal.onlyItemRecs) {
            params.set('item_recs', '1')
        } else {
            const items = [...ctxVal.items]
                .map((itemId) => info.value.items[itemId])
                .map((item) => item.index)
            for (const idx of items) {
                params.append('items', String(idx))
            }
        }

        for (const k of [1, 2, 3] as const) {
            if (ctxVal.stars[k]) {
                params.append('stars', String(k))
            }
        }

        for (const k of Object.keys(ctxVal.traits)) {
            if ((ctxVal.traits as any)[k]) {
                params.append('traits', String(k))
            }
        }

        return params
    }

    function fromUrl(params: URLSearchParams): Partial<SearchContextValue> {
        const val: Partial<SearchContextValue> = {}
        const empty = EMPTY_SEARCH_CONTEXT()

        const t = parseInt(params.get('t') ?? '')
        if (!isNaN(t)) val.period = t

        const units = params
            .getAll('units')
            .map((idxString) => parseInt(idxString))
            .map((idx) => info.value.unitsByIndex[idx])
            .filter((unitId) => !!unitId)
        if (units.length) val.units = new SvelteSet(units)

        if (params.get('item_recs')) {
            val.onlyItemRecs = true
        } else {
            const items = params
                .getAll('items')
                .map((idxString) => parseInt(idxString))
                .map((idx) => info.value.itemsByIndex[idx])
                .filter((itemId) => !!itemId)
            if (items.length) val.items = new SvelteSet(items)
        }

        const stars = params
            .getAll('stars')
            .map((x) => parseInt(x))
            .filter((x): x is keyof SearchContextValue['stars'] => [1, 2, 3].includes(x))
        if (stars.length) {
            val.stars = { 1: false, 2: false, 3: false }
            for (const s of stars) {
                val.stars[s] = true
            }
        }

        const traits = params
            .getAll('traits')
            .filter((x): x is keyof SearchContextValue['traits'] => x in empty.traits)
        if (traits.length) {
            val.traits = empty.traits
            for (const s of traits) {
                val.traits[s] = true
            }
        }

        return val
    }
}

export function getSearchContext(): SearchContext {
    return getContext(CONTEXT_KEY)
}

export interface SearchContextUnit {
    enabled: boolean
    id: string
    minStars: number
    maxStars: number
}

export interface SearchContextItem {
    type: 'multi' | 'exact'
    ids: string
}

export interface SearchContextTrait {
    id: string
    minValue: number
    maxValue: number
}
