<script lang="ts">
    import DpsTable from '$lib/components/dpsTable/dpsTable.svelte'
    import { IdbCache } from '$lib/idbCache'
    import { onMount } from 'svelte'
    import tft_dps from '../assets/tft_dps-0.0.1-py2.py3-none-any.whl?url'

    let runner: any | null = $state(null)
    let loadStatus = $state('')

    onMount(async () => {
        try {
            loadStatus = 'Initializing database ...'
            const cache = new IdbCache()
            await cache.init()
            ;(window as any).tft_cache = cache

            loadStatus = 'Initializing Python ...'
            // @ts-ignore
            const pyodide = await loadPyodide()
            ;(window as any).pyodide = pyodide

            await pyodide.loadPackage('micropip')
            const micropip = pyodide.pyimport('micropip')

            loadStatus = 'Installing dependencies ...'
            // Strip leading slash to make url relative
            const packageUrl = tft_dps.slice(1)
            await micropip.install(packageUrl)

            loadStatus = 'Initializing simulator ...'
            runner = await pyodide.runPythonAsync(`
                from js import tft_cache
                from tft_dps.api import SimulationRunner

                runner = await SimulationRunner.ainit(tft_cache)
                runner
            `)
            ;(window as any).runner = runner

            const result = await runner.run('Characters/TFT15_Gnar')
            ;(window as any).result = JSON.parse(result.as_json())
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
