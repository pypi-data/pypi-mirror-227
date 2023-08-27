from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class BoardDesignSettings(DataClassJsonMixin):
    rule_severities: dict[str, str]
    drc_exclusions: list[str]

    def get_drc_exclusions(self) -> list[str]:
        uuids = []
        for exclusion in self.drc_exclusions:
            uuid = get_excluded_uuid(exclusion)
            if uuid is not None:
                uuids.append(uuid)
        return uuids


@dataclass
class Board(DataClassJsonMixin):
    design_settings: BoardDesignSettings


@dataclass
class Erc(DataClassJsonMixin):
    rule_severities: dict[str, str]
    erc_exclusions: list[str]

    def get_erc_exclusions(self) -> list[str]:
        uuids = []
        for exclusion in self.erc_exclusions:
            uuid = get_excluded_uuid(exclusion)
            if uuid is not None:
                uuids.append(uuid)
        return uuids


@dataclass
class KicadProject(DataClassJsonMixin):
    board: Board
    erc: Erc


def get_excluded_uuid(excluded: str) -> str | None:
    s = excluded.split("|")
    if len(s) >= 4:
        return s[3]
    return None
