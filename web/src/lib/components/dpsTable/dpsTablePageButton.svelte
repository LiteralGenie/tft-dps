<script lang="ts">
    const { label, onclick, disabled }: { label: string; onclick: () => void; disabled: boolean } =
        $props()
</script>

<button
    {onclick}
    class="underline-offset-6 text-foreground/80 disabled:text-foreground/40 hover:text-foreground not-disabled:underline w-20 px-2 py-2 decoration-0 disabled:pointer-events-none"
    {disabled}
>
    {label}
</button>
