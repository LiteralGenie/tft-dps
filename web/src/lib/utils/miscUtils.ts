export function assert(cond: boolean, msg?: string) {
    if (!cond) {
        throw new Error(msg)
    }
}

export function getSortedInsertionIndex(xs: number[], x: number) {
    let low = 0
    let high = xs.length
    while (low < high) {
        const mid = (low + high) >> 1
        if (xs[mid] < x) {
            low = mid + 1
        } else {
            high = mid
        }
    }

    return low
}

export async function compressGzip(data: Uint8Array): Promise<Array<Uint8Array>> {
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

    return asCompressed
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
