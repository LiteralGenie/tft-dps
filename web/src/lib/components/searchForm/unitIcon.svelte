<script lang="ts">
    import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { costToRarity } from '$lib/utils/miscUtils'
    import { assetUrl } from '$lib/utils/networkUtils'

    let { unit, className = '' }: { unit: GameInfoValue['units'][string]; className?: string } =
        $props()

    const rarity = $derived(costToRarity(unit.info.cost))
</script>

<div class="unit unit-bg {rarity} p-[2px]">
    <img class={className} src={assetUrl(unit.info.icon)} title={unit.info.name} />
</div>

<style>
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
