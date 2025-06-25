from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db, get_current_user, role_required
from app.schemas.user import UserOut, UserUpdate
from app.services import user_service
from app.db.models import Role, User
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    try:
        return current_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not fetch user details.")

@router.get("/all", response_model=list[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    _: User = Depends(role_required([Role.ADMIN, Role.MANAGER]))
) -> list[UserOut]:
    try:
        return user_service.get_all_users(db)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not fetch users.")

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: UUID = Path(...),
    db: Session = Depends(get_db),
    _: User = Depends(role_required([Role.ADMIN, Role.MANAGER]))
):
    try:
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not fetch user.")

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user_to_update = user_service.get_user_by_id(db, user_id)
        if not user_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if current_user.role not in [Role.ADMIN, Role.MANAGER] and user_to_update.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        return user_service.update_user(db, user_to_update, user_update.dict(exclude_unset=True))
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during user update.")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(role_required([Role.ADMIN]))
):
    try:
        user_to_delete = user_service.get_user_by_id(db, user_id)
        if not user_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_service.delete_user(db, user_to_delete)
        return None
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error during user deletion.")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
