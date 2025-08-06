<script lang="ts">
    import CheckmarkIcon from '$lib/components/icons/checkmarkIcon.svelte'
    import { getGameInfoContext, type GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { range, sort } from 'radash'
    import UnitIcon from './unitIcon.svelte'

    const { unitInfo }: { unitInfo: GameInfoValue['units'][string] } = $props()
    const unitId = $derived(unitInfo.info.id)

    const search = getSearchContext()
    const searchUnits = $derived(search.value.units)
    const isSelected = $derived(searchUnits.has(unitInfo.info.id))

    const {
        value: { unitsByAlphabeticalIndex, alphaIndexByUnit },
    } = getGameInfoContext()

    let enableRef: HTMLInputElement

    function onClick(ev: MouseEvent) {
        if (searchUnits.has(unitId)) {
            searchUnits.delete(unitId)
        } else {
            searchUnits.add(unitId)
        }

        const hasShift = ev.getModifierState('Shift')
        const alphaIndex = alphaIndexByUnit[unitInfo.info.id]
        if (hasShift && search.lastUnitTouched !== null) {
            const [start, end] = sort([alphaIndex, search.lastUnitTouched], (x) => x)

            for (const otherAlphaIndex of range(start, end)) {
                if (otherAlphaIndex === alphaIndex || otherAlphaIndex === search.lastUnitTouched) {
                    continue
                }

                const otherUnitId = unitsByAlphabeticalIndex[otherAlphaIndex]

                if (searchUnits.has(otherUnitId)) {
                    searchUnits.delete(otherUnitId)
                } else {
                    searchUnits.add(otherUnitId)
                }
            }

            window.getSelection()?.removeAllRanges()
        }

        search.lastUnitTouched = alphaIndex
    }

    $effect(() => {
        enableRef.checked = searchUnits.has(unitId)
    })
</script>

<button
    onclick={onClick}
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
