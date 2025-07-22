<script lang="ts">
    import tft_dps from '../assets/tft_dps-0.0.1-py2.py3-none-any.whl?url'

    class IdbCache {
        IDB_ID = 'tft_dps'
        IDB_TABLE = 'kv'

        async has(key: string): Promise<boolean> {
            const [_, store] = await this.connect()
            return new Promise((resolve, reject) => {
                const req = store.getKey(key)
                req.onsuccess = (ev: any) => resolve(ev.target.result !== undefined)
                req.onerror = () => reject()
            })
        }

        async get(key: string): Promise<string> {
            const [_, store] = await this.connect()
            return new Promise((resolve, reject) => {
                const req = store.get(key)
                req.onsuccess = (ev: any) => {
                    if (ev.target.result === undefined) {
                        console.error(ev)
                        reject()
                    } else {
                        resolve(ev.target.result)
                    }
                }
                req.onerror = () => reject()
            })
        }

        async set(key: string, value: string): Promise<void> {
            const [_, store] = await this.connect()
            return new Promise((resolve, reject) => {
                const req = store.put(value, key)
                req.onsuccess = () => resolve()
                req.onerror = () => reject()
            })
        }

        async init() {
            return new Promise((resolve, reject) => {
                const request = indexedDB.open(this.IDB_ID, 1)

                request.onupgradeneeded = (event) => {
                    // @ts-ignore
                    const db: IDBDatabase = event.target.result
                    db.createObjectStore(this.IDB_TABLE)
                }

                request.onsuccess = () => resolve(request.result)
                request.onerror = () => reject(request.error)
            })
        }

        private async connect(): Promise<[IDBTransaction, IDBObjectStore]> {
            const db: IDBDatabase = await new Promise((resolve, reject) => {
                const req = indexedDB.open(this.IDB_ID, 1)
                req.onsuccess = (ev: any) => resolve(ev.target.result)
                req.onerror = (ev: any) => reject()
                return req
            })

            const txn = db.transaction([this.IDB_TABLE], 'readwrite')
            const store = txn.objectStore(this.IDB_TABLE)
            return [txn, store]
        }
    }

    async function main() {
        const cache = new IdbCache()
        await cache.init()
        ;(window as any).tft_cache = cache

        // @ts-ignore
        const pyodide = await loadPyodide()

        await pyodide.loadPackage('micropip')
        const micropip = pyodide.pyimport('micropip')

        // Strip leading slash to make url relative
        const packageUrl = tft_dps.slice(1)
        await micropip.install(packageUrl)

        console.log(
            pyodide.runPython(`
                import asyncio
                from tft_dps import web
                asyncio.create_task(web.main())
            `),
        )
    }

    main()
</script>
