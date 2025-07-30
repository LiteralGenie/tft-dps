<script lang="ts">
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import Checkbox from '../checkbox.svelte'

    const search = getSearchContext()
</script>

<section>
    <h1>Traits</h1>

    <div class="flex gap-4 pt-1">
        <Checkbox bind:checked={search.value.traits['prismatic']} label="Prismatic" />
        <Checkbox bind:checked={search.value.traits['gold']} label="Gold" />
        <Checkbox bind:checked={search.value.traits['silver']} label="Silver" />
        <Checkbox bind:checked={search.value.traits['bronze']} label="Bronze" />
        <Checkbox bind:checked={search.value.traits['inactive']} label="Inactive" />
    </div>
</section>
