"""Contact CRUD routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.db import models

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


class ContactCreate(BaseModel):
    account_id: Optional[str] = None
    first_name: str
    last_name: str
    title: Optional[str] = None
    persona_type: Optional[str] = None
    seniority_level: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None
    tenure_months: Optional[int] = None
    recently_hired: Optional[int] = 0
    previous_company: Optional[str] = None
    previous_title: Optional[str] = None
    source: Optional[str] = "sales_nav"
    predicted_objection: Optional[str] = None
    objection_response: Optional[str] = None


class ContactUpdate(BaseModel):
    stage: Optional[str] = None
    priority_score: Optional[int] = None
    status: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    predicted_objection: Optional[str] = None
    objection_response: Optional[str] = None
    personalization_score: Optional[int] = None
    do_not_contact: Optional[int] = None
    dnc_reason: Optional[str] = None


@router.post("")
def create_contact(contact: ContactCreate):
    return models.create_contact(contact.model_dump())


@router.get("")
def list_contacts(limit: int = 100, offset: int = 0, stage: str = None,
                  min_priority: int = None, persona_type: str = None,
                  account_id: str = None):
    return models.list_contacts(
        limit=limit, offset=offset, stage=stage,
        min_priority=min_priority, persona_type=persona_type, account_id=account_id
    )


@router.get("/{contact_id}")
def get_contact(contact_id: str):
    result = models.get_contact(contact_id)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result


@router.patch("/{contact_id}")
def update_contact(contact_id: str, data: ContactUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = models.update_contact(contact_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result


@router.post("/{contact_id}/score")
def score_contact(contact_id: str):
    return models.score_and_save(contact_id)


@router.get("/{contact_id}/messages")
def get_contact_messages(contact_id: str):
    return models.get_messages_for_contact(contact_id)


@router.get("/{contact_id}/prep-card")
def prep_card(contact_id: str):
    result = models.get_prep_card(contact_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
