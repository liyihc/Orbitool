from typing import List, NamedTuple, Optional

from Orbitool.base import BaseRowStructure
from ..formula import Formula, FormulaList, FormulaType
from Orbitool.utils.binary_search import indexNearest, indexFirstBiggerThan


class MassListItem(BaseRowStructure):
    position: float
    formulas: FormulaList = []


class CompareRow(NamedTuple):
    """One aligned row of a Mass List comparison.

    `merge` is always present (it is the union row the other two align to);
    `current` / `imported` are present only when that list contributed.
    """

    current: Optional[MassListItem]
    imported: Optional[MassListItem]
    merge: MassListItem


class MassListHelper:
    @classmethod
    def get_position(cls, l: List[MassListItem], index: int):
        return l[index].position

    @classmethod
    def addMassTo(cls, original_list: List[MassListItem], new_item: MassListItem, rtol: float):
        cls._addMassTo(original_list, new_item, rtol)

    @classmethod
    def _addMassTo(cls, original_list: List[MassListItem], new_item: MassListItem, rtol: float):
        """Apply the merge rule in place, reporting what it did.

        Returns `(index, action)` where action is `"insert"`, `"match"` or
        `"replace"` and `index` is the affected row. `addMassTo` is the public
        face of this rule and discards the report; `compare` uses it to align
        the union with its two sources.
        """
        if len(new_item.formulas) == 1:
            new_item.position = new_item.formulas[0].mass()
        if len(original_list) == 0:
            original_list.append(new_item)
            return 0, "insert"
        insert_index = indexFirstBiggerThan(
            original_list, new_item.position, method=cls.get_position)
        index = indexNearest(
            original_list, new_item.position, method=cls.get_position)

        item = original_list[index]

        if abs(item.position / new_item.position - 1) > rtol:
            original_list.insert(insert_index, new_item)
            return insert_index, "insert"

        if set(item.formulas) == set(new_item.formulas):
            return index, "match"

        if len(new_item.formulas) == 0:
            return index, "match"

        if len(item.formulas) == 0:
            original_list[index] = new_item
            return index, "replace"

        original_list.insert(insert_index, new_item)
        return insert_index, "insert"

    @classmethod
    def mergeInto(cls, original_list: List[MassListItem], new_list: List[MassListItem], rtol: float):
        for item in new_list:
            cls.addMassTo(original_list, item, rtol)

    @classmethod
    def compare(cls, current: List[MassListItem], imported: List[MassListItem],
                rtol: float) -> List[CompareRow]:
        """Align `current` against `imported` row by row.

        The Merge column is exactly the union `mergeInto` would produce; the
        current and import sides are filled only where they contributed, so a
        row with both sides is a match and a one-sided row is unique to that
        list. Built on the same rule as the merge, never a separate diff.
        """
        merge_list = list(current)
        current_index: List[Optional[int]] = list(range(len(merge_list)))
        imported_item: List[Optional[MassListItem]] = [None] * len(merge_list)

        for item in imported:
            new_item = MassListItem(
                position=item.position, formulas=list(item.formulas))
            index, action = cls._addMassTo(merge_list, new_item, rtol)
            if action == "insert":
                current_index.insert(index, None)
                imported_item.insert(index, new_item)
            else:
                imported_item[index] = new_item

        return [
            CompareRow(
                current=current[current_index[i]]
                if current_index[i] is not None else None,
                imported=imported_item[i],
                merge=merge_list[i],
            )
            for i in range(len(merge_list))
        ]

    @classmethod
    def fitUseMassList(cls, position: float, masslist: List[MassListItem], rtol: float) -> List[Formula]:
        if len(masslist) == 0:
            return []
        index = indexNearest(masslist, position, method=cls.get_position)
        item = masslist[index]
        if abs(item.position / position - 1) < rtol:
            return item.formulas
        return []
