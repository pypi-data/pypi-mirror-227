from typing import List

from api_compose.root.models.specification import SpecificationModel
from api_compose.services.common.models.base import BaseModel


class SessionModel(BaseModel):
    specifications: List[SpecificationModel]
