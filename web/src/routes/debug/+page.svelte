<script lang="ts">
    import SearchForm from '$lib/components/searchForm/searchForm.svelte'
    import { setGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { IdbCache } from '$lib/idbCache'
    import { setSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'
    import tft_dps from '../../assets/tft_dps-0.0.1-py2.py3-none-any.whl?url'

    let isReady = $state(false)

    const infoCtx = setGameInfoContext()
    ;(window as any).infoCtx = infoCtx

    setSearchContext()

    onMount(async () => {
        const cache = await new IdbCache().init()
        ;(window as any).tft_cache = cache

        // @ts-ignore
        const pyodide = await loadPyodide()
        ;(window as any).pyodide = pyodide

        await pyodide.loadPackage('micropip')
        const micropip = pyodide.pyimport('micropip')

        // Strip leading slash to make url relative
        const packageUrl = tft_dps.slice(1)
        await micropip.install(packageUrl)

        let units = await pyodide.runPythonAsync(`
                import json
                from js import tft_cache
                from tft_dps.web import get_all_units

                units = await get_all_units(tft_cache)
                json.dumps(units)
            `)
        infoCtx.units = JSON.parse(units)

        const runner = await pyodide.runPythonAsync(`
                from js import tft_cache
                from tft_dps.lib.simulator.sim_runner import SimRunner

                runner = await SimRunner.ainit(tft_cache)
                runner
            `)
        ;(window as any).runner = runner

        const result = await runner.run('Characters/TFT15_Gnar')
        ;(window as any).result = JSON.parse(result.as_json())

        isReady = true
    })
</script>

{#if isReady}
    <div class="p-16">
        <div class="rounded-md border p-8">
            <SearchForm />
        </div>
    </div>
{/if}
