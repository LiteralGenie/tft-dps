<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { alphabetical } from 'radash'
    import { type Component } from 'svelte'
    import Checkbox from '../checkbox.svelte'
    import FourSquareIcon from '../icons/fourSquareIcon.svelte'
    import TrashIcon from '../icons/trashIcon.svelte'
    import ItemRow from './itemRow.svelte'

    const { value: info } = getGameInfoContext()
    const search = getSearchContext()

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

    function selectAll() {
        for (const itemId of Object.keys(info.items)) {
            search.value.items.add(itemId)
        }
        search.value.items = search.value.items
    }

    function deselectAll() {
        search.value.items.clear()
        search.value.items = search.value.items
    }
</script>

<section class="flex flex-col">
    <div class="flex items-stretch justify-between">
        <div class="flex flex-col">
            <h1 class="section-header">Items</h1>

            <div class="pb-2 pt-1">
                <Checkbox
                    label="Limit to recommended items"
                    bind:checked={search.value.onlyItemRecs}
                />
            </div>
        </div>

        <div class="my-auto flex justify-center gap-2 pr-6">
            {#snippet IconButton(Tag: Component, onclick: () => void)}
                <button
                    {onclick}
                    class="flex h-full flex-col rounded-md bg-blue-500/30 p-2 text-sm hover:bg-blue-500 disabled:pointer-events-none disabled:opacity-50"
                    disabled={search.value.onlyItemRecs}
                >
                    <Tag class="size-5 grow" />
                </button>
            {/snippet}

            {@render IconButton(FourSquareIcon, selectAll)}
            {@render IconButton(TrashIcon, deselectAll)}
        </div>
    </div>

    <div class="flex flex-wrap items-center" class:pointer-events-none={search.value.onlyItemRecs}>
        {#each itemInfo as d}
            <ItemRow itemInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
