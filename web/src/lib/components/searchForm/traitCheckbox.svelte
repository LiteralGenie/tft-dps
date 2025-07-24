<script lang="ts">
    import { getSearchContext } from '$lib/searchContext.svelte'

    const { key, label }: { key: 'silver' | 'gold' | 'prismatic'; label: string } = $props()

    const searchCtx = getSearchContext()

    let ref: HTMLInputElement

    function onClick(ev: MouseEvent) {
        if (ev.target !== ref) {
            ref.click()
            return
        }
    }

    function onChange() {
        searchCtx.traits[key] = ref.checked
    }
</script>

<div onclick={onClick} class="flex cursor-pointer items-center gap-2">
    <input bind:this={ref} onchange={onChange} type="checkbox" />
    <span>{label}</span>
</div>
