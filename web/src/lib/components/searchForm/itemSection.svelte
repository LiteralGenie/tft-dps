<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { alphabetical } from 'radash'
    import Checkbox from '../checkbox.svelte'
    import ItemRow from './itemRow.svelte'

    const { value: info } = getGameInfoContext()
    const { value: searchCtx } = getSearchContext()

    const itemInfo = alphabetical([...Object.values(info.items)], (u) => {
        let typeValue = ''
        switch (u.type) {
            case 'Component':
                typeValue = 'z'
                break
            case 'Completed':
                typeValue = 'a'
                break
        }

        return String(typeValue) + '_' + u.name
    })
</script>

<section class="flex flex-col">
    <h1 class="section-header">Items</h1>

    <div class="pb-2 pt-1">
        <Checkbox label={'Only recommended items'} bind:checked={searchCtx.onlyItemRecs} />
    </div>

    <div class="flex flex-wrap items-center">
        {#each itemInfo as d}
            <ItemRow itemInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
