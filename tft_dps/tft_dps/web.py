from tft_dps.api import SimulationRunner
from tft_dps.lib.simulator.plot import calc_total_damage


async def main():
    from js import tft_cache  # type: ignore

    runner = await SimulationRunner.ainit(tft_cache)

    result = await runner.run("Characters/TFT15_Garen")

    total = calc_total_damage(result)
    for pt in total:
        print(f"{pt['t']},{pt['physical']},{pt['magical']}")
