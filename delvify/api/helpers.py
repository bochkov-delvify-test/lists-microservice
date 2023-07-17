from typing import Callable, Optional, TypeVar

from fastapi import HTTPException

T = TypeVar("T")


def get_or_404(getter: Callable[..., Optional[T]], *args, **kwargs) -> T:
    maybe_obj = getter(*args, **kwargs)
    if not maybe_obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return maybe_obj
