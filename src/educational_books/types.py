from typing import List
from pydantic import BaseModel
class SectionOutline(BaseModel):
  title: str
  description: str
  covered_skills: List[str]
  objectives: List[str]

class BookOutline(BaseModel):
  sections: List[SectionOutline]

class Section(BaseModel):
  title: str
  content: str