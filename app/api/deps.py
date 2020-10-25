from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app import schemas
from app.core.config import Settings, get_settings
from app.services.employee import get_employee_by_id

settings: Settings = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_employee(
    token: str = Security(reusable_oauth2),
) -> schemas.Employee:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    employee = await get_employee_by_id(employee_id=token_data.sub)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def get_current_active_employee(current_employee=Security(get_current_employee),):
    if not current_employee["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive employee",
        )
    return current_employee


def get_current_manager(
    current_employee=Security(get_current_active_employee),
) -> schemas.Employee:
    if current_employee["role"] != "manager":
        raise HTTPException(
            status_code=400, detail="The employee doesn't have enough privileges"
        )
    return current_employee


def get_current_assitant(
    current_employee=Security(get_current_active_employee),
) -> schemas.Employee:
    if current_employee["role"] != "assitant":
        raise HTTPException(
            status_code=400, detail="The employee doesn't have enough privileges"
        )
    return current_employee


def get_current_supervisor(
    current_employee=Security(get_current_active_employee),
) -> schemas.Employee:
    if current_employee["role"] != "supervisor":
        raise HTTPException(
            status_code=400, detail="The employee doesn't have enough privileges"
        )
    return current_employee


def get_current_techician(
    current_employee=Security(get_current_active_employee),
) -> schemas.Employee:
    if current_employee["role"] != "technician":
        raise HTTPException(
            status_code=400, detail="The employee doesn't have enough privileges"
        )
    return current_employee