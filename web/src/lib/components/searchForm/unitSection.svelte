<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { alphabetical } from 'radash'
    import UnitRow from './unitRow.svelte'

    const gameInfo = getGameInfoContext()

    const unitInfo = alphabetical(
        [...Object.values(gameInfo.units)],
        (u) => u.info.cost.toString() + u.info.name,
    )
</script>

<section class="flex flex-col">
    <h1 class="section-header">Units</h1>

    <div class="grid max-h-[40em] items-center overflow-auto">
        <span></span>
        <span>Name</span>
        <span>Info</span>

        {#each unitInfo as d}
            <UnitRow unitInfo={d} />
        {/each}
    </div>
</section>

<style>
    .grid {
        grid-template-columns: repeat(3, max-content);
        gap: 2rem;
    }
</style>
