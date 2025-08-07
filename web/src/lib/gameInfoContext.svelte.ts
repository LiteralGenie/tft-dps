import { alphabetical } from 'radash'
import { getContext, setContext } from 'svelte'
import { enumerate } from './utils/miscUtils'

export interface GameInfoContext {
    value: GameInfoValue
    set: (
        units: GameInfoValue['units'],
        items: GameInfoValue['items'],
        traits: GameInfoValue['traits'],
        notes: GameInfoValue['notes'],
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
    unitsByAlphabeticalIndex: Record<number, string>
    alphaIndexByUnit: Record<string, number>

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
    itemsByAlphabeticalIndex: Record<number, string>
    alphaIndexByItem: Record<string, number>

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

    notes: Record<string, string[]>
}

const CONTEXT_KEY = 'game_info_context'

export function setGameInfoContext(): GameInfoContext {
    const value = {
        units: {},
        unitsByIndex: {},
        unitsByAlphabeticalIndex: {},
        alphaIndexByUnit: {},
        items: {},
        itemsByIndex: {},
        itemsByAlphabeticalIndex: {},
        alphaIndexByItem: {},
        traits: {},
        notes: {},
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
        notes: GameInfoValue['notes'],
    ) {
        const unitsByIndex: GameInfoValue['unitsByIndex'] = {}
        for (const unit of Object.values(units)) {
            unitsByIndex[unit.index] = unit.info.id
        }

        const itemsByIndex: GameInfoValue['itemsByIndex'] = {}
        for (const item of Object.values(items)) {
            itemsByIndex[item.index] = item.id
        }

        const unitsAlphabetical = alphabetical(
            [...Object.values(units)],
            (u) => u.info.cost.toString() + u.info.name,
        )
        const unitsByAlphabeticalIndex: GameInfoValue['unitsByAlphabeticalIndex'] = {}
        const alphaIndexByUnit: GameInfoValue['alphaIndexByUnit'] = {}
        for (const [idx, unit] of enumerate(unitsAlphabetical)) {
            unitsByAlphabeticalIndex[idx] = unit.info.id
            alphaIndexByUnit[unit.info.id] = idx
        }

        const itemsAlphabetical = alphabetical([...Object.values(items)], (u) => {
            let typeValue = ''
            switch (u.type) {
                case 'Component':
                    typeValue = 'z'
                    break
                case 'Completed':
                    typeValue = 'a'
                    break
            }

            return String(typeValue) + '_' + u.name
        })
        const itemsByAlphabeticalIndex: GameInfoValue['itemsByAlphabeticalIndex'] = {}
        const alphaIndexByItem: GameInfoValue['alphaIndexByItem'] = {}
        for (const [idx, item] of enumerate(itemsAlphabetical)) {
            itemsByAlphabeticalIndex[idx] = item.id
            alphaIndexByItem[item.id] = idx
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
                unitsByAlphabeticalIndex,
                alphaIndexByUnit,
                items,
                itemsByAlphabeticalIndex,
                alphaIndexByItem,
                itemsByIndex,
                traits,
                notes,
            }
        }
    }
}

export function getGameInfoContext(): GameInfoContext {
    return getContext(CONTEXT_KEY)
}
