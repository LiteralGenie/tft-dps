<script lang="ts">
    import type { PackedId } from '$lib/activeSearchContext/activeSearchConstants'
    import { getSimDetailsContext } from '$lib/simDetailsContext/simDetailsContext.svelte'
    import { debounce, sum } from 'radash'

    const { id }: { id: PackedId } = $props()

    const ctx = getSimDetailsContext()

    const details = $derived(ctx.sims.get(id))
    const dist = $derived.by(() => {
        if (!details)
            return {
                unknown: 100,
                physical: 0,
                magical: 0,
                true: 0,
            }

        const allDamage = [...details.attacks, ...details.casts, ...details.misc_damage]

        const totalPhysical = sum(allDamage, (x) => x.physical_damage)
        const totalMagical = sum(allDamage, (x) => x.magical_damage)
        const totalTrue = sum(allDamage, (x) => x.true_damage)
        const totalAll = totalPhysical + totalMagical + totalTrue

        return {
            unknown: 0,
            physical: (100 * totalPhysical) / totalAll,
            magical: (100 * totalMagical) / totalAll,
            true: (100 * totalTrue) / totalAll,
        }
    })

    const doFetch = debounce({ delay: 100 }, (id: PackedId) => ctx.fetchId(id))
    $effect(() => {
        doFetch(id)
    })
</script>

<div
    class="flex h-min w-full items-center"
    title={`
${dist.physical.toFixed(0)}% physical
${dist.magical.toFixed(0)}% magical
${dist.true.toFixed(0)}% true
`.trim()}
>
    <span class="dmg-type unknown" style:width="{dist.unknown}%"></span>
    <span class="dmg-type physical" style:width="{dist.physical}%"></span>
    <span class="dmg-type magical" style:width="{dist.magical}%"></span>
    <span class="dmg-type true" style:width="{dist.true}%"></span>
</div>

<style>
    .dmg-type {
        height: 0.25rem;
        width: 33%;
    }
    .physical {
        background-color: rgb(255, 115, 0);
    }
    .magical {
        background-color: rgb(78, 104, 250);
    }
    .true {
        background-color: white;
    }
    .unknown {
        background-color: black;
    }
</style>
