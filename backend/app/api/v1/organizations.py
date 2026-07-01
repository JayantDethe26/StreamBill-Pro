from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies import get_current_user

from app.models.user import User 

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    InviteMemberRequest
)

from app.services.organization_service import (
    create_organization,
    get_user_organizations,
    invite_user_to_organization,
    accept_invitation,
    reject_invitation
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=201
)
async def create_org(
    payload: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_organization(
        payload,
        current_user,
        db
    )



@router.get(
    "",
    response_model=list[OrganizationResponse]
)
async def get_organizations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_organizations(
        current_user,
        db
    )



@router.post(
    "/{organization_id}/invite"
)
async def invite_member(
    organization_id: str,
    payload: InviteMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await invite_user_to_organization(
        organization_id,
        payload,
        current_user,
        db
    )


@router.post(
    "/invitations/{invitation_id}/accept"
)
async def accept_user_invitation(
    invitation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await accept_invitation(
        invitation_id,
        current_user,
        db
    )


@router.post(
    "/invitations/{invitation_id}/reject"
)
async def reject_user_invitation(
    invitation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await reject_invitation(
        invitation_id,
        current_user,
        db
    )