from tft_dps.lib.simulator.sim_state import SimDamage


def total_sim_damage(d: SimDamage):
    return sum(
        [
            d["mult"] * d["physical_damage"],
            d["mult"] * d["magical_damage"],
            d["mult"] * d["true_damage"],
        ]
    )
