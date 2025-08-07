import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
import { API_URL } from '$lib/constants'
import { getContext, setContext } from 'svelte'
import { SvelteMap } from 'svelte/reactivity'

export interface SimDetailsContext {
    sims: SvelteMap<PackedId, SimDetails>
    _prefetchData: {
        batchId: string
        ids: string[]
    }
    fetchId: (id: PackedId) => Promise<SimDetails>
    prefetch: (ids: PackedId[]) => void
}

export interface SimDetails {
    attacks: SimDamage[]
    casts: SimDamage[]
    misc_damage: SimDamage[]
    initial_stats: {}
    final_stats: {}
}

interface SimDamage {
    t: number
    mult: number
    physical_damage: number
    magical_damage: number
    true_damage: number
}

const CONTEXT_KEY = 'SimDetailsContext'

export function setSimDetailsContext(): SimDetailsContext {
    const ctx = $state<SimDetailsContext>({
        sims: new SvelteMap(),
        _prefetchData: { batchId: '', ids: [] },
        fetchId,
        prefetch,
    })
    setContext(CONTEXT_KEY, ctx)
    return ctx

    async function fetchId(id: PackedId): Promise<SimDetails> {
        if (!ctx.sims.has(id)) {
            const resp = await fetch(API_URL + `/simulate/details/${id}`, {
                method: 'POST',
            })
            const details = await resp.json()
            ctx.sims.set(id, details)
        }

        return ctx.sims.get(id)!
    }

    async function prefetch(ids: PackedId[]) {
        const batchId = Date.now().toString()
        ctx._prefetchData.batchId = batchId

        for (const id of ids) {
            if (ctx._prefetchData.batchId !== batchId) {
                break
            }

            await fetchId(id)
        }
    }
}

export function getSimDetailsContext(): SimDetailsContext {
    return getContext(CONTEXT_KEY)
}
