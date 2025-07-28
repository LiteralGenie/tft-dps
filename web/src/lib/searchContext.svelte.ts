import { getContext, setContext } from 'svelte'
import { DEFAULT_SEARCH_CONTEXT } from './constants'

export type SearchContext = {
    value: SearchContextValue
    reset: () => void
}

export type SearchContextValue = {
    units: Set<string>
    minStars: number
    maxStars: number

    items: Set<string>
    traits: {
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
        reset,
    })
    setContext(CONTEXT_KEY, ctx)
    return ctx

    function reset() {
        ctx.value = DEFAULT_SEARCH_CONTEXT()
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
