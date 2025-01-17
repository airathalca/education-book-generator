#!/usr/bin/env python
from pydantic import BaseModel
from typing import List
from crewai.flow.flow import Flow, listen, start
from educational_books.crews.book_outline.book_outline import BookOutlineCrew
from educational_books.crews.book_content.book_content import BookContentCrew
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

  @listen(generate_book_outline)
  def generate_book(self):
    print("Generating book")
    crew = BookContentCrew()
    book_outline = [section.model_dump_json() for section in self.state.book_outline]
    for section in self.state.book_outline:
      print(f"Generating content for {section.title}")
      content = crew.crew().kickoff(inputs={
        "topic": self.state.topic,
        "section_title": section.title,
        "section_description": section.description,
        "covered_skills": section.covered_skills,
        "objectives": section.objectives,
        "book_outline": book_outline
      })
      print(f"Content generated for {section.title} with {len(content['content'])} characters")
      title = content["title"]
      resources = content["resources"]
      content = content["content"]
      section = Section(title=title, resources=resources, content=content)
      self.state.book.append(section)
    print(f"Book generated with {len(self.state.book)} sections")

  @listen(generate_book)
  def save_book(self):
    print("Saving book")
    with open(f"{self.state.title.replace(' ', '_')}.md", "w") as f:
      for section in self.state.book:
        f.write(f"# {section.title}\n")
        f.write(f"{section.content}\n\n")
        f.write(f"## Resources\n")
        for resource in section.resources:
          f.write(f"- {resource}\n")
        f.write("\n")

def kickoff():
  poem_flow = BookFlow()
  poem_flow.kickoff()

def plot():
  poem_flow = BookFlow()
  poem_flow.plot()


if __name__ == "__main__":
  kickoff()
