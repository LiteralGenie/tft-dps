import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
import { unpackUnitIndex, unpackUnitStars } from '$lib/utils/networkUtils'

// Encodes unit id, items, etc into single number
export type PackedId = number

export interface ActiveSearchData {
    id: PackedId
    bitCount: number
    dps: number
}

export interface ActiveSearchColumn<TFilter = any> {
    id: string
    label: string
    getLabel: (d: ActiveSearchData, info: GameInfoValue) => string
    getSortValue?: (d: ActiveSearchData, info: GameInfoValue) => number
    filter?: {
        prepare: (text: string) => TFilter[]
        isMatch: (d: ActiveSearchData, info: GameInfoValue, filter: TFilter) => boolean
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
    getLabel: (d, info) => {
        const index = unpackUnitIndex(d.id, d.bitCount)
        const id = info.unitsByIndex[index]
        const unit = info.units[id]
        return unit.info.name
    },
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
            const index = unpackUnitIndex(d.id, d.bitCount)
            const id = info.unitsByIndex[index]
            const unit = info.units[id]

            const stars = unpackUnitStars(d.id, d.bitCount)

            const isNameMatch = unit.info.name.toLowerCase().includes(filter.unit)
            const isStarMatch = filter.stars.has(stars)
            return isNameMatch && isStarMatch
        },
    },
}

export const ACTIVE_SEARCH_COLUMNS = [DPS_COLUMN, UNIT_COLUMN]
