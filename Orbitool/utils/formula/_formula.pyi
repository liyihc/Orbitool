# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Union

import numpy as np


class Formula:
    def __init__(self, formula: Union[str, dict]
                 = None, *, charge=..., **kwargs): ...

    @property
    def charge(self) -> int: ...
    @charge.setter
    def charge(self, value: int): ...
    @property
    def isIsotope(self) -> bool: ...
    def mass(self) -> float: ...
    def findOrigin(self) -> Formula: ...
    def addElement(self, element: str, m: int = 0, num: int = 1): ...
    def toStr(self, showProton: bool = False,
              withCharge: bool = True) -> str: ...

    def relativeAbundance(self): ...
    def clear(self): ...
    def to_numpy(self) -> np.ndarray: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_numpy(cls, data: np.ndarray): ...
    def __setitem__(self, key: str, value: int): ...
    def __getitem__(self, key: str) -> int: ...
    def __str__(self): ...
    def __repr__(self): ...
    def __copy__(self): ...
    def __iadd__(self, formula: Formula): ...
    def __add__(self, formula: Formula) -> Formula: ...
    def __isub__(self, formula: Formula): ...
    def __sub__(self, formula: Formula) -> Formula: ...
    def __imul__(self, times): ...
    def __mul__(self, times) -> Formula: ...
    def __eq__(self, formula: Formula): ...
    def __contains__(self, formula: Formula): ...
    def __hash__(self): ...
