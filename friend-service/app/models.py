# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    friend_id = Column(String, index=True)

class FriendRequest(Base):
    __tablename__ = "friend-requests"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(String, index=True)
    to_user_id = Column(String, index=True)
    status = Column(String, default="pending")
