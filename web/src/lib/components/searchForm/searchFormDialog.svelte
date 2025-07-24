<script lang="ts">
    import { createEventDispatcher } from 'svelte'
    import SearchForm from './searchForm.svelte'

    let { open = false }: { open: boolean } = $props()

    $effect(() => {
        if (open) {
            ref.showModal()
        } else {
            ref.close()
        }
    })

    let ref: HTMLDialogElement

    const dispatch = createEventDispatcher()

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

<div onclick={() => onClose()}>
    <dialog
        bind:this={ref}
        onclick={onClick}
        class="bg-background text-foreground z-20 m-auto max-h-[50rem] max-w-[45rem] overflow-auto rounded-md border p-8"
    >
        <div class="flex flex-col items-center justify-center">
            <!-- <button
                onclick={() => onClose()}
                class="p-3! absolute right-4 top-4 size-12 cursor-pointer rounded-full hover:bg-white/40"
                type="button"
            >
                <XIcon class="size-full" />
            </button> -->

            <SearchForm />
        </div>
    </dialog>
</div>
