from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal, getcontext
from typing import Any
from zoneinfo import available_timezones

# Note: Bool, Str, List, and Dict Haystack kinds are assumed to just be
# their Python type equivalents.  We may reevaluate this decision in the
# future.


# -----------------------------------------------------------------------------
# Custom exceptions raised within this module
# -----------------------------------------------------------------------------


@dataclass
class TimezoneMismatchError(Exception):
    help_msg: str


@dataclass
class TimezoneInfoIncorrectError(Exception):
    help_msg: str


# -----------------------------------------------------------------------------
# Project Haystack supported kinds
# -----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Grid:
    meta: dict[str, Any]
    cols: list[dict[str, Any]]
    rows: list[dict[str, Any]]

    @property
    def col_rename_map(self) -> dict[str, str]:
        rename_map: dict[str, str] = {}
        for col in self.cols:
            ori_col_name = col["name"]

            # refer cols named "ts" to "Timestamp"
            if ori_col_name == "ts":
                new_col_name = "Timestamp"

            # use Ref id for name of cols representing points
            elif "meta" in col.keys() and "id" in col["meta"].keys():
                new_col_name = col["meta"]["id"].val

            else:
                new_col_name = ori_col_name

            rename_map[ori_col_name] = new_col_name
        return rename_map

    @staticmethod
    def to_grid(rows: dict[str, Any] | list[dict[str, Any]]) -> Grid:
        if isinstance(rows, dict):
            rows = [rows]

        col_names: list[str] = []
        for row in rows:
            for col_name in row.keys():
                if col_name not in col_names:
                    col_names.append(col_name)

        cols = [{"name": name} for name in col_names]
        meta = {"ver": "3.0"}

        return Grid(meta=meta, cols=cols, rows=rows)

    def __str__(self):
        return "Haystack Grid"


@dataclass(frozen=True, slots=True)
class Number:
    val: int | float
    unit: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.val, int | float):  # type: ignore
            raise TypeError("Val should be of type int or float")

        if not isinstance(self.unit, str | None):
            raise TypeError("Unit should be of type str or None")

    def __str__(self):
        if self.unit is not None:
            return f"{self.val}{self.unit}"
        else:
            return f"{self.val}"


# Marker() is a singleton
class Marker:
    __instance = None

    def __new__(cls):
        if Marker.__instance is None:
            Marker.__instance = object.__new__(cls)
        return Marker.__instance

    def __str__(self):
        return "\u2713"


# Remove() is a singleton
class Remove:
    __instance = None

    def __new__(cls):
        if Remove.__instance is None:
            Remove.__instance = object.__new__(cls)
        return Remove.__instance

    def __str__(self):
        return "remove"


# NA() is a singleton
class NA:
    __instance = None

    def __new__(cls):
        if NA.__instance is None:
            NA.__instance = object.__new__(cls)
        return NA.__instance

    def __str__(self):
        return "NA"


@dataclass(frozen=True, slots=True)
class Ref:
    val: str
    dis: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.val, str):  # type: ignore
            raise TypeError("Val should be of type str")

        if not isinstance(self.dis, str | None):
            raise TypeError("Dis should be of type str or None")

    def __str__(self) -> str:
        if self.dis is not None:
            return self.dis
        else:
            return f"@{self.val}"


@dataclass(frozen=True, slots=True)
class Date:
    val: date

    def __post_init__(self) -> None:
        if not isinstance(self.val, date):  # type: ignore
            raise TypeError("Val should be of type date")

    def __str__(self):
        return self.val.isoformat()


@dataclass(frozen=True, slots=True)
class Time:
    val: time

    def __post_init__(self) -> None:
        if not isinstance(self.val, time):  # type: ignore
            raise TypeError("Val should be of type time")

    def __str__(self):
        return self.val.isoformat()


@dataclass(frozen=True, slots=True)
class DateTime:
    val: datetime
    tz: str  # city name from IANA database

    def __post_init__(self) -> None:
        if not isinstance(self.val, datetime):  # type: ignore
            raise TypeError("Val should be of type datetime")

        if not isinstance(self.tz, str):  # type: ignore
            raise TypeError("tz should be of type str")

        if not str(self.val.tzinfo) in available_timezones():
            raise TimezoneInfoIncorrectError(
                "The DateTime val attribute has tzinfo == "
                f"{self.val.tzinfo}.  This is not an IANA timezone "
                "which is required."
            )

        if self.tz not in str(self.val.tzinfo):
            raise TimezoneMismatchError(
                f"DateTime instance has tz attribute equal to {self.tz} and "
                f"val attribute with tzinfo equal to {str(self.val.tzinfo)}"
            )

    def __str__(self) -> str:
        if self.val.microsecond == 0:
            display = self.val.isoformat(timespec="seconds")
        else:
            display = self.val.isoformat(timespec="milliseconds")

        return f"{display} {self.tz}"


@dataclass(frozen=True, slots=True)
class Uri:
    val: str

    def __post_init__(self) -> None:
        if not isinstance(self.val, str):  # type: ignore
            raise TypeError("Val should be of type str")

    def __str__(self):
        return self.val


@dataclass(frozen=True, slots=True)
class Coord:
    lat: Decimal
    lng: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.lat, Decimal):  # type: ignore
            raise TypeError("Lat should be of type Decimal")

        if not isinstance(self.lng, Decimal):  # type: ignore
            raise TypeError("Lng should be of type Decimal")

    def __str__(self):
        getcontext().prec = 6
        return f"C({self.lat}, {self.lng})"


@dataclass(frozen=True, slots=True)
class XStr:
    type: str
    val: str

    def __post_init__(self) -> None:
        if not isinstance(self.type, str):  # type: ignore
            raise TypeError("Type should be of type str")

        if not isinstance(self.val, str):  # type: ignore
            raise TypeError("Val should be of type str")

    def __str__(self):
        return f"({self.type}, {self.val})"


@dataclass(frozen=True, slots=True)
class Symbol:
    val: str

    def __post_init__(self) -> None:
        if not isinstance(self.val, str):  # type: ignore
            raise TypeError("Val should be of type str")

    def __str__(self):
        return f"^{self.val}"
