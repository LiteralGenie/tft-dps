<script lang="ts">
    import CheckmarkIcon from '$lib/components/icons/checkmarkIcon.svelte'
    import { getGameInfoContext, type GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { range, sort } from 'radash'
    import ItemIcon from './itemIcon.svelte'

    const { itemInfo }: { itemInfo: GameInfoValue['items'][string] } = $props()

    const {
        value: { itemsByAlphabeticalIndex, alphaIndexByItem },
    } = getGameInfoContext()

    const search = getSearchContext()
    const searchItems = $derived(search.value.items)
    const isSelected = $derived(searchItems.has(itemInfo.id) && !search.value.onlyItemRecs)

    let enableRef: HTMLInputElement

    function onEnableChange(ev: MouseEvent) {
        if (searchItems.has(itemInfo.id)) {
            searchItems.delete(itemInfo.id)
        } else {
            searchItems.add(itemInfo.id)
        }

        const hasShift = ev.getModifierState('Shift')
        const alphaIndex = alphaIndexByItem[itemInfo.id]
        console.log('shift', hasShift, alphaIndex, search.lastItemTouched)
        if (hasShift && search.lastItemTouched !== null) {
            const [start, end] = sort([alphaIndex, search.lastItemTouched], (x) => x)
            console.log(start, end)

            for (const otherAlphaIndex of range(start, end)) {
                if (otherAlphaIndex === alphaIndex || otherAlphaIndex === search.lastItemTouched) {
                    continue
                }

                const otherItemId = itemsByAlphabeticalIndex[otherAlphaIndex]

                if (searchItems.has(otherItemId)) {
                    searchItems.delete(otherItemId)
                } else {
                    searchItems.add(otherItemId)
                }
            }

            window.getSelection()?.removeAllRanges()
        }

        search.lastItemTouched = alphaIndex
    }

    $effect(() => {
        enableRef.checked = searchItems.has(itemInfo.id)
    })
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
