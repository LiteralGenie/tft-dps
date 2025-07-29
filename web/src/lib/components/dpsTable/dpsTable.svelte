<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { getSearchContext } from '$lib/searchContext.svelte'
    import SearchFormDialog from '../searchForm/searchFormDialog.svelte'
    import DpsTableBody from './dpsTableBody.svelte'
    import DpsTableHeader from './dpsTableHeader.svelte'

    let showDialog = $state(false)

    const search = getSearchContext()
    const activeSearch = getActiveSearchContext()

    function onClose() {
        showDialog = false
        activeSearch.set(search.value)
    }
</script>

<SearchFormDialog open={showDialog} on:close={onClose} />

<div class="root m-auto flex max-w-max flex-col">
    <button onclick={() => (showDialog = true)} class="mb-4 self-end rounded-md border px-4 py-2">
        Configure
    </button>

    <div class="grid-container rounded-md border px-2">
        <DpsTableHeader />
        <DpsTableBody />
    </div>
</div>

<style lang="css">
    /* Grid */
    .grid-container {
        display: grid;
        grid-template-columns: 5em 5em 15em 10em 11em;
    }

    /* Padded rows */
    .root :global(.th) {
        padding: 1em 1em;
    }
    .root :global(.td) {
        padding: 0.5em 1em;
    }

    /* Smaller body */
    .root :global(.td) {
        font-size: smaller;
    }

    /* Row borders */
    .root :global(.td) {
        border-top: 1px solid var(--color-foreground);
    }

    /* Index col */
    .root :global(.index) {
        padding-right: 1em;
        color: color-mix(in oklab, var(--color-foreground), transparent 30%);
        /* justify-content: start !important; */
    }

    /** Alignment */
    .root :global(.th) {
        display: flex;
        align-items: start;
        justify-content: end;
    }
    .root :global(.td) {
        display: flex;
        align-items: center;
    }
</style>
