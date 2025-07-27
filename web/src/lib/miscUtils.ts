import { API_URL } from './constants'

export function assetUrl(path: string) {
    return `https://raw.communitydragon.org/pbe/game/${path}`
}

export async function fetchApiJson(path: string) {
    const resp = await fetch(API_URL + path)
    const data = await resp.json()
    return data
}

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
