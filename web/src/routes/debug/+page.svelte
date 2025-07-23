<script lang="ts">
    import SearchForm from '$lib/components/searchForm/searchForm.svelte'
    import { bootstrap } from '$lib/ffi'
    import { setGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { setSearchContext } from '$lib/searchContext.svelte'
    import { onMount } from 'svelte'

    let isReady = $state(false)

    const infoCtx = setGameInfoContext()
    ;(window as any).infoCtx = infoCtx

    setSearchContext()

    onMount(async () => {
        const statusGen = bootstrap()
        let tft
        while (true) {
            const x = await statusGen.next()
            if (x.done) {
                tft = x.value
                break
            }
        }

        ;(window as any).tft = tft

        infoCtx.units = tft.units
        infoCtx.items = tft.items

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
