from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas import UserCreateRequest, UserResponse
from app.api.dependencies import get_by_email_use_case, get_register_use_case
from app.application.use_cases import GetUserByEmailUseCase, RegisterUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreateRequest,
    use_case: RegisterUserUseCase = Depends(get_register_use_case),
):
    try:
        user = await use_case.execute(email=payload.email, raw_password=payload.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_email(
    email: str,
    use_case: GetUserByEmailUseCase = Depends(get_by_email_use_case),
):
    try:
        user = await use_case.execute(email=email)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    