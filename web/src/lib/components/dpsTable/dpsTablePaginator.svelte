<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import DpsTablePageButton from './dpsTablePageButton.svelte'
    import DpsTablePageJump from './dpsTablePageJump.svelte'

    /**
      [first] [prev] [1] [2] [...] [i] [...] [n-1] [n] [next] [last] 
    */

    const { className }: { className?: string } = $props()

    const ctx = getActiveSearchContext()

    let elapsed = $state(0)
    $effect(() => {
        const timerId = setInterval(() => {
            const p = ctx.value?.progress
            if (!p) {
                elapsed = 0
                return
            }

            if (p.end) {
                elapsed = p.end - p.start
                return
            }

            elapsed = Date.now() - p.start
        }, 250)

        return () => clearInterval(timerId)
    })

    const numPages = $derived.by(() => {
        const numItems = ctx.value?.data.sortedFilteredIds.length ?? 0
        return Math.ceil(numItems / ctx.pageSize)
    })
</script>

<div>
    <div class="flex w-full justify-center gap-2 rounded text-sm text-gray-200 {className}">
        <DpsTablePageButton label="first" onclick={() => null} />
        <DpsTablePageButton label="prev" onclick={() => null} />

        <DpsTablePageJump />

        <DpsTablePageButton label="next" onclick={() => null} />
        <DpsTablePageButton label="last" onclick={() => null} />
    </div>

    {#if elapsed > 0}
        <p class="flex w-full justify-center pt-4 text-xs opacity-60">
            Fetched {ctx?.value?.data.sortedFilteredIds.length ?? '??'} results / {numPages} pages in
            {elapsed}ms
        </p>
    {/if}
</div>
