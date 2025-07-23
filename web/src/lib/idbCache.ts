export class IdbCache {
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

    async init(): Promise<this> {
        await new Promise((resolve, reject) => {
            const request = indexedDB.open(this.IDB_ID, 1)

            request.onupgradeneeded = (event) => {
                // @ts-ignore
                const db: IDBDatabase = event.target.result
                db.createObjectStore(this.IDB_TABLE)
            }

            request.onsuccess = () => resolve(request.result)
            request.onerror = () => reject(request.error)
        })

        return this
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
