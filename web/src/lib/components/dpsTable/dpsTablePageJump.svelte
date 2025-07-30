<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'

    const ctx = getActiveSearchContext()

    const max = $derived.by(() => {
        const numItems = ctx.value?.data.sortedFilteredIds.length ?? 1
        return Math.ceil(numItems / ctx.pageSize)
    })

    let inputEl: HTMLInputElement

    function onInputChange() {
        let update = parseInt(inputEl.value)

        if (isNaN(update)) {
            inputEl.value = String(ctx.pageIdx + 1)
            return
        }

        if (update < 1) {
            inputEl.value = '1'
            update = 1
        }
        if (update > max) {
            inputEl.value = String(max)
            update = max
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
