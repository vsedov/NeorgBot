from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


def get_pr_number(pr: str) -> str:
    """Get pr number"""
    return pr.split("/")[-1]


class ID(BaseModel):
    """Temp documentation"""
    number: Optional[int] = None


class PRRequestModelItem(BaseModel):
    """Temp documentation."""
    number: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    html_url: Optional[str] = None
    diff_url: Optional[str] = None
    patch_url: Optional[str] = None
    issues_url: Optional[Any] = None
    state: Optional[str] = None
    locked: Optional[bool]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    merged_at: Optional[datetime] = None
    merge_commit_sha: Optional[str] = None


class PRRequestModel(BaseModel):
    """Temp documentation."""
    total_count: Optional[int] = None
    response: List[PRRequestModelItem]


class DictPRRequestModel(BaseModel):
    """Temp documentation."""
    response: dict[int, List[PRRequestModelItem]] = None
