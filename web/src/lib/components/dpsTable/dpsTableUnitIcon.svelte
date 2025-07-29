<script lang="ts">
    import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
    import StarIcon from '$lib/icons/starIcon.svelte'
    import { costToRarity } from '$lib/utils/miscUtils'
    import { assetUrl } from '$lib/utils/networkUtils'
    import { range } from 'radash'

    let { unit, stars }: { unit: GameInfoValue['units'][string]; stars: number } = $props()

    const rarity = $derived(costToRarity(unit.info.cost))
</script>

<div class="unit-bg relative {rarity} size-12 p-[2px]">
    <img src={assetUrl(unit.info.icon)} title={unit.info.name} />
    <div
        class="star-container pb-1.25 absolute bottom-0 left-0 right-0 top-0 flex h-full items-end px-1 pt-1"
    >
        {#each [...range(1, stars)]}
            <StarIcon class="stroke w-1/3 fill-amber-500 stroke-yellow-500" />
        {/each}
    </div>
</div>

<style>
    .star-container {
        background: linear-gradient(
            180deg,
            rgba(0, 0, 0, 0%) 0%,
            rgba(0, 0, 0, 10%) 45%,
            rgba(0, 0, 0, 25%) 55%,
            rgba(0, 0, 0, 60%) 65%,
            rgba(0, 0, 0, 75%) 100%
        );
    }
</style>
