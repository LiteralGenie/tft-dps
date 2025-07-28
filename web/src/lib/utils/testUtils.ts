import type { GameInfoValue } from '$lib/gameInfoContext.svelte'

export function mockGameInfo(): GameInfoValue {
    return {
        units: {
            id_a: {
                index: 9,
                info: {
                    cost: 1,
                    id: 'id_a',
                    name: 'name_a',
                    icon: 'icon_a',
                    traits: ['id_c'],
                },
            },
        },
        unitsByIndex: {
            9: 'id_a',
        },
        items: {
            id_b: {
                desc: 'desc_b',
                icon: 'icon_b',
                type: 'type_b',
                name: 'name_b',
                id: 'id_b',
                index: 22,
            },
        },
        itemsByIndex: {
            22: 'id_b',
        },
        traits: {
            id_c: {
                breakpoints: [1, 2, 4, 8, 16],
                desc: 'desc_c',
                effects_bonus: {
                    effect_c: 'effect_c_value',
                },
                icon: 'icon_c',
                id: 'id_c',
                name: 'name_c',
                styles: [99, 99, 99, 99, 99],
                tiers: [
                    {
                        breakpoint: 1,
                        rarity: 'bronze',
                    },
                    {
                        breakpoint: 2,
                        rarity: 'silver',
                    },
                    {
                        breakpoint: 4,
                        rarity: 'gold',
                    },
                    {
                        breakpoint: 8,
                        rarity: 'prismatic',
                    },
                    {
                        breakpoint: 16,
                        rarity: 'unique',
                    },
                ],
            },
        },
        traitBits: {
            id_c: 3,
        },
    }
}
