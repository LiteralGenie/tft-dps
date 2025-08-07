<script lang="ts">
    import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { getSimDetailsContext } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import DpsDetailsContributions from './dpsDetailsContributions.svelte'
    import DpsDetailsDamage from './dpsDetailsDamage.svelte'

    const { id }: { id: PackedId } = $props()

    const ctx = getSimDetailsContext()
    const activeSearch = getActiveSearchContext()

    const details = $derived(ctx.sims.get(id))
</script>

<div class="flex flex-col gap-6 text-sm">
    {#if details}
        <section>
            <h1 class="pb-2 font-semibold">General</h1>
            Simulation Period: {activeSearch.value!.params.period.toFixed(0)}s
        </section>

        <DpsDetailsDamage {details} />

        <DpsDetailsContributions {id} {details} />

        <section class="flex flex-col gap-2">
            <h1>Graph</h1>
        </section>

        <pre class="text-xs">{JSON.stringify(details, null, 2)}</pre>
    {:else}
        fetching...
    {/if}
</div>
