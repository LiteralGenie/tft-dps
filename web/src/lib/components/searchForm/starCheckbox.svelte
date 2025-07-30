<script lang="ts">
    import { getSearchContext } from '$lib/searchContext.svelte'

    const { key, label }: { key: 1 | 2 | 3; label: string } = $props()

    const { value: searchCtx } = getSearchContext()

    let ref: HTMLInputElement

    function onClick(ev: MouseEvent) {
        if (ev.target !== ref) {
            ref.click()
            return
        }
    }

    function onChange() {
        searchCtx.stars[key] = ref.checked
    }
</script>

<div onclick={onClick} class="flex cursor-pointer items-center gap-2">
    <input bind:this={ref} onchange={onChange} type="checkbox" checked={searchCtx.stars[key]} />
    <span>{label}</span>
</div>
