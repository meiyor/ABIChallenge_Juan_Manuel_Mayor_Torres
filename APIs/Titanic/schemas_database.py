from pydantic import BaseModel


class ItemBase(BaseModel):
    username: str
    code: str
    date: str
    model: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
