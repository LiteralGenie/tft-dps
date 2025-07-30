import { isEqual } from 'radash'
import { getContext, setContext } from 'svelte'
import { areSetsEqual } from '../utils/miscUtils'
import { DEFAULT_SEARCH_CONTEXT } from './searchContextConstants'

export type SearchContext = {
    value: SearchContextValue
    lastValue: SearchContextValue
    reset: () => void
    hasChanges: () => boolean
}

export type SearchContextValue = {
    units: Set<string>
    stars: {
        1: boolean
        2: boolean
        3: boolean
    }

    items: Set<string>
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

export function setSearchContext(): SearchContext {
    const ctx = $state<SearchContext>({
        value: DEFAULT_SEARCH_CONTEXT(),
        lastValue: DEFAULT_SEARCH_CONTEXT(),
        reset,
        hasChanges,
    })
    setContext(CONTEXT_KEY, ctx)
    return ctx

    function reset() {
        ctx.value = DEFAULT_SEARCH_CONTEXT()
    }

    function hasChanges(): boolean {
        const a = ctx.lastValue
        const b = ctx.value

        return checkUnits() || checkStars() || checkItems() || checkTraits()

        function checkUnits() {
            return areSetsEqual(a.units, b.units)
        }

        function checkStars() {
            return !isEqual($state.snapshot(a.stars), $state.snapshot(b.stars))
        }

        function checkItems() {
            return areSetsEqual(a.items, b.items)
        }

        function checkTraits() {
            return !isEqual($state.snapshot(a.traits), $state.snapshot(b.traits))
        }
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
