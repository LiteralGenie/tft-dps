import WHEEL_URL from '../assets/tft_dps-0.0.1-py2.py3-none-any.whl?url'
import { IdbCache } from './idbCache'

export async function* bootstrap() {
    yield { type: 'load_cache' }
    const cache = await new IdbCache().init()
    ;(window as any).tft_cache = cache

    yield { type: 'load_pyodide' }
    // @ts-ignore
    const pyodide = await loadPyodide()
    ;(window as any).pyodide = pyodide

    await pyodide.loadPackage('micropip')
    const micropip = pyodide.pyimport('micropip')

    yield { type: 'load_deps' }
    // Strip leading slash to make url relative
    const packageUrl = WHEEL_URL.slice(1)
    await micropip.install(packageUrl)

    yield { type: 'load_game_info' }
    let units = await pyodide.runPythonAsync(`
        import json
        from js import tft_cache
        from tft_dps.web import get_all_units

        json.dumps(await get_all_units(tft_cache))
    `)
    units = JSON.parse(units)

    yield { type: 'load_runner' }
    const runner = await pyodide.runPythonAsync(`
        from js import tft_cache
        from tft_dps.lib.simulator.sim_runner import SimRunner

        runner = await SimRunner.ainit(tft_cache)
        runner
    `)
    ;(window as any).runner = runner

    let items = await pyodide.runPython(`
        import json
        from tft_dps.lib.constants import ITEMS
        json.dumps({ k: v for k,v in runner.items.items() if k in ITEMS })
    `)
    items = JSON.parse(items)

    return {
        cache,
        items,
        micropip,
        pyodide,
        runner,
        units,
    }
}
