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

    <div class="flex flex-wrap items-center">
        {#each unitInfo as d}
            <UnitRow unitInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
