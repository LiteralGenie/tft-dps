<script>
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'
    import UnitSection from './unitSection.svelte'

    const infoCtx = getGameInfoContext()
    const searchCtx = getSearchContext()

    onMount(() => {
        if (searchCtx.value.length === 0) {
            searchCtx.value.push(searchCtx.getDefaultEntry(infoCtx))
        }
    })
</script>

{#if searchCtx.value.length > 0}
    <div class="root flex">
        <UnitSection entry={searchCtx.value[0]} />
    </div>
{/if}

<style>
    .root {
        font-size: small;
    }

    .root :global(section h1) {
        font-size: medium;
    }
</style>
