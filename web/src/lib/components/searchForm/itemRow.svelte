<script lang="ts">
    import { type GameInfoContext } from '$lib/gameInfoContext.svelte'
    import CheckmarkIcon from '$lib/icons/checkmarkIcon.svelte'
    import { getSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'
    import ItemIcon from './itemIcon.svelte'

    const { itemInfo }: { itemInfo: GameInfoContext['items'][string] } = $props()

    const searchCtx = getSearchContext()
    const isSelected = $derived(searchCtx.items.has(itemInfo.id))

    let enableRef: HTMLInputElement

    onMount(() => {
        enableRef.checked = searchCtx.units.has(itemInfo.id)
    })

    function onEnableChange() {
        enableRef.click()
        if (enableRef.checked) {
            searchCtx.items.add(itemInfo.id)
        } else {
            searchCtx.items.delete(itemInfo.id)
        }
        searchCtx.items = new Set(searchCtx.items)
    }
</script>

<button
    onclick={onEnableChange}
    class="transition-p duration-50 relative size-14 cursor-pointer p-1 opacity-35 hover:p-0 hover:opacity-100"
    class:opacity-100={isSelected}
>
    <ItemIcon {itemInfo} className="size-12" />
    <input hidden bind:this={enableRef} type="checkbox" />
    <div
        class:hidden={!isSelected}
        class="icon p-0.75 absolute bottom-2 right-2 size-4 rounded-full bg-green-500"
    >
        <CheckmarkIcon class="stroke-4 stroke-white" />
    </div>
</button>

<style>
    input {
        font-size: small;
        padding: 0.25em;
        width: 5ch;
    }
</style>
