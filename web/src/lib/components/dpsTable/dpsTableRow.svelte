<script lang="ts">
    import type { ActiveSearchData } from '$lib/activeSearchContext/activeSearchConstants'
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { unpackItemIndices, unpackTraits, unpackUnitIndex } from '$lib/utils/networkUtils'

    const { d, idx }: { d: ActiveSearchData; idx: number } = $props()

    const { value: info } = getGameInfoContext()

    const unit = $derived.by(() => {
        const unitIndex = unpackUnitIndex(d.id)
        const unitId = info.unitsByIndex[unitIndex]
        const unit = info.units[unitId]
        return unit
    })

    const items = $derived.by(() => {
        const itemIndices = unpackItemIndices(d.id)
        const items = itemIndices
            .filter((index) => index > 0)
            .map((index) => info.itemsByIndex[index])
            .map((id) => info.items[id])
        return items
    })

    const traits = $derived(unpackTraits(d.id, info))
</script>

<span class="td index">{idx + 1}_{d.id}</span>
<span class="td">portrait + stars {unit.info.id}</span>
<span class="td">{d.dps.toFixed(0)}</span>
<span class="td">{items.join(', ')}</span>
<span class="td">{JSON.stringify(traits)}</span>
