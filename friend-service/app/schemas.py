from pydantic import BaseModel

class FriendRequestIn(BaseModel):
    to_user_id: str

class FriendRequestOut(BaseModel):
    id: int
    from_user_id: str
    to_user_id: str
    status: str

    class Config:
        orm_mode = True

class FriendOut(BaseModel):
    id: int
    user_id: str
    friend_id: str

    class Config:
        orm_mode = True
