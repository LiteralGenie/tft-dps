<script lang="ts">
    import { setActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { bootstrap } from '$lib/bootstrap'
    import DpsTable from '$lib/components/dpsTable/dpsTable.svelte'
    import { setGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { setSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'

    let loadStatus = $state<string | null>('')

    const infoCtx = setGameInfoContext()
    ;(window as any).infoCtx = infoCtx

    setSearchContext()
    setActiveSearchContext(infoCtx)

    onMount(async () => {
        try {
            const statusGen = bootstrap()
            let tft
            while (true) {
                const x = await statusGen.next()
                if (x.done) {
                    tft = x.value
                    infoCtx.units = tft.units
                    break
                } else {
                    switch (x.value.type) {
                        case 'load_cache':
                            loadStatus = 'Initializing database ...'
                            break
                        case 'load_game_info':
                            loadStatus = 'Loading TFT data ...'
                            break
                        default:
                            loadStatus = '???'
                            break
                    }
                }
            }

            ;(window as any).tft = tft

            infoCtx.units = tft.units
            infoCtx.items = tft.items
            infoCtx.traits = tft.traits

            loadStatus = null
        } catch (e) {
            loadStatus = `Error.\n${String(e)}`
        }
    })
</script>

{#if loadStatus !== null}
    <pre>{loadStatus}</pre>
{:else}
    <div class="p-8">
        <DpsTable />
    </div>
{/if}
