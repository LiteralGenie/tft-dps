<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { summarizeDamage } from '$lib/utils/simUtils'

    const { details }: { details: SimDetails } = $props()
    const activeSearch = getActiveSearchContext()

    const dist = $derived(summarizeDamage(details, activeSearch.value!.params.period))
</script>

<section class="flex flex-col gap-2 pb-8">
    <h1 class="font-semibold">Damage</h1>

    <div class="grid-container">
        <div class="row">
            <span class="tdd">Total Damage</span>
            <span class="tdd">{dist.total.totalString}</span>
            <span class="tdd">100%</span>
        </div>

        <div class="row divider-padding">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <span class="divider"></span>
        <div class="row divider-padding">
            <span></span>
            <span></span>
            <span></span>
        </div>

        <div class="row">
            <span class="tdd">Physical Damage</span>
            <span class="tdd">{dist.physical.totalString}</span>
            <span class="tdd">{dist.physical.frac}%</span>
        </div>

        <div class="row">
            <span class="tdd">Magical Damage</span>
            <span class="tdd">{dist.magical.totalString}</span>
            <span class="tdd">{dist.magical.frac}%</span>
        </div>

        <div class="row">
            <span class="tdd">True Damage</span>
            <span class="tdd">{dist.true.totalString}</span>
            <span class="tdd">{dist.true.frac}%</span>
        </div>

        <div class="row divider-padding">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <span class="divider"></span>
        <div class="row divider-padding">
            <span></span>
            <span></span>
            <span></span>
        </div>

        <div class="row">
            <span class="tdd">Auto Attacks ({dist.auto.count})</span>
            <span class="tdd">{dist.auto.totalString}</span>
            <span class="tdd">{dist.auto.frac}%</span>
        </div>

        <div class="row">
            <span class="tdd">Spells / Other ({dist.cast.count})</span>
            <span class="tdd">{dist.cast.totalString}</span>
            <span class="tdd">{dist.cast.frac}%</span>
        </div>
    </div>
</section>

<style>
    .grid-container {
        display: grid;
        grid-template-columns: max-content max-content max-content;
        line-height: 1;
        font-size: small;
        text-align: right;
    }

    .row {
        display: contents;
    }

    .tdd,
    .divider,
    .divider-padding > * {
        border-style: solid;
        border-color: color-mix(in oklab, var(--color-foreground), transparent 50%);
    }

    .tdd {
        padding: 0.25em 1rem;
    }

    .row:first-child .tdd {
        border-top-width: 1px;
        padding-top: 0.75em;
    }
    .row:last-child .tdd {
        border-bottom-width: 1px;
        padding-bottom: 0.75em;
    }

    .tdd:first-child,
    .row.divider-padding > :first-child {
        border-left-width: 1px;
        border-right-width: 1px;
    }
    .tdd:last-child,
    .row.divider-padding > :last-child {
        border-left-width: 1px;
        border-right-width: 1px;
    }

    .divider {
        grid-column: span 3 / span 3;
        height: 0.25em;
        border-left-width: 1px;
        border-right-width: 1px;
        border-top-width: 0.5px;
        border-bottom-width: 0.5px;
    }
    .row.divider-padding > * {
        height: 0.5em;
        width: auto;
    }
</style>
