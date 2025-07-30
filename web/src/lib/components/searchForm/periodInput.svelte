<script>
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'

    const search = getSearchContext()
</script>

<section class="flex flex-col gap-1">
    <h1>Simulation Period ({search.value.period}s)</h1>

    <div class="flex max-w-60 flex-col">
        <input
            bind:value={search.value.period}
            type="range"
            min="1"
            max="30"
            step="1"
            list="period-markers"
        />

        <div class="flex justify-between">
            <span>1</span>
            <span>15</span>
            <span>30</span>
        </div>
    </div>
</section>
