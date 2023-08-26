from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class ErcCoordinate(DataClassJsonMixin):
    x: float
    y: float


@dataclass
class ErcAffectedItem(DataClassJsonMixin):
    uuid: str
    description: str
    pos: ErcCoordinate


@dataclass
class ErcViolation(DataClassJsonMixin):
    type: str
    description: str
    severity: str
    items: list[ErcAffectedItem]


@dataclass
class ErcSheet(DataClassJsonMixin):
    uuid_path: str
    path: str
    violations: list[ErcViolation]


@dataclass
class ErcReport(DataClassJsonMixin):
    source: str
    date: str
    kicad_version: str
    sheets: list[ErcSheet]
    coordinate_units: str
