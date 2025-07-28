import { API_URL } from '$lib/constants'
import type { GameInfoContext } from '$lib/gameInfoContext.svelte'
import { range, sum } from 'radash'
import { assert } from './miscUtils'

const ID_COUNT_BYTES = 2
const ID_SIZE_BYTES = 1

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

 remaining are the active traits
 number of bits for each depends on number of tiers for trait
    eg 3 tiers means 2 bits, 9 tiers means 4 bits
   tier 3 / 9 = 0011
   tier 6 / 7 = 110
 */

export function packUnitId(
    infoCtx: GameInfoContext,
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

        const itemIndex = infoCtx.items[id].index
        return itemIndex
    })
    const unitIndex = infoCtx.units[unitId].index
    const traitTiers = infoCtx.units[unitId].info.traits.map((id) => {
        const tier = traitTierMap[id] ?? 0
        const maxTier = infoCtx.traits[id].breakpoints.length

        let bits
        if (maxTier < 2) {
            bits = 1
        } else if (maxTier < 4) {
            bits = 2
        } else if (maxTier < 8) {
            bits = 3
        } else if (maxTier < 16) {
            bits = 4
        } else {
            throw new Error()
        }

        return { tier, maxTier, bits }
    })

    // Unit (7 bits)
    let packedId = unitIndex
    let bitCount = 7

    // Stars (2 bits)
    packedId = (packedId << 2) | stars
    bitCount += 2

    // Items (6 bits each)
    for (let idx = 0; idx < 3; idx++) {
        packedId = (packedId << 6) | itemIndexes[idx]
        bitCount += 6
    }

    // Tiers (1-4 bits each)
    for (const d of traitTiers) {
        packedId = (packedId << d.bits) | d.tier
        bitCount += d.bits
    }

    const remBits = (2 ** 8) ** ID_SIZE_BYTES - bitCount
    packedId = packedId << remBits

    const idBytes = numToUint8BE(packedId, bitCount)

    console.log(idBytes, { unitIndex, stars, itemIndexes, traitTiers })
    return { idBytes, bitCount }
}

/** Little-endian */
export function numToUint8BE(n: number, numBits: number): Uint8Array {
    const numBytes = Math.ceil(numBits / 8)
    const arr = new Uint8Array(numBytes)

    let rem = n
    for (let idx = numBytes - 1; idx >= 0; idx -= 1) {
        arr[idx] = rem & 0xff
        rem = rem >> 8
    }

    return arr
}

/**
 * (id count) - (id 1 size) - (id 1) - (id 2 size) - ...
 */
export function packAllUnitIds(packedIds: Array<ReturnType<typeof packUnitId>>): Uint8Array {
    assert(packedIds.length < 2 ** (8 * ID_COUNT_BYTES))

    const bytesForIds = sum(packedIds.map((x) => Math.ceil(x.bitCount / 8)))
    const bytesForIdLength = ID_SIZE_BYTES * packedIds.length
    const bytesForIdCount = ID_COUNT_BYTES

    const totalBytes = bytesForIds + bytesForIdLength + bytesForIdCount
    const result = new Uint8Array(totalBytes)

    let byteOffset = 0

    setSliceBE(result, packedIds.length, byteOffset, ID_COUNT_BYTES)
    byteOffset += ID_COUNT_BYTES

    for (const { idBytes, bitCount } of packedIds) {
        const byteCount = idBytes.length

        setSliceBE(result, byteCount, byteOffset, ID_SIZE_BYTES)
        byteOffset += ID_SIZE_BYTES

        for (let idx = 0; idx < byteCount; idx++) {
            result[byteOffset + idx] = idBytes[idx]
        }
        byteOffset += byteCount
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
