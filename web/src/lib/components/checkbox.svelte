<script lang="ts">
    let { label = '', checked = $bindable(false) }: { label: string; checked: boolean } = $props()

    let ref: HTMLInputElement

    function onClick(ev: MouseEvent) {
        if (ev.target !== ref) {
            ref.click()
            return
        }
    }

    function onChange() {
        checked = ref.checked
    }
</script>

<div onclick={onClick} class="flex cursor-pointer items-center gap-2">
    <input bind:this={ref} onchange={onChange} type="checkbox" {checked} />
    <span>{label}</span>
</div>
