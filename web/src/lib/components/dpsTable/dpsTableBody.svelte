<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import LoaderIcon from '$lib/icons/loaderIcon.svelte'
    import DpsTableRow from './dpsTableRow.svelte'

    const ctx = getActiveSearchContext()

    const rows = $derived.by(() => {
        const ctxValue = ctx.value
        if (!ctxValue) {
            return []
        }

        const start = ctx.pageIdx * ctx.pageSize
        const end = (ctx.pageIdx + 1) * ctx.pageSize

        return ctxValue.data.sortedFilteredIds
            .map((id) => ctxValue.data.values.get(id)!)
            .slice(start, end)
    })
</script>

<div class="font-xs contents">
    {#if ctx.value?.progress.count !== ctx.value?.progress.total}
        <div class="col-span-5 flex items-center justify-center gap-2 border-t p-4 text-sm">
            <LoaderIcon class="size-6 fill-white text-white" />
            <span>Simulating {ctx.value!.progress.count} / {ctx.value!.progress.total} ...</span>
        </div>
    {/if}

    {#each rows as d, idx}
        <DpsTableRow {d} {idx} />
    {/each}

    {#if !ctx.value?.progress.total}
        <div class="col-span-5 flex w-full justify-center border-t p-4 opacity-75">No results!</div>
    {/if}
</div>
