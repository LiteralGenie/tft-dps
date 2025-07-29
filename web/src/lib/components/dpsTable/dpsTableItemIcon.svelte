<script lang="ts">
    import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { assetUrl } from '$lib/utils/networkUtils'

    let { item }: { item: GameInfoValue['items'][string] | null } = $props()
</script>

<div class="size-8 border border-gray-800">
    {#if item}
        <img src={assetUrl(item.icon)} title={item.name} />
    {:else}
        <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 16 16"
            stroke-width="0.5"
            class="size-full stroke-gray-800"
        >
            <path stroke-linecap="round" stroke-linejoin="round" d="M0 0 L16 16 M16 0 L0 16"></path>
        </svg>
    {/if}
</div>
