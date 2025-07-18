"""
dps(T) = total_auto_dmg + total_spell_dmg

total_auto_dmg(T) = auto_count(T) * auto_dmg(T)

total_spell_dmg(T) = cast_count(T) * cast_dmg(T)

cast_count(T) = mana_regen(T) + auto_count(T) * auto_mana

auto_count(T) = [simulated]
"""

import json
from pathlib import Path

from lib.resolver import get_units
from lib.utils.misc_utils import log_http_requests

log_http_requests()


def main():
    units = get_units()
    Path("/tmp/units").write_text(json.dumps(units, indent=2))


main()
