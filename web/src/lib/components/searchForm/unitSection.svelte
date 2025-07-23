<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import type { SearchContextEntry } from '$lib/searchContext.svelte'
    import { alphabetical } from 'radash'
    import UnitRow from './unitRow.svelte'

    export let entry: SearchContextEntry

    const infoCtx = getGameInfoContext()

    const units = alphabetical(
        [...Object.values(infoCtx.units)],
        (u) => u.info.cost.toString() + u.info.name,
    )
</script>

<section class="flex flex-col">
    <h1 class="section-header">Units</h1>

    <div class="grid max-h-[40em] items-center overflow-auto">
        <span></span>
        <span>Name</span>
        <span>Stars</span>
        <span>Info</span>

        {#each units as unit}
            <UnitRow unit={entry.units[unit.info.id]} />
        {/each}
    </div>
</section>

<style>
    .grid {
        grid-template-columns: repeat(4, max-content);
        gap: 2rem;
    }
</style>
