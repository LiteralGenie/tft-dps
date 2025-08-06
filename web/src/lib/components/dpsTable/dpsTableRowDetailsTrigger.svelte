<script lang="ts">
    import ChevronDownIcon from '../icons/chevronDownIcon.svelte'

    const { open, onclick }: { open: boolean; onclick: () => void } = $props()
</script>

<!-- Trigger -->
<button
    {onclick}
    class="text-foreground/60 hover:bg-foreground/10 flex h-full w-full items-center justify-center gap-1 px-3"
>
    <!-- {#if open}
        <ChevronUpIcon class="stroke-foreground/60 size-4 stroke-2" />
    {:else}
        <ChevronDownIcon class="stroke-foreground/60 size-4 stroke-2" />
    {/if} -->

    <ChevronDownIcon
        class={{
            'stroke-foreground/60 transition-350 size-4 stroke-2 transition-all': true,
            'rotate-180': open,
        }}
    />
</button>

<style>
</style>
