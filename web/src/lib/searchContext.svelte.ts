import { getContext, setContext } from 'svelte'
import { DEFAULT_SEARCH_CONTEXT } from './constants'

export type SearchContext = {
    units: Set<string>
    minStars: number
    maxStars: number

    items: Set<string>
    traits: {
        silver: boolean
        gold: boolean
        prismatic: boolean
    }
}

const CONTEXT_KEY = 'search_context'

export function setSearchContext(): SearchContext {
    const ctx = $state<SearchContext>(DEFAULT_SEARCH_CONTEXT())
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
