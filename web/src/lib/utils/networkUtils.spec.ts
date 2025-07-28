import { describe, expect, it } from 'vitest'
import {
    packSimId,
    unpackItemIndices,
    unpackTraits,
    unpackUnitIndex,
    unpackUnitStars,
} from './networkUtils'
import { mockGameInfo } from './testUtils'

const info = mockGameInfo()

describe('', () => {
    const id = BigInt(0b0001001_11_010110_010110_010110_0000000000_010)

    it('packing should work', () => {
        const toCheck = packSimId(info, 'id_a', 3, ['id_b', 'id_b', 'id_b'], { id_c: 2 })
        expect(toCheck).toEqual(id)
    })

    it('unpacking should work', () => {
        expect(unpackUnitIndex(id)).toEqual(9)
        expect(unpackUnitStars(id)).toEqual(3)
        expect(unpackItemIndices(id)).toEqual([22, 22, 22])
        expect(unpackTraits(id, info)).toEqual([{ id: 'id_c', tier: 2 }])
    })
})
