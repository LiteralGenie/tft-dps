<script>
    import ItemSection from './itemSection.svelte'
    import TraitSection from './traitSection.svelte'
    import UnitSection from './unitSection.svelte'
</script>

<div class="root flex flex-col">
    <TraitSection />
    <UnitSection />
    <ItemSection />
</div>

<style>
    .root {
        font-size: small;
    }

    .root :global(section h1) {
        font-size: medium;
    }
</style>
