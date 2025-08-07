<script lang="ts">
    import { setActiveSearchContext } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { bootstrap } from '$lib/bootstrap'
    import DpsTable from '$lib/components/dpsTable/dpsTable.svelte'
    import { setGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { setSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { setSimDetailsContext } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { onMount } from 'svelte'

    let loadStatus = $state<string | null>('')

    const infoCtx = setGameInfoContext()

    setSearchContext(infoCtx)
    setActiveSearchContext(infoCtx)
    setSimDetailsContext()

    onMount(async () => {
        try {
            const statusGen = bootstrap()
            let tft
            while (true) {
                const x = await statusGen.next()
                if (x.done) {
                    tft = x.value
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
            infoCtx.set(tft.units, tft.items, tft.traits, tft.notes)

            loadStatus = null
        } catch (e) {
            loadStatus = `Error.\n${String(e)}`
        }
    })
</script>

<svelte:window onpopstate={() => window.location.reload()} />

{#if loadStatus !== null}
    <pre>{loadStatus}</pre>
{:else}
    <div class="min-h-full p-8">
        <DpsTable />
    </div>
{/if}
