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

    function selectAll() {
        for (const itemId of Object.keys(info.items)) {
            searchCtx.items.add(itemId)
        }
        searchCtx.items = searchCtx.items
    }

    function deselectAll() {
        searchCtx.items.clear()
        searchCtx.items = searchCtx.items
    }
</script>

<section class="flex flex-col">
    <div class="flex items-stretch justify-between">
        <div class="flex flex-col">
            <h1 class="section-header">Items</h1>

            <div class="pb-2 pt-1">
                <Checkbox
                    label="Limit to recommended items"
                    bind:checked={searchCtx.onlyItemRecs}
                />
            </div>
        </div>

        <div class="my-auto flex justify-center gap-2 pr-6">
            {#snippet IconButton(Tag: Component, onclick: () => void)}
                <button
                    {onclick}
                    class="hover:bg-foreground/10 flex h-full flex-col rounded-md p-2 text-sm disabled:pointer-events-none disabled:opacity-50"
                    disabled={searchCtx.onlyItemRecs}
                >
                    <Tag class="size-5 grow" />
                </button>
            {/snippet}

            {@render IconButton(FourSquareIcon, selectAll)}
            {@render IconButton(TrashIcon, deselectAll)}
        </div>
    </div>

    <div class="flex flex-wrap items-center" class:pointer-events-none={searchCtx.onlyItemRecs}>
        {#each itemInfo as d}
            <ItemRow itemInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
