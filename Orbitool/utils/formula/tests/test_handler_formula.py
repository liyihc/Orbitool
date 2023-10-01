import io
import h5py
from pydantic import BaseModel, ValidationError
import pytest
from numpy import testing as nptest

from ..h5handlers import *
from ..formula_list import *
from ....structures import HDF5, field

formula_list = [Formula('C7H8O2'), Formula('C3H3Ti-'), Formula('CC[13]H[2]')]


class FormulaItem(BaseRowItem):
    item_name = "test_formula_item"

    formula: Formula


def test_pydantic_validate():
    class Formulas(BaseModel):
        formula: FormulaType
    Formulas(formula="CH4")

    with pytest.raises(ValidationError):
        Formulas(formula=123)


def test_formula():
    f = HDF5.H5File()

    row = Row((FormulaItem,))
    row.write_to_h5(f._obj, "table", [FormulaItem(
        formula=formula) for formula in formula_list])

    formulas = row.read_from_h5(f._obj, "table")
    for f1, f2 in zip(formulas, formula_list):
        assert f1.formula == f2


class FormulasItem(BaseRowItem):
    item_name = "test formulas item"
    formulas: FormulaList = field(list)


def test_formulas():
    f = HDF5.H5File()

    row = Row((FormulasItem,))
    row.write_to_h5(f._obj, "table", [FormulasItem(
        formulas=formula_list)] * 10)

    formulas_table = row.read_from_h5(f._obj, "table")
    for formulas in formulas_table:
        assert formulas.formulas == formula_list
