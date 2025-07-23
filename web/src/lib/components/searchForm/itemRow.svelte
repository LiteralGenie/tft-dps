<script lang="ts">
    import { type GameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'

    export let itemInfo: GameInfoContext['items'][string]

    const searchCtx = getSearchContext()

    let enableRef: HTMLInputElement

    onMount(() => {
        enableRef.checked = searchCtx.units.has(itemInfo.id)
    })

    function onEnableChange() {
        if (enableRef.checked) {
            searchCtx.units.add(itemInfo.id)
        } else {
            searchCtx.units.delete(itemInfo.id)
        }
    }
</script>

<div class="contents">
    <span>
        <input on:change={onEnableChange} bind:this={enableRef} type="checkbox" />
    </span>

    <span>{itemInfo.name}</span>

    <span class="flex flex-col">
        <span>{itemInfo.desc}</span>
    </span>
</div>

<style>
    input {
        font-size: small;
        padding: 0.25em;
        width: 5ch;
    }
</style>
