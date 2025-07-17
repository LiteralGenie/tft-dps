"""
dps(T) = total_auto_dmg + total_spell_dmg

total_auto_dmg(T) = auto_count(T) * auto_dmg(T)

total_spell_dmg(T) = cast_count(T) * cast_dmg(T)

cast_count(T) = mana_regen(T) + auto_count(T) * auto_mana

auto_count(T) = [simulated]
"""

from calc_ctx import CalcCtx


def main():
    ctx = CalcCtx(
        T=10,
        stats=dict(),
        items=dict(),
    )

    calc_dps(ctx)


def calc_dps(ctx: CalcCtx):
    pass


def calc_total_auto_damage(ctx: CalcCtx):
    pass


main()
