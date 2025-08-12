<script lang="ts">
    import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { sort } from 'radash'

    const { details }: { details: SimDetails } = $props()

    const events = $derived.by(() => {
        let evs = [
            ...details.attacks.map((ev) => ({ ...ev, type: 'Basic Attack' })),
            ...details.casts.map((ev) => ({ ...ev, type: 'Spell Cast' })),
            ...details.misc_damage.map((ev) => ({ ...ev, type: 'Misc' })),
        ].map((ev) => ({
            ...ev,
            withMult: {
                physical: ev.physical_damage * ev.mult,
                magical: ev.magical_damage * ev.mult,
                true: ev.true_damage * ev.mult,
            },
        }))
        evs = sort(evs, (ev) => ev.t)
        return evs
    })

    function round(x: number) {
        return Math.round(x).toLocaleString()
    }
</script>

<section class="flex flex-col">
    <h1 class="pb-2 font-semibold">Combat Log</h1>

    <div class="grid-container max-h-[50vh] overflow-auto">
        <div class="row contents">
            <span class="thh text-end"> Time </span>
            <span class="thh"> Attack Type </span>
            <span class="thh"> Phys. </span>
            <span class="thh"> Magic </span>
            <span class="thh"> True </span>
        </div>

        {#each events as ev}
            <div class="row contents">
                <span class="tdd text-end">{ev.t.toFixed(2)}s</span>
                <span class="tdd">
                    {ev.type}
                </span>
                <span
                    class={{
                        'tdd text-end': true,
                        'text-orange-300': true,
                        'text-orange-300/60': ev.withMult.physical === 0,
                    }}
                >
                    {round(ev.withMult.physical)}
                </span>
                <span
                    class={{
                        'tdd text-end': true,
                        'text-blue-300': true,
                        'text-blue-300/60': ev.withMult.magical === 0,
                    }}
                >
                    {round(ev.withMult.magical)}
                </span>
                <span
                    class={{
                        'tdd text-end': true,
                        'text-foreground/60': ev.withMult.true === 0,
                    }}
                >
                    {round(ev.withMult.true)}
                </span>
            </div>
        {/each}
    </div>
</section>

<style>
    .grid-container {
        display: grid;
        grid-template-columns: max-content max-content max-content max-content max-content;
        align-items: center;

        border: 1px solid color-mix(in oklab, var(--color-foreground), transparent 20%);
        width: max-content;
    }

    .tdd {
        padding: 0.375em 0.75em;
        width: 100%;
    }
    .tdd:first-child {
        padding-left: 2em;
    }
    .tdd:last-child {
        padding-right: 2em;
    }

    .thh {
        padding: 0.5em 0.75em;
    }
    .thh:first-child {
        padding-left: 2em;
    }
    .thh:last-child {
        padding-right: 2em;
    }

    .tdd {
        border-top-width: 1px;
        border-style: solid;
        border-color: color-mix(in oklab, var(--color-foreground), transparent 50%);
    }

    .row:nth-child(2n) > * {
        background-color: color-mix(in oklab, var(--color-foreground), transparent 95%);
    }
    .row:hover > * {
        background-color: color-mix(in oklab, var(--color-foreground), transparent 90%);
    }
</style>
