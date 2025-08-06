<script lang="ts">
    import { type SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'

    const { details }: { details: SimDetails | undefined } = $props()
</script>

<div>
    {#if details}
        <pre class="text-xs">{JSON.stringify(details, null, 2)}</pre>
    {:else}
        fetching...
    {/if}
</div>
