from sqlmodel import SQLModel, Session
from sqlmodel.orm.session import _TSelectParam
from typing import List, Optional, Type


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
