# app/routes.py
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, utils

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/request", response_model=schemas.FriendRequestOut)
def send_friend_request(
    request: schemas.FriendRequestIn,
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    from_user_id = utils.verify_jwt(Authorization.split(" ")[1])
    if from_user_id == request.to_user_id:
        raise HTTPException(status_code=400, detail="You can't friend yourself")

    existing = db.query(models.FriendRequest).filter(
        models.FriendRequest.from_user_id == from_user_id,
        models.FriendRequest.to_user_id == request.to_user_id,
        models.FriendRequest.status == "pending"
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Friend request already sent")

    friend_request = models.FriendRequest(
        from_user_id=from_user_id,
        to_user_id=request.to_user_id
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return friend_request

@router.post("/accept/{request_id}")
def accept_friend_request(
    request_id: int,
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    to_user_id = utils.verify_jwt(Authorization.split(" ")[1])

    friend_request = db.query(models.FriendRequest).filter(
        models.FriendRequest.id == request_id,
        models.FriendRequest.to_user_id == to_user_id,
        models.FriendRequest.status == "pending"
    ).first()

    if not friend_request:
        raise HTTPException(status_code=404, detail="Request not found or already handled")

    # Mark as accepted
    friend_request.status = "accepted"

    # Create friendship both ways
    db.add_all([
        models.Friendship(user_id=to_user_id, friend_id=friend_request.from_user_id),
        models.Friendship(user_id=friend_request.from_user_id, friend_id=to_user_id)
    ])
    db.commit()
    return {"message": "Friend request accepted"}

@router.get("/requests", response_model=list[schemas.FriendRequestOut])
def list_pending_requests(
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user_id = utils.verify_jwt(Authorization.split(" ")[1])
    requests = db.query(models.FriendRequest).filter(
        models.FriendRequest.to_user_id == user_id,
        models.FriendRequest.status == "pending"
    ).all()
    return requests

@router.get("/", response_model=list[schemas.FriendOut])
def list_friends(
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user_id = utils.verify_jwt(Authorization.split(" ")[1])
    friends = db.query(models.Friendship).filter(
        models.Friendship.user_id == user_id
    ).all()
    return friends

@router.delete("/{friend_id}")
def remove_friend(
    friend_id: str,
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user_id = utils.verify_jwt(Authorization.split(" ")[1])

    db.query(models.Friendship).filter(
        ((models.Friendship.user_id == user_id) & (models.Friendship.friend_id == friend_id)) |
        ((models.Friendship.user_id == friend_id) & (models.Friendship.friend_id == user_id))
    ).delete(synchronize_session=False)

    db.commit()
    return {"message": "Friend removed"}
