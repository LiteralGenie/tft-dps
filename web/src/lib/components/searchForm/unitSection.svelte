<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { alphabetical } from 'radash'
    import Checkbox from '../checkbox.svelte'
    import UnitRow from './unitRow.svelte'

    const { value: info } = getGameInfoContext()
    const { value: searchCtx } = getSearchContext()

    const unitInfo = alphabetical(
        [...Object.values(info.units)],
        (u) => u.info.cost.toString() + u.info.name,
    )
</script>

<section class="flex flex-col">
    <h1 class="section-header">Units</h1>

    <div class="flex gap-4 pb-2 pt-1">
        <Checkbox bind:checked={searchCtx.stars[1]} label="1 Star" />
        <Checkbox bind:checked={searchCtx.stars[2]} label="2 Stars" />
        <Checkbox bind:checked={searchCtx.stars[3]} label="3 Stars" />
    </div>

    <div class="flex flex-wrap items-center">
        {#each unitInfo as d}
            <UnitRow unitInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
