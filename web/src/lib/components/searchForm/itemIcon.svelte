<script lang="ts">
    import type { GameInfoContext } from '$lib/gameInfoContext.svelte'
    import { assetUrl } from '$lib/miscUtils'

    let {
        itemInfo,
        className = '',
    }: { itemInfo: GameInfoContext['items'][string]; className?: string } = $props()
</script>

<div>
    <img class={className} src={assetUrl(itemInfo.icon)} title={itemInfo.name} />
</div>
