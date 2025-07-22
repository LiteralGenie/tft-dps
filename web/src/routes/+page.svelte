<script>
    import tft_dps from '../assets/tft_dps-0.0.1-py2.py3-none-any.whl?url'

    async function main() {
        // @ts-ignore
        const pyodide = await loadPyodide()

        await pyodide.loadPackage('micropip')
        const micropip = pyodide.pyimport('micropip')

        // Strip leading slash to make url relative
        const packageUrl = tft_dps.slice(1)
        await micropip.install(packageUrl)

        console.log(
            pyodide.runPython(`
                from tft_dps import main
                main.main()
            `),
        )
    }

    main()
</script>
