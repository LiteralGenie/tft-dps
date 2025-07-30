<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { alphabetical } from 'radash'
    import StarCheckbox from './starCheckbox.svelte'
    import UnitRow from './unitRow.svelte'

    const { value: info } = getGameInfoContext()

    const unitInfo = alphabetical(
        [...Object.values(info.units)],
        (u) => u.info.cost.toString() + u.info.name,
    )
</script>

<section class="flex flex-col">
    <h1 class="section-header">Units</h1>

    <div class="flex gap-4 pb-2 pt-1">
        <StarCheckbox key={1} label="1 Star" />
        <StarCheckbox key={2} label="2 Stars" />
        <StarCheckbox key={3} label="3 Stars" />
    </div>

    <div class="flex flex-wrap items-center">
        {#each unitInfo as d}
            <UnitRow unitInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
