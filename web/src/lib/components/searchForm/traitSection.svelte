<script lang="ts">
    import TraitCheckbox from './traitCheckbox.svelte'
</script>

<section>
    <h1>Traits</h1>

    <div class="flex gap-4 pt-1">
        <TraitCheckbox key="silver" label="Silver" />
        <TraitCheckbox key="gold" label="Gold" />
        <TraitCheckbox key="prismatic" label="Prismatic" />
    </div>
</section>
