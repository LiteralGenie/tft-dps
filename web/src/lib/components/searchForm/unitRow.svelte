<script lang="ts">
    import CheckmarkIcon from '$lib/components/icons/checkmarkIcon.svelte'
    import { type GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'
    import UnitIcon from './unitIcon.svelte'

    const { unitInfo }: { unitInfo: GameInfoValue['units'][string] } = $props()
    const unitId = $derived(unitInfo.info.id)

    const { value: searchCtx } = getSearchContext()
    const isSelected = $derived(searchCtx.units.has(unitInfo.info.id))

    let enableRef: HTMLInputElement

    onMount(() => {
        enableRef.checked = searchCtx.units.has(unitId)
    })

    function onEnableChange() {
        enableRef.click()
        if (enableRef.checked) {
            searchCtx.units.add(unitId)
        } else {
            searchCtx.units.delete(unitId)
        }
        searchCtx.units = new Set(searchCtx.units)
    }
</script>

<button
    onclick={onEnableChange}
    class="transition-p duration-50 relative size-14 cursor-pointer p-1 opacity-35 hover:p-0 hover:opacity-70"
    class:opacity-100!={isSelected}
>
    <UnitIcon unit={unitInfo} />
    <input hidden bind:this={enableRef} type="checkbox" />
    <div
        class:hidden={!isSelected}
        class="icon p-0.75 absolute bottom-2 right-2 size-4 rounded-full bg-green-500"
    >
        <CheckmarkIcon class="stroke-4 stroke-white" />
    </div>
</button>

<style>
    button:hover .icon {
        height: 1.25rem;
        width: 1.25rem;
        transition: all 50ms;
        bottom: 0.25rem;
        right: 0.25rem;
    }
</style>
