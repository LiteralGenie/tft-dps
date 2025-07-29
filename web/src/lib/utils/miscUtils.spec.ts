import { describe, expect, it } from 'vitest'
import { iterCombinations } from './miscUtils'

describe('iterCombinations() should work', () => {
    it('for numbers', () => {
        const ex = [
            [1, 3, 5],
            [1, 3, 6],
            [1, 4, 5],
            [1, 4, 6],
            [2, 3, 5],
            [2, 3, 6],
            [2, 4, 5],
            [2, 4, 6],
        ]
        const actual = [...iterCombinations([1, 2], [3, 4], [5, 6])]
        expect(actual).toEqual(ex)
    })

    it('for arrays', () => {
        const ex = [
            [
                ['a', 'b'],
                ['e', 'f'],
            ],
            [
                ['a', 'b'],
                ['g', 'h'],
            ],
            [
                ['c', 'd'],
                ['e', 'f'],
            ],
            [
                ['c', 'd'],
                ['g', 'h'],
            ],
        ]
        const actual = [
            ...iterCombinations(
                [
                    ['a', 'b'],
                    ['c', 'd'],
                ],
                [
                    ['e', 'f'],
                    ['g', 'h'],
                ],
            ),
        ]
        expect(actual).toEqual(ex)
    })
})
