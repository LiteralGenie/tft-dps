<script lang="ts">
    import type { ActiveSearchData } from '$lib/activeSearchContext/activeSearchConstants'
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import {
        unpackItemIndices,
        unpackTraits,
        unpackUnitIndex,
        unpackUnitStars,
    } from '$lib/utils/networkUtils'
    import { range, sort } from 'radash'
    import DpsTableItemIcon from './dpsTableItemIcon.svelte'
    import DpsTableTraitIcon from './dpsTableTraitIcon.svelte'
    import DpsTableUnitIcon from './dpsTableUnitIcon.svelte'

    const { d, idx }: { d: ActiveSearchData; idx: number } = $props()

    const { value: info } = getGameInfoContext()

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
</script>

<span class="td index">#{idx + 1}</span>
<span class="td">{d.dps.toFixed(0)}</span>
<span class="td flex gap-2">
    <DpsTableUnitIcon {unit} {stars} />
    <span class="whitespace-nowrap">{stars}* {unit.info.name}</span>
</span>
<span class="td flex gap-1">
    {#each [...range(0, 2)] as idx}
        <DpsTableItemIcon item={items[idx] ?? null} />
    {/each}
</span>
<span class="td py-0!">
    {#each traits as trait}
        <DpsTableTraitIcon trait={info.traits[trait.id]} tier={trait.tier} />
    {/each}
</span>
