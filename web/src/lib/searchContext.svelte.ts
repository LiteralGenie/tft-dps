import { getContext, setContext } from 'svelte'
import type { GameInfoContext } from './gameInfoContext.svelte'

export type SearchContext = {
    value: SearchContextEntry[]
    getDefaultEntry: (infoCtx: GameInfoContext) => SearchContextEntry
}

export interface SearchContextEntry {
    enabled: boolean
    name: string
    units: Record<string, SearchContextUnit>
    items: SearchContextItem[]
    traits: SearchContextTrait[]
}

const CONTEXT_KEY = 'search_context'

export function setSearchContext(): SearchContext {
    const value = $state<SearchContextEntry[]>([])

    const ctx = {
        value,
        getDefaultEntry,
    }

    setContext(CONTEXT_KEY, ctx)
    return ctx

    function getDefaultEntry(infoCtx: GameInfoContext): SearchContextEntry {
        const units: SearchContextEntry['units'] = Object.fromEntries(
            Object.entries(infoCtx.units).map(([unitId, unit]) => {
                return [
                    unitId,
                    {
                        enabled: false,
                        id: unitId,
                        minStars: 3,
                        maxStars: 3,
                    },
                ]
            }),
        )

        return {
            enabled: true,
            name: '',
            units,
            items: [],
            traits: [],
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
