<script lang="ts">
    import DpsTable from '$lib/components/dpsTable/dpsTable.svelte'
    import { bootstrap } from '$lib/ffi'
    import { setGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { setSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'

    let runner: any | null = $state(null)
    let loadStatus = $state('')

    const infoCtx = setGameInfoContext()
    ;(window as any).infoCtx = infoCtx

    setSearchContext()

    onMount(async () => {
        try {
            const statusGen = bootstrap()
            let tft
            while (true) {
                const x = await statusGen.next()
                if (x.done) {
                    tft = x.value
                    runner = tft.runner
                    infoCtx.units = tft.units
                    break
                } else {
                    switch (x.value.type) {
                        case 'load_cache':
                            loadStatus = 'Initializing database ...'
                            break
                        case 'load_pyodide':
                            loadStatus = 'Initializing Python ...'
                            break
                        case 'load_deps':
                            loadStatus = 'Installing dependencies ...'
                            break
                        case 'load_game_info':
                            loadStatus = 'Loading TFT data ...'
                            break
                        case 'load_runner':
                            loadStatus = 'Initializing simulator ...'
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
        } catch (e) {
            loadStatus = `Error.\n${String(e)}`
        }
    })
</script>

{#if !runner}
    <pre>{loadStatus}</pre>
{:else}
    <div class="p-8">
        <DpsTable />
    </div>
{/if}
