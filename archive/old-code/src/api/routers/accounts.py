"""Account CRUD routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.db import models

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


class AccountCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    employee_count: Optional[int] = None
    employee_band: Optional[str] = None
    tier: Optional[str] = None
    known_tools: Optional[list] = []
    linkedin_company_url: Optional[str] = None
    website_url: Optional[str] = None
    buyer_intent: Optional[int] = 0
    hq_location: Optional[str] = None
    notes: Optional[str] = None


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    employee_count: Optional[int] = None
    employee_band: Optional[str] = None
    tier: Optional[str] = None
    known_tools: Optional[list] = None
    linkedin_company_url: Optional[str] = None
    website_url: Optional[str] = None
    buyer_intent: Optional[int] = None
    hq_location: Optional[str] = None
    notes: Optional[str] = None


@router.post("")
def create_account(account: AccountCreate):
    return models.create_account(account.model_dump())


@router.get("")
def list_accounts(limit: int = 100, offset: int = 0, industry: str = None):
    return models.list_accounts(limit=limit, offset=offset, industry=industry)


@router.get("/{account_id}")
def get_account(account_id: str):
    result = models.get_account(account_id)
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result


@router.patch("/{account_id}")
def update_account(account_id: str, data: AccountUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = models.update_account(account_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result
