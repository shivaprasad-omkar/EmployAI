
# EmployAI
### Research. Prepare. Succeed.

EmployAI is an AI-powered Pre-Meeting Briefing Assistant that helps students and freshers prepare for company meetings and job interviews.

## Features

1. **Company Intelligence**
   - Research company developments from the previous 30 days.
   - Collect information using Tavily Search API.
   - Display research sources and links.

2. **Job Role Research**
   - Research job roles and required skills.
   - Provide role-specific preparation information.

3. **Interview Studio**
   - Generate interview questions.
   - Evaluate submitted answers using keyword matching.
   - Generate assessment reports.

4. **Dashboard**
   - View report statistics.
   - Access project sections.

5. **My Reports**
   - View, preview and download generated reports.

## Technologies Used

- Python
- Streamlit
- Tavily Search API
- python-dotenv

## Project Structure

- `app.py` — Research and briefing backend
- `assessment.py` — Interview assessment module
- `ui.py` — Streamlit user interface
- `.env` — API key configuration
- `.gitignore` — Excludes sensitive files

## Installation

Install dependencies:

```bash
pip install streamlit tavily-python python-dotenv
```

Create a `.env` file:

```text
TAVILY_API_KEY=your_api_key_here
```

Run the application:

```bash
python -m streamlit run ui.py
```

## Security

Keep API keys private. Never upload the `.env` file to a public repository.

## Assessment Limitation

The current assessment uses basic keyword matching. It is a prototype, not a semantic AI evaluation or professional hiring decision.

## Project Goal

To make company research and interview preparation easier and more accessible for students and freshers.

**EmployAI — Your Intelligent Career Preparation Assistant.**
## 🚀 Live Demo

Try EmployAI here:

https://employai-shivaprasad.streamlit.app/
