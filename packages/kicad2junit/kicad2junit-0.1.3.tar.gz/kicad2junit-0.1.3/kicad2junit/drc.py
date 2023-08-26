from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class DrcCoordinate(DataClassJsonMixin):
    x: float
    y: float


@dataclass
class DrcAffectedItem(DataClassJsonMixin):
    uuid: str
    description: str
    pos: DrcCoordinate


@dataclass
class DrcViolation(DataClassJsonMixin):
    type: str
    description: str
    severity: str
    items: list[DrcAffectedItem]


@dataclass
class DrcReport(DataClassJsonMixin):
    source: str
    date: str
    kicad_version: str
    violations: list[DrcViolation]
    unconnected_items: list[DrcViolation]
    schematic_parity: list[DrcViolation]
    coordinate_units: str
