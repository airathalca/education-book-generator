# Education Book Generator Crew

Welcome to the Education Book Generator Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the requirements:

```bash
uv pip install -r requirements.txt
```

Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

## Customizing

**Add your `SERPER_API_KEY` into the `.env` file**

**Add your `GEMINI_API_KEY` into the `.env` file**

**You can use other LLMs by changing the model in the `src/educational_books/crews/book_content/book_content.py` file and the `src/educational_books/crews/book_outline/book_outline.py` file**

## Running the Project

To run the project, use the following command:

```bash
streamlit run src/app.py
```

## Deployment
You can access the streamlit app by clicking [here](https://huggingface.co/spaces/fr1tzTh/education_book_generator)

## Understanding Your Crew

The educational_books Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.