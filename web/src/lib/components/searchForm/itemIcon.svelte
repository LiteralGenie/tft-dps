<script lang="ts">
    import type { GameInfoValue } from '$lib/gameInfoContext.svelte'
    import { assetUrl } from '$lib/utils/networkUtils'

    let {
        itemInfo,
        className = '',
    }: { itemInfo: GameInfoValue['items'][string]; className?: string } = $props()
</script>

<div>
    <img class={className} src={assetUrl(itemInfo.icon)} title={itemInfo.name} draggable="false" />
</div>
