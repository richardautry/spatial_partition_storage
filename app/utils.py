from sqlmodel import SQLModel, Session
from sqlmodel.orm.session import _TSelectParam
from typing import List, Optional, Type, Union


_OPERATOR_TYPES = ("eq", "ge", "le")


def get_stepped_value(val, step_size):
    return val - val % step_size


def get_stepped_values(min_val: int, max_val: int, step_size: int) -> List[int]:
    """
    Get step-sized values for the indicated range.

    Example:
    INPUT 3, 9, 2 -> OUTPUT [2, 4, 6, 8]

    :param min_val:
    :param max_val:
    :param step_size:
    :return:
    """
    range_min = min_val - min_val % step_size
    range_max = max_val - max_val % step_size
    if range_min == range_max:
        return [range_min]
    return list(range(range_min, range_max + 1, step_size))


def get_dimension_values(
        session: Session,
        model: Type[_TSelectParam],
        min_val: int,
        max_val: int,
        step_size: int) -> List[Optional[_TSelectParam]]:
    values = []
    for stepped_value in get_stepped_values(min_val, max_val, step_size):
        value = session.get(model, stepped_value)
        if not value:
            value = model(id=stepped_value)
        values.append(value)
    return values


class DimensionQuery:
    def __init__(self, Model: Type[SQLModel], LinkModel: Type[SQLModel], fidelity: int = 0):
        self.Model = Model
        self.LinkModel = LinkModel
        self.fidelity = fidelity

    def get_full_statement(self, eq_value, ge_value, le_value, statement):
        if all((val is None for val in [eq_value, ge_value, le_value])):
            return statement

        statement = statement.join(self.LinkModel).join(self.Model)

        value_map = {
            "eq": eq_value,
            "ge": ge_value,
            "le": le_value
        }

        for operator_type, value in value_map.items():
            statement = self.get_statement(value, statement, operator_type)

        return statement

    def get_statement(self, value: Union[int, None], statement, operator_type: str):
        if value is None:
            return statement

        if operator_type == "eq":
            return self.get_eq_statement(statement, value)
        elif operator_type == "ge":
            return self.get_ge_statement(statement, value)
        elif operator_type == "le":
            return self.get_le_statement(statement, value)
        else:
            raise Exception(f"Unknown statement 'operator_type': {operator_type}.\n"
                            f"Options are: {_OPERATOR_TYPES}")

    def get_eq_statement(self, statement, value):
        # TODO: Make this prettier by ensuring id exists before returning statement
        return statement.where(self.Model.id == get_stepped_value(value, self.fidelity))

    def get_ge_statement(self, statement, value):
        return statement.where(self.Model.id >= get_stepped_value(value, self.fidelity))

    def get_le_statement(self, statement, value):
        return statement.where(self.Model.id <= get_stepped_value(value, self.fidelity))
