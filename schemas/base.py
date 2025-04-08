from pydantic import BaseModel
from typing import Optional, Any, List


class BaseResponse(BaseModel):
    status: bool = True
    data: Optional[Any] = None
    errors: Optional[List[dict]] = None