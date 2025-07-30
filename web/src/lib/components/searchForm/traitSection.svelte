<script lang="ts">
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import Checkbox from '../checkbox.svelte'

    const { value: searchCtx } = getSearchContext()
</script>

<section>
    <h1>Traits</h1>

    <div class="flex gap-4 pt-1">
        <Checkbox bind:checked={searchCtx.traits['prismatic']} label="Prismatic" />
        <Checkbox bind:checked={searchCtx.traits['gold']} label="Gold" />
        <Checkbox bind:checked={searchCtx.traits['silver']} label="Silver" />
        <Checkbox bind:checked={searchCtx.traits['bronze']} label="Bronze" />
        <Checkbox bind:checked={searchCtx.traits['inactive']} label="Inactive" />
    </div>
</section>
