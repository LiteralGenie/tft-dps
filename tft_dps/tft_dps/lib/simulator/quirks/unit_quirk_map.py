from abc import ABCMeta

from . import five, four, one, three, two
from .quirks import UnitQuirks

UNIT_QUIRK_MAP: dict[str, type[UnitQuirks]] = {
    cls.id: cls
    for mod in [one, two, three, four, five]
    for cls in mod.__dict__.values()
    if type(cls) == ABCMeta and issubclass(cls, UnitQuirks) and cls is not UnitQuirks
}
