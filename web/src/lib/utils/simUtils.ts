import type { SimDetails } from '$lib/simDetailsContext/simDetailsContext.svelte'
import { sum } from 'radash'

export function summarizeDamage(details: SimDetails, period: number) {
    const allDamage = [...details.attacks, ...details.casts, ...details.misc_damage].filter(
        (x) => x.t <= period,
    )

    const totalPhysical = sum(allDamage, (x) => x.mult * x.physical_damage)
    const totalMagical = sum(allDamage, (x) => x.mult * x.magical_damage)
    const totalTrue = sum(allDamage, (x) => x.mult * x.true_damage)

    const totalAll = totalPhysical + totalMagical + totalTrue

    const totalAuto = sum(
        details.attacks
            .filter((x) => x.t <= period)
            .flatMap((x) => [
                x.mult * x.physical_damage,
                x.mult * x.magical_damage,
                x.mult * x.true_damage,
            ]),
    )
    const totalCast = sum(
        [...details.casts, ...details.misc_damage]
            .filter((x) => x.t <= period)
            .flatMap((x) => [
                x.mult * x.physical_damage,
                x.mult * x.magical_damage,
                x.mult * x.true_damage,
            ]),
    )

    return {
        total: { total: totalAll, totalString: fmt(totalAll), frac: 100 },
        physical: {
            total: totalPhysical,
            totalString: fmt(totalPhysical),
            frac: fmt(100 * (totalPhysical / totalAll)),
        },
        magical: {
            total: totalMagical,
            totalString: fmt(totalMagical),
            frac: fmt(100 * (totalMagical / totalAll)),
        },
        true: {
            total: totalTrue,
            totalString: fmt(totalTrue),
            frac: fmt(100 * (totalTrue / totalAll)),
        },
        auto: {
            total: totalAuto,
            totalString: fmt(totalAuto),
            frac: fmt(100 * (totalAuto / totalAll)),
            count: details.attacks.length,
        },
        cast: {
            total: totalCast,
            totalString: fmt(totalCast),
            frac: fmt(100 * (totalCast / totalAll)),
            count: details.casts.length,
        },
    }
}

export function fmt(x: number) {
    return Math.round(x).toLocaleString()
}
