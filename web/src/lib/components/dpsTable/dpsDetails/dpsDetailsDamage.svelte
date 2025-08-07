<script lang="ts">
    import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { sum } from 'radash'

    const { details }: { details: SimDetails } = $props()

    const dist = $derived.by(() => {
        const allDamage = [...details.attacks, ...details.casts, ...details.misc_damage]

        const totalPhysical = sum(allDamage, (x) => x.mult * x.physical_damage)
        const totalMagical = sum(allDamage, (x) => x.mult * x.magical_damage)
        const totalTrue = sum(allDamage, (x) => x.mult * x.true_damage)

        const totalAll = totalPhysical + totalMagical + totalTrue

        const totalAuto = sum(
            details.attacks.flatMap((x) => [
                x.mult * x.physical_damage,
                x.mult * x.magical_damage,
                x.mult * x.true_damage,
            ]),
        )
        const totalCast = sum(
            [...details.casts, ...details.misc_damage].flatMap((x) => [
                x.mult * x.physical_damage,
                x.mult * x.magical_damage,
                x.mult * x.true_damage,
            ]),
        )

        return {
            total: { total: fmt(totalAll), frac: 1 },
            physical: {
                total: fmt(totalPhysical),
                frac: fmt(100 * (totalPhysical / totalAll)),
            },
            magical: {
                total: fmt(totalMagical),
                frac: fmt(100 * (totalMagical / totalAll)),
            },
            true: {
                total: fmt(totalTrue),
                frac: fmt(100 * (totalTrue / totalAll)),
            },
            auto: {
                total: fmt(totalAuto),
                frac: fmt(100 * (totalAuto / totalAll)),
            },
            cast: {
                total: fmt(totalCast),
                frac: fmt(100 * (totalCast / totalAll)),
            },
        }
    })

    function fmt(x: number) {
        return Math.round(x).toLocaleString()
    }
</script>

<section class="flex flex-col gap-2 pb-8">
    <!-- <h1>Damage</h1> -->

    <div class="grid-container">
        <div class="row">
            <span class="tdd">Total Damage</span>
            <span class="tdd">{dist.total.total}</span>
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
            <span class="tdd">{dist.physical.total}</span>
            <span class="tdd">{dist.physical.frac}%</span>
        </div>

        <div class="row">
            <span class="tdd">Magical Damage</span>
            <span class="tdd">{dist.magical.total}</span>
            <span class="tdd">{dist.magical.frac}%</span>
        </div>

        <div class="row">
            <span class="tdd">True Damage</span>
            <span class="tdd">{dist.true.total}</span>
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
            <span class="tdd">Auto Attacks</span>
            <span class="tdd">{dist.auto.total}</span>
            <span class="tdd">{dist.auto.frac}%</span>
        </div>

        <div class="row">
            <span class="tdd">Spells / Other</span>
            <span class="tdd">{dist.cast.total}</span>
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
