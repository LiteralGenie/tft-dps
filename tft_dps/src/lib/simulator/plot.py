from lib.simulator.sim_state import SimAttack, SimCast, SimState


def calc_total_damage(s: SimState) -> list[dict]:
    pts = []

    instances: list[SimAttack | SimCast] = [*s.attacks, *s.casts]
    instances.sort(key=lambda pt: pt.t)

    total_physical = 0
    total_magical = 0
    for x in instances:
        total_physical += x.physical_damage
        total_magical += x.magical_damage

        pt = dict(
            t=x.t,
            physical=total_physical,
            magical=total_magical,
        )

        if pts and pt["t"] == pts[-1]["t"]:
            pts[-1] = pt
        else:
            pts.append(pt)

    return pts
