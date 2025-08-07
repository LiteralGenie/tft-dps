<script lang="ts">
    import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
    import { getSimDetailsContext } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import DpsDetailsDamage from './dpsDetailsDamage.svelte'

    const { id }: { id: PackedId } = $props()

    const ctx = getSimDetailsContext()

    const details = $derived(ctx.sims.get(id))
</script>

<div class="text-sm">
    {#if details}
        <DpsDetailsDamage {details} />

        <section class="flex flex-col gap-2">
            <h1>Item Contributions</h1>
        </section>

        <section class="flex flex-col gap-2">
            <h1>Trait Contributions</h1>
        </section>

        <section class="flex flex-col gap-2">
            <h1>Graph</h1>
        </section>

        <pre class="text-xs">{JSON.stringify(details, null, 2)}</pre>
    {:else}
        fetching...
    {/if}
</div>
