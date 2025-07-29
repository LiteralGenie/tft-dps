<script lang="ts">
    import type { ActiveSearchColumn } from '$lib/activeSearchContext/activeSearchConstants'
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'

    const { col, className }: { col: ActiveSearchColumn; className?: string } = $props()

    const ctx = getActiveSearchContext()

    let inputEl: HTMLInputElement

    function onInput() {
        ctx.setFilter(col.id, inputEl.value)
    }
</script>

<div class="th {col.id} flex flex-col {className}">
    <span class="font-bold"> {col.label} </span>

    {#if col.filter}
        <input
            bind:this={inputEl}
            type="text"
            class="text-foreground! w-full bg-transparent p-1 text-xs"
            placeholder={col.filter?.placeholder}
            oninput={onInput}
        />
    {/if}
</div>
