<script lang="ts">
    import type { Snippet } from 'svelte'

    const p = $props()
    const {
        onclick,
        icon,
        iconArg,
        label = '',
        labelClass = '',
    }: {
        onclick?: () => any
        icon?: Snippet<[any]>
        iconArg?: any
        label?: string
        labelClass?: string
    } = p
</script>

<button {onclick} class="mb-4 self-end rounded-md px-4 py-2 text-sm {p.class}">
    <span class="flex items-center gap-1 {labelClass}">
        {#if icon}
            {@render icon(iconArg)}
        {/if}
        {#if label}
            <span>{label}</span>
        {/if}
    </span>
</button>

<style>
    button {
        color: oklch(0.7 0 271.152 / 0.9);
        border: 1px solid oklch(0.7 0 271.152 / 0.9);
    }
    button:hover {
        color: oklch(0.7 0 271.152 / 1);
        border: 1px solid oklch(0.7 0 271.152 / 1);
    }
</style>
