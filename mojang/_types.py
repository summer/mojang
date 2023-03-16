from datetime import datetime
from typing import List, Optional

from dataclasses import dataclass


@dataclass
class UserProfile:
    id: str
    timestamp: int
    name: str
    is_legacy_profile: bool
    skin_variant: str
    cape_url: Optional[str] = None
    skin_url: Optional[str] = None


@dataclass
class Skin:
    id: str
    enabled: bool
    url: str
    variant: str
    alias: Optional[str] = None


@dataclass
class Cape:
    id: str
    enabled: bool
    url: str
    alias: str


@dataclass
class Profile:
    id: str
    name: str
    capes: List[Cape]
    skins: List[Skin]


@dataclass
class NameInformation:
    name_change_allowed: bool
    created_at: Optional[datetime] = None
    changed_at: Optional[datetime] = None
