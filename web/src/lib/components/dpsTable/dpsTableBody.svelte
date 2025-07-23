<script lang="ts">
    import type { DpsTableRow } from './dpsTable.svelte'

    let data: DpsTableRow[] = [
        { dps: 120, unitId: 'unitId', stars: 1, items: {}, traits: {} },
        { dps: 120, unitId: 'unitId', stars: 1, items: {}, traits: {} },
    ]
</script>

<div class="contents">
    {#each data as d, idx}
        <span class="td index">{idx + 1}</span>
        <span class="td">portrait + stars</span>
        <span class="td">dps</span>
        <span class="td">items</span>
        <span class="td">traits</span>
    {/each}
</div>
