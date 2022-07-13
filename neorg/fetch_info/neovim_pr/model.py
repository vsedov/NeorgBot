from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class PRRequestModelItem(BaseModel):
    """Temp documentation."""
    url: Optional[str] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    html_url: Optional[str] = None
    diff_url: Optional[str] = None
    patch_url: Optional[str] = None
    issues_url: Optional[Any] = None
    pr_number: Optional[int] = None
    state: Optional[str] = None
    locked: Optional[bool]
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    merged_at: Optional[datetime] = None
    merge_commit_sha: Optional[str] = None


class PRRequestModel(BaseModel):
    """Temp documentation."""
    response: List[PRRequestModelItem]
