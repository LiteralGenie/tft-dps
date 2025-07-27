import { getContext, setContext } from 'svelte'

export interface GameInfoContext {
    units: Record<
        string,
        {
            index: number
            info: {
                id: string
                name: string
                traits: string[]
                cost: number
                icon: string
            }
        }
    >
    items: Record<
        string,
        {
            id: string
            name: string
            desc: string
            type: string
            icon: string
            index: number
        }
    >
    traits: Record<
        string,
        {
            id: string
            name: string
            desc: string
            icon: string
            tiers: number[]
            effects_bonus: Record<string, any>
        }
    >
}

const CONTEXT_KEY = 'game_info_context'

export function setGameInfoContext(): GameInfoContext {
    const ctx = $state<GameInfoContext>({ units: {}, items: {}, traits: {} })
    setContext(CONTEXT_KEY, ctx)
    return ctx
}

export function getGameInfoContext(): GameInfoContext {
    return getContext(CONTEXT_KEY)
}
