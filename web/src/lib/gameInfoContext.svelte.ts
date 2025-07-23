import { getContext, setContext } from 'svelte'

export interface GameInfoContext {
    units: Record<
        string,
        {
            info: {
                id: string
                name: string
                traits: string[]
                cost: number
            }
        }
    >
}

const CONTEXT_KEY = 'game_info_context'

export function setGameInfoContext(): GameInfoContext {
    const ctx = $state<GameInfoContext>({ units: {} })
    setContext(CONTEXT_KEY, ctx)
    return ctx
}

export function getGameInfoContext(): GameInfoContext {
    return getContext(CONTEXT_KEY)
}
