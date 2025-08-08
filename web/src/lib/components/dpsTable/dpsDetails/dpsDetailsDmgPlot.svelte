<script lang="ts">
    import { getActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import * as Plot from '@observablehq/plot'
    import { sort } from 'radash'

    const { details }: { details: SimDetails } = $props()
    const activeSearch = getActiveSearchContext()

    let containerEl: HTMLDivElement

    const plot = $derived.by(() => {
        let points = [
            ...details.attacks.map((x) => ({ ...x, type: 'attack' })),
            ...details.casts.map((x) => ({ ...x, type: 'cast' })),
            ...details.misc_damage.map((x) => ({ ...x, type: 'misc' })),
        ]
        points = sort(points, (pt) => pt.t).filter(
            (pt) => pt.t <= activeSearch.value!.params.period,
        )

        const parsed = points.reduce(
            (acc, pt) => {
                const totalPhysical = pt.mult * pt.physical_damage
                const totalMagical = pt.mult * pt.magical_damage
                const totalTrue = pt.mult * pt.true_damage
                const total = totalPhysical + totalMagical + totalTrue
                if (total === 0) {
                    // return acc
                }

                const grandTotal = acc.grandTotal + total

                const pFrac = totalPhysical / (total - totalTrue)
                const fill = `color-mix(in oklab, orange ${pFrac * 100}%, blue)`

                acc.newPoints.push({ ...pt, grandTotal, total, fill })

                return {
                    grandTotal,
                    newPoints: acc.newPoints,
                }
            },
            {
                grandTotal: 0,
                newPoints: [] as Array<
                    (typeof points)[number] & { grandTotal: number; total: number; fill: string }
                >,
            },
        ).newPoints

        return Plot.plot({
            marks: [
                Plot.line(parsed, {
                    x: 't',
                    y: 'grandTotal',
                    stroke: 'color-mix(in oklab, var(--color-foreground), transparent 50%)',
                }),
                Plot.dot(parsed, {
                    x: 't',
                    y: 'grandTotal',
                    fill: 'fill',
                    r: 4,
                    symbol: (d: (typeof parsed)[number]) =>
                        d.type === 'attack' ? 'circle' : 'star',
                    stroke: (d: (typeof parsed)[number]) =>
                        `color-mix(in oklab, var(--color-foreground) 40%, ${d.fill})`,
                    strokeWidth: 1,
                }),
                Plot.ruleY([0]),
                Plot.ruleX([0]),
            ],
            labelArrow: false,
            symbol: { legend: true },
            grid: true,
        })
    })

    $effect(() => {
        containerEl.append(plot)
        return () => [...containerEl.children].forEach((el) => el.remove())
    })
</script>

<section>
    <h1 class="pb-1 font-semibold">Damage Graph</h1>

    <p class="text-foreground/80 pb-2 pt-1 text-xs">
        Dots indicate auto attacks. Stars indicate spell casts and other damage (eg DoTs, wraith
        damage).

        <br />

        Color indicates the damage type. Orange for physical, blue for magical.
    </p>

    <div bind:this={containerEl}></div>
</section>
