<script lang="ts">
    import CheckmarkIcon from '$lib/components/icons/checkmarkIcon.svelte'
    import { type GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { SvelteSet } from 'svelte/reactivity'
    import ItemIcon from './itemIcon.svelte'

    const { itemInfo }: { itemInfo: GameInfoValue['items'][string] } = $props()

    const search = getSearchContext()
    const isSelected = $derived(search.value.items.has(itemInfo.id) && !search.value.onlyItemRecs)

    let enableRef: HTMLInputElement

    function onEnableChange() {
        enableRef.click()
        if (enableRef.checked) {
            search.value.items.add(itemInfo.id)
        } else {
            search.value.items.delete(itemInfo.id)
        }
        search.value.items = new SvelteSet(search.value.items)
    }
</script>

<button
    onclick={onEnableChange}
    class="transition-p duration-50 relative size-14 cursor-pointer p-1 opacity-35 hover:p-0 hover:opacity-70"
    class:opacity-100!={isSelected}
>
    <ItemIcon {itemInfo} />
    <input
        hidden
        bind:this={enableRef}
        type="checkbox"
        checked={search.value.items.has(itemInfo.id)}
    />
    <div
        class:hidden={!isSelected}
        class="icon absolute bottom-2 right-2 size-4 rounded-full bg-green-500 p-1"
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

    button:hover .icon {
        height: 1.125rem;
        width: 1.125rem;
        padding: 0.25rem;
        /* transition: height 50ms; */
        bottom: 0.375rem;
        right: 0.375rem;
    }
</style>
