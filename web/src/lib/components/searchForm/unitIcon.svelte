<script lang="ts">
    import type { GameInfoContext } from '$lib/gameInfoContext.svelte'
    import { assetUrl } from '$lib/utils/networkUtils'

    let {
        unitInfo,
        className = '',
    }: { unitInfo: GameInfoContext['units'][string]; className?: string } = $props()

    const c = $derived(unitInfo.info.cost)
    const rarity = $derived(
        c === 5
            ? 'legendary'
            : c === 4
              ? 'epic'
              : c === 3
                ? 'rare'
                : c === 2
                  ? 'uncommon'
                  : 'common',
    )
</script>

<div class="unit {rarity} p-[2px]">
    <img class={className} src={assetUrl(unitInfo.info.icon)} title={unitInfo.info.name} />
</div>

<style>
    :global(.unit.common) {
        background: linear-gradient(
            90deg,
            oklch(59.987% 0.00007 271.152),
            oklch(99.987% 0.00007 271.152),
            oklch(59.987% 0.00007 271.152)
        );
    }
    :global(.unit.uncommon) {
        background: linear-gradient(
            90deg,
            oklch(68.998% 0.19237 146.106),
            oklch(28.998% 0.19237 146.106),
            oklch(68.998% 0.19237 146.106)
        );
    }
    :global(.unit.rare) {
        background: linear-gradient(
            90deg,
            oklch(63.16% 0.13921 239.251),
            oklch(23.16% 0.13921 239.251),
            oklch(63.16% 0.13921 239.251)
        );
    }
    :global(.unit.epic) {
        background: linear-gradient(
            90deg,
            oklab(59.388% 0.22203 -0.15626),
            oklab(19.388% 0.22203 -0.15626),
            oklab(59.388% 0.22203 -0.15626)
        );
    }
    :global(.unit.legendary) {
        background: linear-gradient(
            90deg,
            oklab(86.31% 0.02689 0.10655),
            oklab(46.31% 0.02689 0.10655),
            oklab(86.31% 0.02689 0.10655)
        );
    }

    .unit:hover {
        animation: gradient-animation 3s linear infinite;
        background-size: 200%;
    }

    @keyframes gradient-animation {
        0% {
            background-position: 0% 0%;
        }
        50% {
            background-position: 100% 100%;
        }
        100% {
            background-position: 200% 200%;
        }
    }
</style>
