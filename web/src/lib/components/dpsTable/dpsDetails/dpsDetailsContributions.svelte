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
                diff = {
                    total: dist.total.total - newDist.total.total,
                    physical: dist.physical.total - newDist.physical.total,
                    magical: dist.magical.total - newDist.magical.total,
                    true: dist.true.total - newDist.true.total,
                }
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
                    diff: {
                        total: 0,
                        physical: 0,
                        magical: 0,
                        true: 0,
                    },
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
                diff = {
                    total: dist.total.total - newDist.total.total,
                    physical: dist.physical.total - newDist.physical.total,
                    magical: dist.magical.total - newDist.magical.total,
                    true: dist.true.total - newDist.true.total,
                }
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
        Damage lost if item is removed or trait level is set to 1.
    </p>

    <div class="grid-container bg-foreground/3 w-max">
        {#snippet divider()}
            <div class="row divider-padding">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span class="divider"></span>
            <div class="row divider-padding">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        {/snippet}

        {#snippet cont(label: string, c: (typeof contributions)['items'][number])}
            <div class="row">
                {#if c.diff}
                    <span class="tdd">{label}</span>
                    <span class="tdd">{Math.round(c.diff.total).toLocaleString()}</span>
                    <span class="tdd">{Math.round(c.diff.physical).toLocaleString()}</span>
                    <span class="tdd">{Math.round(c.diff.magical).toLocaleString()}</span>
                    <span class="tdd">{Math.round(c.diff.true).toLocaleString()}</span>
                {:else}
                    <span class="tdd">{label}</span>
                    <span class="tdd"> ... </span>
                    <span class="tdd"> ... </span>
                    <span class="tdd"> ... </span>
                    <span class="tdd"> ... </span>
                {/if}
            </div>
        {/snippet}

        <div class="row">
            <span class="tdd"></span>
            <span class="tdd">Total</span>
            <span class="tdd">Physical</span>
            <span class="tdd">Magical</span>
            <span class="tdd">True</span>
        </div>

        {@render divider()}

        {#each contributions.items as c}
            {@render cont(iv.items[c.original].name, c)}
        {/each}

        {@render divider()}

        {#each contributions.traits as c}
            {@render cont(iv.traits[c.original].name, c)}
        {/each}
    </div>
</section>

<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(5, max-content);
        line-height: 1;
        font-size: small;
        text-align: right;
    }
    .row {
        display: contents;
    }

    .tdd,
    .divider,
    .divider-padding > * {
        border-style: solid;
        border-color: color-mix(in oklab, var(--color-foreground), transparent 50%);
    }

    .tdd {
        padding: 0.25em 1rem;
    }

    .row:first-child .tdd {
        border-top-width: 1px;
        padding-top: 0.75em;
    }
    .row:last-child .tdd {
        border-bottom-width: 1px;
        padding-bottom: 0.75em;
    }

    .tdd,
    .row.divider-padding > * {
        border-left-width: 1px;
    }
    .tdd:last-child,
    .row.divider-padding > :last-child {
        border-right-width: 1px;
    }

    .divider {
        grid-column: span 5 / span 5;
        height: 0.25em;
        border-left-width: 1px;
        border-right-width: 1px;
        border-top-width: 0.5px;
        border-bottom-width: 0.5px;
    }
    .row.divider-padding > * {
        height: 0.5em;
        width: auto;
    }
</style>
