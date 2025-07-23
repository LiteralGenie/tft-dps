<script lang="ts">
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import type { SearchContextUnit } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'

    export let unit: SearchContextUnit

    const infoCtx = getGameInfoContext()
    const unitInfo = infoCtx.units[unit.id]

    let enableRef: HTMLInputElement
    let minRef: HTMLInputElement
    let maxRef: HTMLInputElement

    onMount(() => {
        enableRef.checked = unit.enabled
        minRef.value = String(unit.minStars)
        maxRef.value = String(unit.maxStars)
    })

    function onEnableChange() {
        unit.enabled = enableRef.checked
    }

    function onMinChange() {
        unit.minStars = parseInt(minRef.value)
    }

    function onMaxChange() {
        unit.maxStars = parseInt(maxRef.value)
    }
</script>

<div class="contents">
    <span>
        <input on:change={onEnableChange} bind:this={enableRef} type="checkbox" />
    </span>

    <span>{unitInfo.info.name}</span>

    <span class="flex h-min items-center gap-2">
        <input on:change={onMinChange} bind:this={minRef} type="number" min="1" max="3" />
        <span>to</span>
        <input on:change={onMaxChange} bind:this={maxRef} type="number" min="1" max="3" />
    </span>

    <span class="flex flex-col">
        <span>{unitInfo.info.cost}-cost</span>
        <span> {unitInfo.info.traits.join(', ')} </span>
    </span>
</div>

<style>
    input {
        font-size: small;
        padding: 0.25em;
        width: 5ch;
    }
</style>
