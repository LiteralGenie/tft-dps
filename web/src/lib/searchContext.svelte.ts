import { getContext, setContext } from 'svelte'

export type SearchContext = {
    units: Set<string>
    minStars: number
    maxStars: number

    items: Set<string>
    traits: Set<string>
}

const CONTEXT_KEY = 'search_context'

export function setSearchContext(): SearchContext {
    const ctx = $state<SearchContext>({
        units: new Set(),
        minStars: 1,
        maxStars: 3,
        items: new Set(),
        traits: new Set(),
    })

    setContext(CONTEXT_KEY, ctx)
    return ctx
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
