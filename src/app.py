import streamlit as st
from educational_books.main import BookFlow
import threading
import time

def reset_state():
  st.session_state.book_outline = None
  st.session_state.book = None
  st.session_state.title = None
  st.session_state.book_flow = None
  st.session_state.section_finished = 0
  st.session_state.total_sections = 0

def start_generation(topic):
  book_flow = BookFlow()
  st.session_state.book_flow = book_flow
  def run_kickoff():
    book_flow.kickoff(inputs={"topic": topic})
  kickoff_thread = threading.Thread(target=run_kickoff)
  kickoff_thread.start()

def update_state():
  book_flow = st.session_state.get("book_flow", None)
  if book_flow is not None:
    if hasattr(book_flow.state, "book_outline") and book_flow.state.book_outline and st.session_state.book_outline is None:
      st.session_state.book_outline = book_flow.state.book_outline_md
      st.session_state.title = book_flow.state.title
      st.session_state.total_sections = len(book_flow.state.book_outline)
    if hasattr(book_flow.state, "section_finished") and book_flow.state.section_finished != st.session_state.section_finished:
      st.session_state.section_finished = book_flow.state.section_finished
    if hasattr(book_flow.state, "book") and book_flow.state.book and st.session_state.book is None:
      st.session_state.book = book_flow.state.book_md
      st.session_state.generation_started = False

st.title("Educational Book Generator")
topic = st.text_input("Enter the topic for the book:", "Bubble Sort")

if "generation_started" not in st.session_state:
  st.session_state.generation_started = False
if "book_outline" not in st.session_state:
  st.session_state.book_outline = None
if "book" not in st.session_state:
  st.session_state.book = None
if "title" not in st.session_state:
  st.session_state.title = None
if "book_flow" not in st.session_state:
  st.session_state.book_flow = None
if "section_finished" not in st.session_state:
  st.session_state.section_finished = 0

# Button to start generation
if st.button("Generate Book"):
  st.session_state.generation_started = True
  reset_state()
  start_generation(topic)

# Show "Generating book..." message if the process has started
if st.session_state.generation_started:
  if st.session_state.book_outline is None:
    st.write("Generating book outline... Please wait.")
  elif st.session_state.book is None:
    st.write("Book Outline is ready")
    outline_filename = f"{st.session_state.title.replace(' ', '_')}_outline.md"
    st.download_button(
      label="Download Book Outline",
      data=st.session_state.book_outline,
      file_name=outline_filename,
      mime="text/markdown"
    )
    st.progress(st.session_state.section_finished / st.session_state.total_sections, text=f"Generating book content... {st.session_state.section_finished}/{st.session_state.total_sections}")
elif st.session_state.book_outline is not None and st.session_state.book is not None:
  st.write("Book Outline is ready")
  outline_filename = f"{st.session_state.title.replace(' ', '_')}_outline.md"
  st.download_button(
    label="Download Book Outline",
    data=st.session_state.book_outline,
    file_name=outline_filename,
    mime="text/markdown"
  )
  st.write("Book content is ready")
  content_filename = f"{st.session_state.title.replace(' ', '_')}.md"
  st.download_button(
    label="Download Generated Book",
    data=st.session_state.book,
    file_name=content_filename,
    mime="text/markdown"
  )
if st.session_state.generation_started:
  time.sleep(5)
  update_state()
  st.rerun()