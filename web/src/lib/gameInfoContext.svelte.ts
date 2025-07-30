import { getContext, setContext } from 'svelte'

export interface GameInfoContext {
    value: GameInfoValue
    set: (
        units: GameInfoValue['units'],
        items: GameInfoValue['items'],
        traits: GameInfoValue['traits'],
    ) => void
}

export interface GameInfoValue {
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
                role_items: string[]
            }
        }
    >
    unitsByIndex: Record<number, string>

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
    itemsByIndex: Record<number, string>

    traits: Record<
        string,
        {
            id: string
            name: string
            desc: string
            icon: string
            breakpoints: number[]
            styles: number[]
            effects_bonus: Record<string, any>
            tiers: Array<{
                breakpoint: number
                rarity: 'unique' | 'bronze' | 'silver' | 'gold' | 'prismatic'
            }>
            num_bits: number
            has_bp_1: boolean
        }
    >
}

const CONTEXT_KEY = 'game_info_context'

export function setGameInfoContext(): GameInfoContext {
    const value = {
        units: {},
        unitsByIndex: {},
        items: {},
        itemsByIndex: {},
        traits: {},
    }
    const ctx = $state<GameInfoContext>({
        value,
        set,
    })
    setContext(CONTEXT_KEY, ctx)
    return ctx

    function set(
        units: GameInfoValue['units'],
        items: GameInfoValue['items'],
        traits: GameInfoValue['traits'],
    ) {
        const unitsByIndex: GameInfoValue['unitsByIndex'] = {}
        for (const unit of Object.values(units)) {
            unitsByIndex[unit.index] = unit.info.id
        }

        const itemsByIndex: GameInfoValue['itemsByIndex'] = {}
        for (const item of Object.values(items)) {
            itemsByIndex[item.index] = item.id
        }

        for (const trait of Object.values(traits)) {
            let numBps = trait.breakpoints.length
            if (trait.breakpoints[0] <= 1) numBps += 1

            let bits
            if (numBps <= 2) {
                bits = 1
            } else if (numBps <= 4) {
                bits = 2
            } else if (numBps <= 8) {
                bits = 3
            } else if (numBps <= 16) {
                bits = 4
            } else {
                throw new Error()
            }

            ctx.value = {
                units,
                unitsByIndex,
                items,
                itemsByIndex,
                traits,
            }
        }
    }
}

export function getGameInfoContext(): GameInfoContext {
    return getContext(CONTEXT_KEY)
}
