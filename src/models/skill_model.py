from beanie import Document, Link, before_event, Replace, Insert
from pydantic import Field
from uuid import UUID, uuid4
from src.models.user_model import User
from datetime import datetime
from enum import Enum

class ProficiencyEnum(str, Enum):
    beginner = 'Beginner'
    intermediate = 'Intermediate'
    advanced = 'Advanced'


class Skill(Document):
    skill_id: UUID = Field(default_factory=uuid4, unique=True)
    owner: Link[User]
    name: str
    profiency: ProficiencyEnum

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Skill {self.name}>"

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Skill):
            return self.name == other.name
        return False

    @before_event([Replace, Insert])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = 'skills'
