from typing import List

from ...utils.formula import Formula
from ...structures.spectrum import MassListItem
from ..binary_search import indexNearest, indexFirstBiggerThan


def get_position(l: List[MassListItem], index: int):
    return l[index].position


def addMassTo(original_list: List[MassListItem], new_item: MassListItem, rtol: float):
    if len(new_item.formulas) == 1:
        new_item.position = new_item.formulas[0].mass()
    if len(original_list) == 0:
        original_list.append(new_item)
        return
    insert_index = indexFirstBiggerThan(
        original_list, new_item.position, method=get_position)
    index = indexNearest(
        original_list, new_item.position, method=get_position)

    item = original_list[index]

    if abs(item.position / new_item.position - 1) > rtol:
        original_list.insert(insert_index, new_item)
        return

    if set(item.formulas) == set(new_item.formulas):
        return

    if len(new_item.formulas) == 0:
        return

    if len(item.formulas) == 0:
        original_list[index] = new_item
        return

    original_list.insert(insert_index, new_item)


def MergeInto(original_list: List[MassListItem], new_list: List[MassListItem], rtol: float):
    for item in new_list:
        addMassTo(original_list, item, rtol)


def fitUseMassList(position: float, masslist: List[MassListItem], rtol: float) -> List[Formula]:
    if len(masslist) == 0:
        return []
    index = indexNearest(masslist, position, method=get_position)
    item = masslist[index]
    if abs(item.position / position - 1) < rtol:
        return item.formulas
    return []