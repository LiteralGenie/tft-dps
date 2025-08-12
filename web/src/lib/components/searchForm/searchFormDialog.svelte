<script lang="ts">
    import { ComboIter } from '$lib/activeSearchContext/activeSearchContext.svelte'
    import { getGameInfoContext } from '$lib/gameInfoContext.svelte'
    import { getSearchContext } from '$lib/searchContext/searchContext.svelte'
    import { createEventDispatcher } from 'svelte'
    import SearchForm from './searchForm.svelte'

    let { open = false }: { open: boolean } = $props()

    const search = getSearchContext()
    const gameInfo = getGameInfoContext()

    $effect(() => {
        if (open) {
            ref.showModal()
        } else {
            ref.close()
        }
    })

    let ref: HTMLDialogElement

    const dispatch = createEventDispatcher()

    const estimate = $derived.by(() => {
        const iter = new ComboIter(search.value, gameInfo.value)
        return iter.total
    })

    function onClose() {
        dispatch('close')
    }

    function onClick(ev: MouseEvent) {
        ev.stopPropagation()

        if (ev.target === ref) {
            onClose()
        }
    }
</script>

<div onclick={onClose}>
    <dialog
        bind:this={ref}
        onclick={onClick}
        onclose={onClose}
        class="bg-background text-foreground z-20 m-auto h-full max-h-[50rem] max-w-[45rem] overflow-auto rounded-md border"
    >
        {#if estimate > 300_000}
            <p class="sticky top-0 z-10 bg-red-900 p-4">
                Current filters match ~{estimate.toLocaleString()} simulations. <br /> This may take
                a while and make the page unresponsive!
            </p>
        {/if}

        <div class="">
            <div class="flex flex-col items-center justify-center p-8">
                <!-- <button
                onclick={() => onClose()}
                class="p-3! absolute right-4 top-4 size-12 cursor-pointer rounded-full hover:bg-white/40"
                type="button"
            >
                <XIcon class="size-full" />
            </button> -->

                <SearchForm />
            </div>
        </div>
    </dialog>
</div>
