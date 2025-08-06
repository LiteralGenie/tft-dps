<script lang="ts">
    import {
        DETAILS_COLUMN,
        DPS_COLUMN,
        INDEX_COLUMN,
        ITEM_COLUMN,
        TRAIT_COLUMN,
        UNIT_COLUMN,
    } from '$lib/activeSearchContext/activeSearchConstants'
    import DpsTableHeaderCell from './dpsTableHeaderCell.svelte'
</script>

<div class="contents">
    <DpsTableHeaderCell col={INDEX_COLUMN} />
    <DpsTableHeaderCell col={DPS_COLUMN} />
    <DpsTableHeaderCell col={UNIT_COLUMN} />
    <DpsTableHeaderCell col={ITEM_COLUMN} />
    <DpsTableHeaderCell col={TRAIT_COLUMN} />
    <DpsTableHeaderCell col={DETAILS_COLUMN} />
</div>
