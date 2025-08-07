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
    const infoCtx = getGameInfoContext()
    const activeSearch = getActiveSearchContext()

    const dist = $derived(summarizeDamage(details, activeSearch.value!.params.period))

    const contributions = $derived.by(() => {
        const unitId = infoCtx.value.unitsByIndex[unpackUnitIndex(id)]
        const stars = unpackUnitStars(id)
        const items = unpackItemIndices(id)
            .filter((itemIndex) => itemIndex > 0)
            .map((itemIndex) => infoCtx.value.itemsByIndex[itemIndex])
        const traits = Object.fromEntries(
            unpackTraits(id, infoCtx.value).map((x) => {
                const trait = infoCtx.value.traits[x.id]

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
            const newId = packSimId(infoCtx.value, unitId, stars, newItems, traits)

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

            const newId = packSimId(infoCtx.value, unitId, stars, items, newTraits)

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

<section class="flex flex-col gap-2 pb-8">
    <h1 class="font-semibold">Contributions</h1>

    {#each contributions.items as c}
        <div>
            {c.original} - {c.diff}
        </div>
    {/each}

    {#each contributions.traits as c}
        <div>
            {c.original} - {c.diff}
        </div>
    {/each}
</section>

<style>
</style>
