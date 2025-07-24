<script lang="ts" module>
    import SearchFormDialog from '../searchForm/searchFormDialog.svelte'
    import DpsTableBody from './dpsTableBody.svelte'
    import DpsTableHeader from './dpsTableHeader.svelte'

    export interface DpsTableRow {
        dps: number
        unitId: string
        stars: number
        items: Record<string, number>
        traits: Record<string, number>
    }

    let showDialog = $state(false)
</script>

<SearchFormDialog open={showDialog} on:close={() => (showDialog = false)} />

<div class="root m-auto flex max-w-[70rem] flex-col">
    <button onclick={() => (showDialog = true)} class="mb-4 self-end rounded-md border px-4 py-2"
        >Configure</button
    >

    <div class="grid-container rounded-md border p-2">
        <DpsTableHeader />
        <DpsTableBody />
    </div>
</div>

<style lang="css">
    /* Grid */
    .grid-container {
        display: grid;
        grid-template-columns: max-content 1fr 1fr 1fr 1fr;
    }

    /* Padded rows */
    .root :global(.td),
    .root :global(.th) {
        padding: 0.5rem 1rem;
    }

    /* Header emphasis */
    .root :global(.th) {
        font-weight: bold;
    }
    .root :global(.td) {
        font-size: smaller;
    }

    /* Row borders */
    .root :global(.td) {
        border-top: 1px solid var(--color-foreground);
    }

    /* Index col */
    .root :global(.index) {
        padding-right: 1rem;
        color: color-mix(in oklab, var(--color-foreground), transparent 30%);
    }
</style>
