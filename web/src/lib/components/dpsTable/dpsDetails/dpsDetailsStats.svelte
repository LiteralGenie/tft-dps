<script lang="ts">
    import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { assetUrl } from '$lib/utils/networkUtils'

    const { details }: { details: SimDetails } = $props()

    const stats = $derived.by(() => {
        const s = details.initial_stats
        return [
            {
                value: Math.round(s.ad * s.ad_mult),
                label: 'Basic Attack Damage',
                icon: {
                    x: -864 - 24 * 24,
                    y: 0,
                },
            },
            {
                value: Math.round((s.ad_mult - 1) * 100),
                label: 'Attack Damage',
                icon: {
                    x: -864,
                    y: 0,
                },
            },
            {
                value: s.ap - 100,
                label: 'Ability Power',
                icon: {
                    x: -864 - 3 * 24,
                    y: 0,
                },
            },
            {
                value: (s.speed * s.speed_mult).toFixed(2),
                label: 'Attack Speed',
                icon: {
                    x: -864 - 6 * 24,
                    y: 0,
                },
            },
            {
                value: `${Math.round(100 * s.crit_rate)}%`,
                label: 'Crit Rate',
                icon: {
                    x: -864 - 8 * 24,
                    y: 0,
                },
            },
            {
                value: `${Math.round(100 * s.crit_mult)}%`,
                label: 'Crit Damage',
                icon: {
                    x: -864 - 9 * 24,
                    y: 0,
                },
            },
            {
                value: `${Math.round(100 * s.amp)}%`,
                label: 'Damage Amp',
                icon: {
                    x: -1976,
                    y: 0,
                },
            },
            {
                value: s.armor,
                label: 'Armor',
                icon: {
                    x: -864 - 5 * 24,
                    y: 0,
                },
            },
            {
                value: s.mr,
                label: 'Magic Resist',
                icon: {
                    x: -864 - 18 * 24,
                    y: 0,
                },
            },
            {
                value: s.health_max * s.health_mult,
                label: 'Health',
                icon: {
                    x: -864 - 11 * 24,
                    y: 0,
                },
            },
            {
                value: s.mana_max,
                label: 'Max Mana',
                icon: {
                    x: -864 - 15 * 24,
                    y: 0,
                },
            },
            {
                value: s.mana_regen,
                label: 'Mana Regen',
                icon: {
                    x: -864 - 16 * 24,
                    y: 0,
                },
            },
            { value: s.mana_per_auto, label: 'Mana Regen (attacks)', icon: null },
        ]
    })
</script>

<section>
    <h1 class="font-semibold">Stats</h1>

    <p class="text-foreground/80 pb-3 pt-1 text-xs">
        Stats at combat start, including bonuses from items, traits, etc.
    </p>

    <div class="grid-container">
        {#each stats as s}
            <div class="stat">
                <div class="label">
                    <span>{s.label}</span>
                </div>

                <div class="value">
                    <span>{s.value}</span>
                    {#if s.icon}
                        <img
                            src={assetUrl('/uiautoatlas/ux/fonts/css/stylesheet_tft9/atlas_0.png')}
                            style="object-position: {s.icon.x}px {s.icon.y}px;"
                        />
                    {/if}
                </div>
            </div>
        {/each}
    </div>
</section>

<style>
    .grid-container {
        display: grid;
        width: 100%;
        grid-template-columns: repeat(auto-fill, 11rem);
        gap: 0.5rem 1rem;
    }

    .stat {
        display: flex;
        flex-flow: column;
        /* gap: 0.125rem; */
        width: max-content;
    }

    .label {
        color: color-mix(in oklab, var(--color-foreground), transparent 15%);
    }

    .value {
        display: flex;
        gap: 0.25rem;
        align-items: center;
    }

    img {
        object-fit: none;
        height: 24px;
        width: 24px;
        transform: scale(0.75);
    }
</style>
