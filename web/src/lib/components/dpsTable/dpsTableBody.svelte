<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import DpsTableRow from './dpsTableRow.svelte'

    const ctx = getActiveSearchContext()

    const rows = $derived.by(() => {
        const ctxValue = ctx.value
        if (!ctxValue) {
            return []
        }

        return ctxValue.data.sortedFilteredIds.map((id) => ctxValue.data.values.get(id)!)
    })
</script>

<div class="contents">
    {#each rows as d, idx}
        <DpsTableRow {d} {idx} />
    {/each}
</div>
