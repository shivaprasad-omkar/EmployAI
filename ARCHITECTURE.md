
# EmployAI — System Architecture

## System Workflow

```mermaid
flowchart TD
    A["User"] --> B["Streamlit UI - ui.py"]

    B --> C["Company Intelligence"]
    B --> D["Interview Studio"]
    B --> E["Dashboard"]
    B --> F["My Reports"]

    C --> G["Backend - app.py"]
    G --> H["Tavily Search API"]
    H --> I["Company Research"]
    H --> J["Job Role Research"]

    I --> K["Briefing Generator"]
    J --> K

    K --> L["Briefing Report"]

    D --> M["Assessment - assessment.py"]
    M --> N["Keyword Matching"]
    N --> O["Assessment Report"]

    L --> P["Text File Storage"]
    O --> P

    P --> F
    P --> E
```

## Technology Architecture

| Component | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | User interface |
| Backend | Python | Application logic |
| Research | Tavily API | Web research |
| Assessment | Python | Keyword-based evaluation |
| Configuration | python-dotenv | Secure API key loading |
| Storage | Text files | Save generated reports |

## Application Flow

1. User enters company and job-role details.
2. Streamlit sends the information to the Python backend.
3. Tavily searches for relevant company and job-role information.
4. EmployAI generates a pre-meeting briefing.
5. Interview Studio generates questions and evaluates submitted answers.
6. Reports are saved as text files.
7. Users can access reports through the Dashboard and My Reports.

## Future Scope

- Semantic AI-based interview evaluation.
- More detailed company intelligence.
- Personalized interview preparation.
- PDF report generation.
- Additional research sources.
