import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
import { API_URL } from '$lib/constants'
import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
import { range } from 'radash'
import { assert, enumerate } from './miscUtils'

const ID_BYTES = 5
const ID_BITS = 8 * ID_BYTES

export function assetUrl(path: string) {
    return `https://raw.communitydragon.org/pbe/game/${path}`
}

export async function fetchApiJson(path: string) {
    const resp = await fetch(API_URL + path)
    const data = await resp.json()
    return data
}

/**
 * unit     - ~60   -   7 bits
 * stars    -   3   -   2 bits
 * item 1   - ~44   -   6 bits
 * item 2   - ~44   -   6 bits
 * item 3   - ~44   -   6 bits
 * traits   - ???   -   13 bits
 *                    = 40 bits / 5 bytes
 *
 * of the 13 bits reserved for traits
 * the number of bits for each trait depends on
 * the number of breakpoints for that trait
 *
 * first trait is stored closest to end
 * ie ..._items_zeros_trait3_trait2_trait1
 */

export function packSimId(
    info: GameInfoValue,
    unitId: string,
    stars: number,
    itemIds: string[],
    traitTierMap: Record<string, number>,
) {
    const itemIndexes = [...range(0, 2)].map((idx) => {
        const id = itemIds[idx]
        if (!id) {
            return 0
        }

        const itemIndex = info.items[id].index
        return itemIndex
    })
    const unitIndex = info.units[unitId].index
    const traitTiers = info.units[unitId].info.traits.map((id) => {
        const tier = traitTierMap[id] ?? 0
        const maxTier = info.traits[id].breakpoints.length
        const bits = info.traitBits[id]
        return { tier, maxTier, bits }
    })

    // Unit (7 bits)
    let packedId = BigInt(unitIndex)

    // Stars (2 bits)
    packedId = (packedId << 2n) | BigInt(stars)

    // Items (6 bits each)
    for (let idx = 0; idx < 3; idx++) {
        packedId = (packedId << 6n) + BigInt(itemIndexes[idx])
    }

    // Traits (13 bits total)
    let traitOffset = 0
    packedId = packedId << 13n
    for (const d of traitTiers) {
        packedId += BigInt(d.tier << traitOffset)
        traitOffset += d.bits
    }

    return packedId
}

export function unpackUnitIndex(id: PackedId) {
    return Number(id >> BigInt(13 + 6 * 3 + 2)) & 0b1111111
}

export function unpackUnitStars(id: PackedId) {
    let x = id
    x = x >> BigInt(13 + 6 * 3)
    x = x & BigInt(0b11)
    return Number(x)
}

export function unpackItemIndices(id: PackedId) {
    return [unpack(0), unpack(1), unpack(2)]

    function unpack(idx: number) {
        let x = id
        x = x >> 13n
        x = x >> BigInt((3 - idx - 1) * 6)
        x = x & BigInt(0b111111)
        return Number(x)
    }
}

export function unpackTraits(id: PackedId, info: GameInfoValue) {
    const unitIndex = unpackUnitIndex(id)
    const unitId = info.unitsByIndex[unitIndex]
    const unit = info.units[unitId]

    const traits = unit.info.traits.map((id) => ({ id, tier: 0 }))

    let rem = Number(id & BigInt(0b0000000_00_000000_000000_000000_1111111111111))

    for (const [idx, trait] of enumerate(traits)) {
        const numBits = info.traitBits[trait.id]

        // 2 bits -> 0b11, 3 bits -> 0b111
        const mask = 2 ** (numBits + 1) - 1

        traits[idx].tier = rem & mask
        rem >> numBits
    }

    return traits
}

/** Big-endian */
export function biToUint8Be(n: bigint, numBytes: number): Uint8Array {
    const arr = new Uint8Array(numBytes)

    let rem = n
    for (let idx = numBytes - 1; idx >= 0; idx -= 1) {
        arr[idx] = Number(rem & BigInt(0xff))
        rem = rem >> 8n
    }

    return arr
}

export function ui8ToNumBe(bytes: Uint8Array): number {
    let num = 0
    for (let idx = 0; idx < bytes.length; idx++) {
        num |= bytes[idx] << (8 * idx)
    }
    return num
}

/**
 * (id count) - (id 1 size) - (id 1) - (id 2 size) - ...
 */
export function packAllUnitIds(packedIds: Array<PackedId>): Uint8Array {
    const ID_COUNT_BYTES = 2
    assert(packedIds.length < 2 ** (8 * ID_COUNT_BYTES))

    const totalBytes = ID_COUNT_BYTES + packedIds.length * ID_BYTES
    const result = new Uint8Array(totalBytes)

    let byteOffset = 0

    setSliceBE(result, packedIds.length, byteOffset, ID_COUNT_BYTES)
    byteOffset += ID_COUNT_BYTES

    for (const id of packedIds) {
        const idBytes = biToUint8Be(id, ID_BYTES)

        for (let idx = 0; idx < idBytes.length; idx++) {
            result[byteOffset + idx] = idBytes[idx]
        }
        byteOffset += idBytes.length
    }

    return result

    function setSliceBE(arr: Uint8Array, x: number, start: number, numBytes: number) {
        let rem = x
        for (let idx = numBytes - 1; idx >= 0; idx -= 1) {
            arr[start + idx] = rem & 0xff
            rem >>= 8
        }

        return arr
    }
}
