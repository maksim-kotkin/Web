import datetime
from typing import Literal

from pydantic import BaseModel


class IdReturnBase(BaseModel):
    id: int


class StatusSuccessBase(BaseModel):
    status: Literal["success"]


class GetAdvResponse(BaseModel):

    id: int
    title: str
    description: str
    price: int
    author: str
    registration_time: datetime.datetime


class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: int
    author: str


class CreateAdvResponse(IdReturnBase):
    pass


class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None


class UpdateAdvResponse(IdReturnBase):
    pass


class DeleteAdvResponse(StatusSuccessBase):
    pass
