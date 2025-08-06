<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { sort } from 'radash'
    import { type Component } from 'svelte'
    import Checkbox from '../checkbox.svelte'
    import FourSquareIcon from '../icons/fourSquareIcon.svelte'
    import TrashIcon from '../icons/trashIcon.svelte'
    import UnitRow from './unitRow.svelte'

    const { value: info } = getGameInfoContext()
    const search = getSearchContext()

    // prettier-ignore
    const unitInfo = sort(
        Object.entries(info.unitsByAlphabeticalIndex),
        ([idx, _]) => parseInt(idx),
    ).map(([_, unitId]) => info.units[unitId])

    function selectAll() {
        for (const unitId of Object.keys(info.units)) {
            search.value.units.add(unitId)
        }
        search.value.units = search.value.units
    }

    function deselectAll() {
        search.value.units.clear()
        search.value.units = search.value.units
    }
</script>

<section>
    <div class="flex items-stretch justify-between">
        <div class="flex flex-col">
            <h1 class="section-header">Units</h1>

            <div class="flex gap-4 pb-2 pt-1">
                <Checkbox bind:checked={search.value.stars[1]} label="1 Star" />
                <Checkbox bind:checked={search.value.stars[2]} label="2 Stars" />
                <Checkbox bind:checked={search.value.stars[3]} label="3 Stars" />
            </div>
        </div>

        <div class="my-auto flex justify-center gap-2 pr-6">
            {#snippet IconButton(Tag: Component, onclick: () => void)}
                <button
                    {onclick}
                    class="flex h-full flex-col rounded-md bg-blue-500/30 p-2 text-sm hover:bg-blue-500"
                >
                    <Tag class="size-5 grow" />
                </button>
            {/snippet}

            {@render IconButton(FourSquareIcon, selectAll)}
            {@render IconButton(TrashIcon, deselectAll)}
        </div>
    </div>

    <div class="flex flex-wrap items-center">
        {#each unitInfo as d}
            <UnitRow unitInfo={d} />
        {/each}
    </div>
</section>

<style>
</style>
