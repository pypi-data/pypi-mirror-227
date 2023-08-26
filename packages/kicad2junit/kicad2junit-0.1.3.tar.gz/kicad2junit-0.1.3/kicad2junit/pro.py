from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class BoardDesignSettings(DataClassJsonMixin):
    rule_severities: dict[str, str]


@dataclass
class Board(DataClassJsonMixin):
    design_settings: BoardDesignSettings


@dataclass
class Erc(DataClassJsonMixin):
    rule_severities: dict[str, str]


@dataclass
class KicadProject(DataClassJsonMixin):
    board: Board
    erc: Erc
