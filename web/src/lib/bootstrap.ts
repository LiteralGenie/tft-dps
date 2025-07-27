import { IdbCache } from './idbCache'
import { fetchApiJson } from './utils/networkUtils'

export async function* bootstrap() {
    yield { type: 'load_cache' }
    const cache = await new IdbCache().init()
    ;(window as any).tft_cache = cache

    yield { type: 'load_game_info' }
    const units = await fetchApiJson('/info/units')
    const items = await fetchApiJson('/info/items')
    const traits = await fetchApiJson('/info/traits')

    return {
        cache,
        units,
        items,
        traits,
    }
}
