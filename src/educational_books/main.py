#!/usr/bin/env python
from pydantic import BaseModel
from typing import List
from crewai.flow.flow import Flow, listen, start
from educational_books.crews.book_outline.book_outline import BookOutlineCrew
from educational_books.types import Section, SectionOutline

class BookState(BaseModel):
  title: str = "Algorithm and Data Structures"
  book: List[Section] = []
  book_outline: List[SectionOutline] = []
  topic: str = "Algorithm and Data Structures"

class BookFlow(Flow[BookState]):
  initial_state = BookState

  @start()
  def generate_book_outline(self):
    print("Generating book outline")
    crew = BookOutlineCrew()
    outline = crew.crew().kickoff(inputs={"topic": self.state.topic})
    self.state.book_outline = outline["sections"]
  
  @listen(generate_book_outline)
  def save_book_outline(self):
    print("Saving book outline")
    with open("book_outline.md", "w") as f:
      for section in self.state.book_outline:
        f.write(f"# {section.title}\n")
        f.write(f"{section.description}\n\n")
        f.write(f"## Covered Skills\n")
        for skill in section.covered_skills:
          f.write(f"- {skill}\n")
        f.write("\n")
        f.write(f"## Learning Objectives\n")
        for objective in section.objectives:
          f.write(f"- {objective}\n")

def kickoff():
    poem_flow = BookFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = BookFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
