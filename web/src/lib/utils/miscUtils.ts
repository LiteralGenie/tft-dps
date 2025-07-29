import { last, sum } from 'radash'

export function assert(cond: boolean, msg?: string) {
    if (!cond) {
        throw new Error(msg)
    }
}

export function getSortedInsertionIndex<T = number>(xs: T[], x: number, get: (y: T) => number) {
    let low = 0
    let high = xs.length
    while (low < high) {
        const mid = (low + high) >> 1
        if (get(xs[mid]) < x) {
            low = mid + 1
        } else {
            high = mid
        }
    }

    return low
}

export async function compressGzip(data: Uint8Array): Promise<Uint8Array> {
    const asStream = new ReadableStream({
        start(controller) {
            controller.enqueue(data)
            controller.close()
        },
    })
        .pipeThrough(new CompressionStream('gzip'))
        .getReader()

    const asCompressed: Array<Uint8Array> = []
    while (true) {
        const { done, value } = (await asStream.read()) as {
            done: boolean
            value: Uint8Array
        }

        if (done) {
            break
        } else {
            asCompressed.push(value)
        }
    }

    const totalLength = sum(asCompressed.map((xs) => xs.length))
    const asConcat = new Uint8Array(totalLength)

    let i = 0
    for (const xs of asCompressed) {
        asConcat.set(xs, i)
        i += xs.length
    }
    return asConcat
}

// export async function decompressGzip(
//     data: Array<Uint8Array> | Array<ArrayBuffer>,
// ): Promise<string> {
//     const asStream = new ReadableStream({
//         start(controller) {
//             for (const arr of data) {
//                 controller.enqueue(arr)
//             }
//             controller.close()
//         },
//     })
//         .pipeThrough(new DecompressionStream('gzip'))
//         .getReader()

//     let parts: string[] = []
//     const decoder = new TextDecoder()
//     while (true) {
//         const { done, value } = (await asStream.read()) as {
//             done: boolean
//             value: Uint8Array
//         }
//         if (done) {
//             break
//         } else {
//             parts.push(decoder.decode(value, { stream: true }))
//         }
//     }

//     parts.push(decoder.decode())
//     return parts.join('')
// }

export function* iterCombinations<T = any>(
    ...arrs: Array<Array<any>>
): Generator<unknown, void, T> {
    assert(arrs.length > 0)

    const lst = last(arrs)!
    if (arrs.length === 1) {
        for (const x of lst) {
            yield [x]
        }
    } else {
        const item = iterCombinations(arrs.slice(0, -1))
        for (const x of lst) {
            yield [...item, x]
        }
    }
}

export function* iterBatches<T>(xs: Iterable<T>, n: number): Iterable<T[]> {
    let buf: T[] = []

    for (const x of xs) {
        buf.push(x)
        if (buf.length === n) {
            yield buf
            buf = []
        }
    }

    if (buf.length > 0) {
        yield buf
    }
}

export function enumerate<T>(xs: T[]): Array<[number, T]> {
    return xs.map((x, idx) => [idx, x])
}

export function costToRarity(c: number) {
    switch (c) {
        case 5:
            return 'legendary'
        case 4:
            return 'epic'
        case 3:
            return 'rare'
        case 2:
            return 'uncommon'
        case 1:
            return 'common'
        default:
            throw new Error()
    }
}
