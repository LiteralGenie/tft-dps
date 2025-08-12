<script lang="ts">
    import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSimDetailsContext } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { unpackItemIndices, unpackTraits, unpackUnitIndex } from '$lib/utils/networkUtils'
    import DpsDetailsContributions from './dpsDetailsContributions.svelte'
    import DpsDetailsDamage from './dpsDetailsDamage.svelte'
    import DpsDetailsDmgPlot from './dpsDetailsDmgPlot.svelte'
    import DpsDetailsEvents from './dpsDetailsEvents.svelte'
    import DpsDetailsStats from './dpsDetailsStats.svelte'

    const { id }: { id: PackedId } = $props()

    const ctx = getSimDetailsContext()
    const activeSearch = getActiveSearchContext()
    const info = getGameInfoContext()

    const details = $derived(ctx.sims.get(id))
    const notes = $derived.by(() => {
        const iv = info.value

        const unitNotes = iv.notes[iv.unitsByIndex[unpackUnitIndex(id)]]
        const itemNotes = unpackItemIndices(id)
            .filter((index) => index > 0)
            .flatMap((index) => iv.notes[iv.itemsByIndex[index]])
        const traitNotes = unpackTraits(id, iv).flatMap(({ id }) => iv.notes[id])

        return new Set([...unitNotes, ...itemNotes, ...traitNotes])
    })
</script>

<div class="flex flex-col gap-8 text-sm">
    {#if details}
        <section>
            <h1 class="pb-1 font-semibold">Notes</h1>
            <ul class="flex flex-col gap-0 pl-4">
                <li>
                    - Simulation Period: {activeSearch.value!.params.period.toFixed(0)}s
                </li>
                {#each notes as note}
                    <li>
                        - {note}
                    </li>
                {/each}
            </ul>
        </section>

        <DpsDetailsDamage {details} />

        <DpsDetailsContributions {id} {details} />

        <DpsDetailsDmgPlot {details} />

        <DpsDetailsEvents {details} />

        <DpsDetailsStats {details} />

        <!-- <pre class="text-xs">{JSON.stringify(details, null, 2)}</pre> -->
    {:else}
        fetching...
    {/if}
</div>
