<script lang="ts">
    import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import {
        getSimDetailsContext,
        type SimDetails,
    } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import {
        packSimId,
        unpackItemIndices,
        unpackTraits,
        unpackUnitIndex,
        unpackUnitStars,
    } from '$lib/utils/networkUtils'
    import { summarizeDamage } from '$lib/utils/simUtils'
    import { debounce } from 'radash'

    const { id, details }: { id: PackedId; details: SimDetails } = $props()
    const detailsCtx = getSimDetailsContext()
    const { value: iv } = getGameInfoContext()
    const activeSearch = getActiveSearchContext()

    const dist = $derived(summarizeDamage(details, activeSearch.value!.params.period))

    const contributions = $derived.by(() => {
        const unitId = iv.unitsByIndex[unpackUnitIndex(id)]
        const stars = unpackUnitStars(id)
        const items = unpackItemIndices(id)
            .filter((itemIndex) => itemIndex > 0)
            .map((itemIndex) => iv.itemsByIndex[itemIndex])
        const traits = Object.fromEntries(
            unpackTraits(id, iv).map((x) => {
                const trait = iv.traits[x.id]

                if (trait.has_bp_1) {
                    const tier = trait.tiers[x.tier]
                    return [x.id, tier.breakpoint]
                } else if (x.tier === 0) {
                    return [x.id, 1]
                } else {
                    const tier = trait.tiers[x.tier - 1]
                    return [x.id, tier.breakpoint]
                }
            }),
        )

        // Remove each item
        const itemContributions = []
        for (let idx = 0; idx < items.length; idx++) {
            const newItems = [...items.slice(0, idx), ...items.slice(idx + 1)]
            const newId = packSimId(iv, unitId, stars, newItems, traits)

            let diff = null
            const newDetails = detailsCtx.sims.get(newId)
            if (newDetails) {
                const newDist = summarizeDamage(newDetails, activeSearch.value!.params.period)
                diff = dist.total.total - newDist.total.total
            }

            itemContributions.push({
                original: items[idx],
                newId,
                diff,
            })
        }

        // Remove each trait
        const traitContributions = []
        const traitIds = Object.keys(traits)
        for (const traitId of traitIds) {
            const newTraits = { ...traits }

            if (traits[traitId] === 1) {
                traitContributions.push({
                    original: traitId,
                    newId: id,
                    diff: 0,
                })
                continue
            } else {
                newTraits[traitId] = 1
            }

            const newId = packSimId(iv, unitId, stars, items, newTraits)

            let diff = null
            const newDetails = detailsCtx.sims.get(newId)
            if (newDetails) {
                const newDist = summarizeDamage(newDetails, activeSearch.value!.params.period)
                diff = dist.total.total - newDist.total.total
            }

            traitContributions.push({
                original: traitId,
                newId,
                diff,
            })
        }

        return {
            items: itemContributions,
            traits: traitContributions,
        }
    })

    const doFetch = debounce({ delay: 100 }, (ids: PackedId[]) => detailsCtx.prefetch(ids))
    $effect(() => {
        const ids = [...contributions.items, ...contributions.traits].map((x) => x.newId)
        doFetch(ids)
    })
</script>

<section class="flex flex-col">
    <h1 class="font-semibold">Contributions</h1>

    <p class="text-foreground/80 pb-2 pt-1 text-xs">
        Damage lost if item is removed or trait count is set to 1
    </p>

    <ul class="flex flex-col gap-1 pl-4">
        {#each contributions.items as c}
            <li>
                <!-- <DpsTableItemIcon item={iv.items[c.original]} /> -->
                <span class="">- {iv.items[c.original].name}:</span>
                <span class="font-semibold">{Math.round(c.diff ?? 0).toLocaleString()}</span>
            </li>
        {/each}

        {#each contributions.traits as c}
            <li>
                <!-- <DpsTableTraitIcon trait={iv.traits[c.original]} tier={0} showBp={false} /> -->
                <span>- {iv.traits[c.original].name}:</span>
                <span class="font-semibold">{Math.round(c.diff ?? 0).toLocaleString()}</span>
            </li>
        {/each}
    </ul>
</section>

<style>
</style>
