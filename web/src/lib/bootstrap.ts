import { API_URL } from './constants'
import { IdbCache } from './idbCache'

export async function* bootstrap() {
    yield { type: 'load_cache' }
    const cache = await new IdbCache().init()
    ;(window as any).tft_cache = cache

    yield { type: 'load_game_info' }
    const units = await (await fetch(API_URL + '/info/units')).json()
    const items = await (await fetch(API_URL + '/info/items')).json()
    const traits = await (await fetch(API_URL + '/info/traits')).json()

    return {
        cache,
        units,
        items,
        traits,
    }
}
