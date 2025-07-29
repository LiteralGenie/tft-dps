<script lang="ts">
    const { label, onclick }: { label: string; onclick: () => void } = $props()
</script>

<button {onclick} class="underline-offset-6 w-20 px-2 py-2 text-gray-400 underline decoration-0">
    {label}
</button>
