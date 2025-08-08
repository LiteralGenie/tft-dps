<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { summarizeDamage } from '$lib/utils/simUtils'

    const { details }: { details: SimDetails } = $props()
    const activeSearch = getActiveSearchContext()

    const dist = $derived(summarizeDamage(details, activeSearch.value!.params.period))
</script>

<section class="flex flex-col">
    <h1 class="font-semibold">Damage</h1>

    <p class="text-foreground/80 pb-2 pt-1 text-xs">Damage before mitigations (armor / mr).</p>

    <div class="grid-container bg-foreground/3 w-max pt-2">
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
            <span
                class={{
                    'tdd text-orange-300': true,
                    'text-orange-300/60': dist.physical.total === 0,
                }}
            >
                {dist.physical.totalString}
            </span>
            <span
                class={{
                    'tdd text-orange-300': true,
                    'text-orange-300/60': dist.physical.total === 0,
                }}
            >
                {dist.physical.frac}%
            </span>
        </div>

        <div class="row">
            <span class="tdd">Magical Damage</span>
            <span
                class={{
                    'tdd text-blue-300': true,
                    'text-blue-300/60': dist.magical.total === 0,
                }}
            >
                {dist.magical.totalString}
            </span>
            <span
                class={{
                    'tdd text-blue-300': true,
                    'text-blue-300/60': dist.magical.total === 0,
                }}
            >
                {dist.magical.frac}%
            </span>
        </div>

        <div class="row">
            <span class="tdd">True Damage</span>
            <span
                class={{
                    tdd: true,
                    'text-foreground/60': dist.true.total === 0,
                }}
            >
                {dist.true.totalString}
            </span>
            <span
                class={{
                    tdd: true,
                    'text-foreground/60': dist.true.total === 0,
                }}
            >
                {dist.true.frac}%
            </span>
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
            <span
                class={{
                    tdd: true,
                    'opacity-60': dist.auto.total === 0,
                }}
            >
                {dist.auto.totalString}
            </span>
            <span
                class={{
                    tdd: true,
                    'opacity-60': dist.auto.total === 0,
                }}
            >
                {dist.auto.frac}%
            </span>
        </div>

        <div class="row">
            <span class="tdd">Spells / Other ({dist.cast.count})</span>
            <span
                class={{
                    tdd: true,
                    'opacity-60': dist.cast.total === 0,
                }}
            >
                {dist.cast.totalString}
            </span>
            <span
                class={{
                    tdd: true,
                    'opacity-60': dist.cast.total === 0,
                }}
            >
                {dist.cast.frac}%
            </span>
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
