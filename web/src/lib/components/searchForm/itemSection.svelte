<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { alphabetical } from 'radash'
    import ItemRow from './itemRow.svelte'

    const { value: info } = getGameInfoContext()

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

    <div class="flex flex-wrap items-center">
        {#each itemInfo as d}
            <ItemRow itemInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
