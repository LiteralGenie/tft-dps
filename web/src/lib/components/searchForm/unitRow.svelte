<script lang="ts">
    import CheckmarkIcon from '$lib/components/icons/checkmarkIcon.svelte'
    import { type GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import UnitIcon from './unitIcon.svelte'

    const { unitInfo }: { unitInfo: GameInfoValue['units'][string] } = $props()
    const unitId = $derived(unitInfo.info.id)

    const search = getSearchContext()
    const isSelected = $derived(search.value.units.has(unitInfo.info.id))

    let enableRef: HTMLInputElement

    function onEnableChange() {
        enableRef.click()
        if (enableRef.checked) {
            search.value.units.add(unitId)
        } else {
            search.value.units.delete(unitId)
        }
        // search.value.units = new Set(search.value.units)
    }

    $effect(() => {
        enableRef.checked = search.value.units.has(unitId)
    })
</script>

<button
    onclick={onEnableChange}
    class="transition-p duration-50 relative size-14 cursor-pointer p-1 opacity-35 hover:p-0 hover:opacity-70"
    class:opacity-100!={isSelected}
>
    <UnitIcon unit={unitInfo} />
    <input hidden bind:this={enableRef} type="checkbox" checked={search.value.units.has(unitId)} />
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
