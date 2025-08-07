<script lang="ts">
    import type { ActiveSearchData } from '$lib/activeSearchContext/activeSearchConstants'
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSimDetailsContext } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import {
        unpackItemIndices,
        unpackTraits,
        unpackUnitIndex,
        unpackUnitStars,
    } from '$lib/utils/networkUtils'
    import { range, sort } from 'radash'
    import DpsDetails from './dpsDetails/dpsDetails.svelte'
    import DpsTableDmgDistributionIcon from './dpsTableDmgDistributionIcon.svelte'
    import DpsTableItemIcon from './dpsTableItemIcon.svelte'
    import DpsTableRowDetailsTrigger from './dpsTableRowDetailsTrigger.svelte'
    import DpsTableTraitIcon from './dpsTableTraitIcon.svelte'
    import DpsTableUnitIcon from './dpsTableUnitIcon.svelte'

    const { d, idx }: { d: ActiveSearchData; idx: number } = $props()

    const { value: info } = getGameInfoContext()

    const ctx = getActiveSearchContext()

    const unit = $derived.by(() => {
        const unitIndex = unpackUnitIndex(d.id)
        const unitId = info.unitsByIndex[unitIndex]
        const unit = info.units[unitId]
        return unit
    })

    const stars = $derived(unpackUnitStars(d.id))

    const items = $derived.by(() => {
        const itemIndices = unpackItemIndices(d.id)
        const items = itemIndices
            .filter((index) => index > 0)
            .map((index) => info.itemsByIndex[index])
            .map((id) => info.items[id])
        return items
    })

    const traits = $derived(sort(unpackTraits(d.id, info), (trait) => trait.tier))

    const offset = $derived(ctx.pageIdx * ctx.pageSize)

    let showDetails = $state(false)

    const detailsCtx = getSimDetailsContext()
    const details = $derived(detailsCtx.sims.get(d.id))
</script>

<span class="td index">#{offset + idx + 1}</span>
<span class="td text-base! flex flex-col justify-center gap-1 font-bold">
    <span>{d.dps.toFixed(0)}</span>
    <DpsTableDmgDistributionIcon id={d.id} />
</span>
<span class="td flex gap-2">
    <DpsTableUnitIcon {unit} {stars} />
    <span class="whitespace-nowrap">{stars}* {unit.info.name}</span>
</span>
<span class="td flex gap-1">
    {#each [...range(0, 2)] as idx}
        <DpsTableItemIcon item={items[idx] ?? null} />
    {/each}
</span>
<span class="td py-2!">
    {#each traits as trait}
        <DpsTableTraitIcon trait={info.traits[trait.id]} tier={trait.tier} />
    {/each}
</span>
<span class="td p-0! bg-foreground/3 h-full">
    <DpsTableRowDetailsTrigger open={showDetails} onclick={() => (showDetails = !showDetails)} />
</span>

<span class:hidden={!showDetails} class="border-foreground/10 col-span-6 border-t px-12 py-8">
    <DpsDetails id={d.id} />
</span>
