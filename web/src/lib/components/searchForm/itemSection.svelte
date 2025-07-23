<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { alphabetical } from 'radash'
    import ItemRow from './itemRow.svelte'

    const gameInfo = getGameInfoContext()

    const itemInfo = alphabetical([...Object.values(gameInfo.items)], (u) => {
        let typeValue = 0
        switch (u.type) {
            case 'Component':
                typeValue = 0
                break
            case 'Completed':
                typeValue = -1
                break
        }

        return String(typeValue) + '_' + u.name
    })
</script>

<section class="flex flex-col">
    <h1 class="section-header">Items</h1>

    <div class="grid max-h-[40em] items-center overflow-auto">
        <span></span>
        <span>Name</span>
        <span>Info</span>

        {#each itemInfo as d}
            <ItemRow itemInfo={d} />
        {/each}
    </div>
</section>

<style>
    .grid {
        grid-template-columns: repeat(3, max-content);
        gap: 2rem;
    }
</style>
