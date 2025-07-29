import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
import { unpackItemIndices, unpackUnitIndex, unpackUnitStars } from '$lib/utils/networkUtils'

// Encodes unit id, items, etc into single number
export type PackedId = bigint

export interface ActiveSearchData {
    id: PackedId
    dps: number
}

export interface ActiveSearchColumn<TFilter = any> {
    id: string
    label: string
    getLabel: (opts: GetLabelOptions) => string
    sort?: {
        getValue: (d: ActiveSearchData, info: GameInfoValue) => number
        order: 'asc' | 'desc'
    }
    filter?: {
        prepare: (text: string, info: GameInfoValue) => TFilter[]
        isMatch: (d: ActiveSearchData, info: GameInfoValue, filter: TFilter) => boolean
        placeholder?: string
    }
}

interface GetLabelOptions {
    d: ActiveSearchData
    info: GameInfoValue
}

export const INDEX_COLUMN: ActiveSearchColumn = {
    id: 'index',
    label: '',
    getLabel: ({ d }) => 'todo',
}

export const DPS_COLUMN: ActiveSearchColumn = {
    id: 'dps',
    label: 'DPS',
    getLabel: ({ d }) => String(d.dps),
    sort: {
        getValue: (d) => d.dps,
        order: 'desc',
    },
}

export const UNIT_COLUMN: ActiveSearchColumn<{ unit: string; stars: Set<number> }> = {
    id: 'unit',
    label: 'Champion',
    getLabel: ({ d, info }) => {
        const index = unpackUnitIndex(d.id)
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
            const index = unpackUnitIndex(d.id)
            const id = info.unitsByIndex[index]
            const unit = info.units[id]

            const stars = unpackUnitStars(d.id)

            const isNameMatch = unit.info.name.toLowerCase().includes(filter.unit)
            const isStarMatch = filter.stars.has(stars)
            return isNameMatch && isStarMatch
        },
        placeholder: '3* irelia, 2* malz',
    },
}

export const ITEM_COLUMN: ActiveSearchColumn<number> = {
    id: 'item',
    label: 'Items',
    getLabel: ({ d }) => 'todo',
    filter: {
        prepare: (text, info) => {
            const clauses = text.split(',').map((cl) => cl.toLowerCase())
            const matchingItemIndices = Object.values(info.items)
                .filter((item) => clauses.some((cl) => item.name.toLowerCase().includes(cl)))
                .map((item) => item.index)
            return matchingItemIndices
        },
        isMatch: (d, info, filter) => {
            return unpackItemIndices(d.id).some((idx) => idx === filter)
        },
        placeholder: 'gunblade, bloodthirster',
    },
}

export const TRAIT_COLUMN: ActiveSearchColumn = {
    id: 'trait',
    label: 'Traits',
    getLabel: ({ d }) => 'todo',
}

export const ACTIVE_SEARCH_COLUMNS = [
    INDEX_COLUMN,
    DPS_COLUMN,
    UNIT_COLUMN,
    ITEM_COLUMN,
    TRAIT_COLUMN,
]
