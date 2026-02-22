"""Schemas for R³/H³/C³ feature metadata."""

from pydantic import BaseModel


class R3GroupInfo(BaseModel):
    key: str
    name: str
    start: int
    end: int
    color: str
    feature_names: list[str]


class R3Metadata(BaseModel):
    n_features: int
    groups: list[R3GroupInfo]
    feature_names: list[str]
