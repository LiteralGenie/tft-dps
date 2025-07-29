<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'

    const ctx = getActiveSearchContext()

    const max = $derived.by(() => {
        const numItems = ctx.value?.data.sortedFilteredIds.length ?? 1
        return Math.ceil(numItems / ctx.pageSize)
    })

    let inputEl: HTMLInputElement

    function onInputChange() {
        const update = parseInt(inputEl.value)
        const defaultUpdate = String(ctx.pageIdx + 1)

        if (isNaN(update)) {
            inputEl.value = defaultUpdate
            return
        }
        if (update < 1 || update > max) {
            inputEl.value = defaultUpdate
            return
        }

        ctx.pageIdx = update - 1
    }

    $effect(() => {
        inputEl.value = String(ctx.pageIdx + 1)
    })
</script>

<input
    onchange={onInputChange}
    bind:this={inputEl}
    type="number"
    {max}
    min="1"
    class="text-foreground! w-18 rounded-md bg-transparent"
/>
