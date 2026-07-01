from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.models.user import User
from fastapi import HTTPException
from app.schemas.organization import InviteMemberRequest
from app.schemas.organization import OrganizationCreate


from app.models.organization_invitation import (
    OrganizationInvitation
)



async def create_organization(
    payload: OrganizationCreate,
    current_user: User,
    db: AsyncSession
):

    organization = Organization(
        name=payload.name
    )

    db.add(organization)

    await db.flush()

    owner_record = OrganizationMember(
        user_id=current_user.id,
        organization_id=organization.id,
        role="owner"
    )

    db.add(owner_record)

    await db.commit()
    await db.refresh(organization)

    return organization



async def get_user_organizations(
    current_user: User,
    db: AsyncSession
):

    result = await db.execute(
        select(Organization)
        .join(
            OrganizationMember,
            Organization.id == OrganizationMember.organization_id
        )
        .where(
            OrganizationMember.user_id == current_user.id
        )
    )

    organizations = result.scalars().all()

    return organizations



async def invite_user_to_organization(
    organization_id,
    payload: InviteMemberRequest,
    current_user: User,
    db: AsyncSession
):
    owner_check = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role == "owner"
        )
    )

    owner_record = owner_check.scalar_one_or_none()

    if not owner_record:
        raise HTTPException(
            status_code=403,
            detail="Only owners can invite users"
        )

    existing_invite = await db.execute(
        select(OrganizationInvitation).where(
            OrganizationInvitation.organization_id == organization_id,
            OrganizationInvitation.email == payload.email,
            OrganizationInvitation.status == "pending"
        )
    )

    if existing_invite.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Invitation already exists"
        )

    invitation = OrganizationInvitation(
        organization_id=organization_id,
        invited_by=current_user.id,
        email=payload.email,
        status="pending"
    )

    db.add(invitation)

    await db.commit()
    await db.refresh(invitation)

    return {
        "message": "Invitation created",
        "invitation_id": str(invitation.id)
    }



async def accept_invitation(
    invitation_id,
    current_user: User,
    db: AsyncSession
):
    invitation_result = await db.execute(
        select(OrganizationInvitation).where(
            OrganizationInvitation.id == invitation_id
        )
    )

    invitation = invitation_result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Invitation not found"
        )

    if invitation.email != current_user.email:
        raise HTTPException(
            status_code=403,
            detail="This invitation does not belong to you"
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Invitation already processed"
        )

    existing_member_result = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == invitation.organization_id,
            OrganizationMember.user_id == current_user.id
        )
    )

    existing_member = existing_member_result.scalar_one_or_none()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User already belongs to organization"
        )

    member = OrganizationMember(
        user_id=current_user.id,
        organization_id=invitation.organization_id,
        role="member"
    )

    db.add(member)

    invitation.status = "accepted"

    await db.commit()

    return {
        "message": "Invitation accepted"
    }


async def reject_invitation(
    invitation_id,
    current_user: User,
    db: AsyncSession
):
    invitation_result = await db.execute(
        select(OrganizationInvitation).where(
            OrganizationInvitation.id == invitation_id
        )
    )

    invitation = invitation_result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Invitation not found"
        )

    if invitation.email != current_user.email:
        raise HTTPException(
            status_code=403,
            detail="This invitation does not belong to you"
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Invitation already processed"
        )

    invitation.status = "rejected"

    await db.commit()

    return {
        "message": "Invitation rejected"
    }