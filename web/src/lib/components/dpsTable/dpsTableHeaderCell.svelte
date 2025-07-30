<script lang="ts">
    import type { ActiveSearchColumn } from '$lib/activeSearchContext/activeSearchConstants'
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import FunnelIcon from '$lib/components/icons/funnelIcon.svelte'

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
        <div class="relative">
            <input
                bind:this={inputEl}
                type="text"
                class="text-foreground! w-full border-gray-200 bg-transparent py-1 pl-1.5 pr-6 text-xs"
                placeholder={col.filter?.placeholder}
                oninput={onInput}
            />

            <div class="p-1.25 absolute bottom-0 right-0 top-0 pr-[0.25em] opacity-30">
                <FunnelIcon class="size-full" />
            </div>
        </div>
    {/if}
</div>
