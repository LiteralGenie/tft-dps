import type { GameInfoContext } from '$lib/gameInfoContext.svelte'

// Encodes unit id, items, etc into single number
export type PackedId = number

export interface ActiveSearchData {
    id: PackedId
    dps: number
    idUnit: string
    stars: number
    traits: Record<string, number>
    items: Record<string, number>
}

export interface ActiveSearchColumn<TFilter = any> {
    id: string
    label: string
    getLabel: (d: ActiveSearchData, info: GameInfoContext) => string
    getSortValue?: (d: ActiveSearchData, info: GameInfoContext) => number
    filter?: {
        prepare: (text: string) => TFilter[]
        isMatch: (d: ActiveSearchData, info: GameInfoContext, filter: TFilter) => boolean
    }
}

const DPS_COLUMN: ActiveSearchColumn = {
    id: 'dps',
    label: 'DPS',
    getLabel: (d) => String(d.dps),
    getSortValue: (d) => d.dps,
}

const UNIT_COLUMN: ActiveSearchColumn<{ unit: string; stars: Set<number> }> = {
    id: 'unit',
    label: 'Champion',
    getLabel: (d, info) => info.units[d.idUnit].info.name,
    getSortValue: (d, info) => info.units[d.idUnit].info.index,
    filter: {
        prepare: (text) => {
            const filters: Array<{ unit: string; stars: Set<number> }> = []

            const clauses = text.split(',')
            for (const c of clauses) {
                const words = c.split(' ')

                let stars, unit
                const m = (words[0] ?? '').trim().match(/(\d)+\*/)
                if (m?.[0]) {
                    stars = new Set([parseInt(m[0])])
                    unit = words.slice(1).join(' ')
                } else {
                    stars = new Set([1, 2, 3])
                    unit = words.join(' ')
                }

                unit = unit.toLowerCase()

                filters.push({ unit, stars })
            }

            return filters
        },
        isMatch: (d, info, filter) => {
            const isNameMatch = info.units[d.idUnit].info.name.toLowerCase().includes(filter.unit)
            const isStarMatch = filter.stars.has(d.stars)
            return isNameMatch && isStarMatch
        },
    },
}

export const ACTIVE_SEARCH_COLUMNS = [DPS_COLUMN, UNIT_COLUMN]
