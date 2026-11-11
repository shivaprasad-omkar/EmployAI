
from datetime import datetime, timedelta
from pathlib import Path
import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient
import assessment


def show_header():
    print("=" * 60)
    print("          PRE-MEETING BRIEFING AGENT")
    print("=" * 60)


def get_meeting_details():
    print("\nMEETING DETAILS")
    print("-" * 60)

    company = input("Company / Person Name: ").strip()
    while not company:
        company = input("Please enter a company / person name: ").strip()

    date_text = input("Meeting Date (DD/MM/YYYY): ").strip()
    meeting_time = input("Meeting Time: ").strip()
    job_role = input("Job Role: ").strip()
    experience = input("Experience (Fresher/Experienced): ").strip()
    focus = input("Focus (Technical/HR/Both): ").strip().lower()

    meeting_date = datetime.strptime(date_text, "%d/%m/%Y").date()

    if not job_role:
        job_role = "General"

    if not experience:
        experience = "Fresher"

    if focus not in ["technical", "hr", "both"]:
        focus = "both"

    return company, meeting_date, meeting_time, job_role, experience, focus


def initialize_tavily():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in .env file.")

    return TavilyClient(api_key=api_key)


def research_company(client, company, meeting_date):
    print("\nResearching company developments...")

    start_date = meeting_date - timedelta(days=30)

    response = client.search(
        query=(
            f"{company} company news announcements product launches "
            "partnerships leadership and business updates"
        ),
        topic="news",
        start_date=start_date.isoformat(),
        end_date=meeting_date.isoformat(),
        max_results=10,
        search_depth="advanced"
    )

    return response.get("results", [])


def research_job_role(client, company, job_role, experience):
    print("Researching job role requirements...")

    query = (
        f"{company} {job_role} {experience} job role "
        "skills responsibilities technical requirements "
        "interview preparation and hiring trends"
    )

    response = client.search(
        query=query,
        topic="general",
        max_results=7,
        search_depth="advanced"
    )

    return response.get("results", [])


def remove_duplicate_sources(results):
    unique = []
    seen = set()

    for item in results:
        url = item.get("url", "")

        if url and url not in seen:
            seen.add(url)
            unique.append(item)

    return unique


def create_interview_questions(job_role, focus):
    technical = [
        f"What are the important technical skills required for a {job_role}?",
        "Explain a technical project you have worked on.",
        "How do you identify and fix errors in your code?",
        "How do you approach solving an unfamiliar technical problem?",
        "How do you keep your technical knowledge up to date?"
    ]

    hr = [
        "Tell me about yourself.",
        "Why are you interested in this company?",
        "What are your strengths and areas to improve?",
        "How do you handle challenges while working in a team?",
        "What are your career goals?"
    ]

    sections = []

    if focus in ["technical", "both"]:
        sections.append(("TECHNICAL QUESTIONS", technical))

    if focus in ["hr", "both"]:
        sections.append(("HR QUESTIONS", hr))

    return sections


def build_briefing(
    company,
    meeting_date,
    meeting_time,
    job_role,
    experience,
    focus,
    company_results,
    job_results
):
    lines = []

    lines.append("=" * 65)
    lines.append("PRE-MEETING BRIEFING REPORT")
    lines.append("=" * 65)

    lines.append(f"\nCompany / Person: {company}")
    lines.append(f"Meeting Date: {meeting_date.strftime('%d/%m/%Y')}")
    lines.append(f"Meeting Time: {meeting_time}")
    lines.append(f"Job Role: {job_role}")
    lines.append(f"Experience: {experience}")
    lines.append(f"Preparation Focus: {focus.title()}")

    lines.append("\n" + "=" * 65)
    lines.append("1. COMPANY DEVELOPMENTS - PREVIOUS 30 DAYS")
    lines.append("=" * 65)

    if company_results:
        for i, item in enumerate(company_results, 1):
            lines.append(f"\n{i}. {item.get('title', 'Untitled')}")
            lines.append(item.get('content', 'No summary available.'))
            lines.append(f"Source: {item.get('url', 'Not available')}")
    else:
        lines.append("No company updates were found.")

    lines.append("\n" + "=" * 65)
    lines.append("2. JOB ROLE RESEARCH")
    lines.append("=" * 65)

    if job_results:
        for i, item in enumerate(job_results, 1):
            lines.append(f"\n{i}. {item.get('title', 'Untitled')}")
            lines.append(item.get('content', 'No summary available.'))
            lines.append(f"Source: {item.get('url', 'Not available')}")
    else:
        lines.append("No job role research results were found.")

    lines.append("\n" + "=" * 65)
    lines.append("3. INTERVIEW PREPARATION")
    lines.append("=" * 65)

    for heading, questions in create_interview_questions(job_role, focus):
        lines.append(f"\n{heading}")

        for i, question in enumerate(questions, 1):
            lines.append(f"{i}. {question}")

    lines.append("\n" + "=" * 65)
    lines.append("4. DISCUSSION QUESTIONS")
    lines.append("=" * 65)

    discussion = [
        f"What are the current priorities for the {job_role} role?",
        "What skills are most important for success in this team?",
        "What challenges is the team currently working to solve?",
        "What are the next steps after this meeting?"
    ]

    for i, question in enumerate(discussion, 1):
        lines.append(f"{i}. {question}")

    lines.append("\n" + "=" * 65)
    lines.append("5. RESEARCH NOTES")
    lines.append("=" * 65)
    lines.append(
        "This report is based on Tavily search results. "
        "Verify important claims using the original source links."
    )
    lines.append(
        "Search results may be incomplete. No result does not prove "
        "that no development occurred."
    )

    lines.append("\n" + "=" * 65)
    lines.append("END OF BRIEFING")
    lines.append("=" * 65)

    return "\n".join(lines)


def save_text_file(file_name, content):
    output_path = Path(__file__).resolve().parent / file_name
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    show_header()

    try:
        (
            company,
            meeting_date,
            meeting_time,
            job_role,
            experience,
            focus
        ) = get_meeting_details()

        client = initialize_tavily()

        company_results = research_company(
            client, company, meeting_date
        )

        job_results = research_job_role(
            client, company, job_role, experience
        )

        company_results = remove_duplicate_sources(company_results)
        job_results = remove_duplicate_sources(job_results)

        briefing = build_briefing(
            company,
            meeting_date,
            meeting_time,
            job_role,
            experience,
            focus,
            company_results,
            job_results
        )

        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", company)
        briefing_file = f"{safe_name}_briefing.txt"

        save_text_file(briefing_file, briefing)

        print("\n" + briefing)
        print(f"\nBriefing saved: {briefing_file}")

        # CONNECTED SKILL ASSESSMENT

        print("\n" + "=" * 60)
        print("             SKILL ASSESSMENT")
        print("=" * 60)

        choice = input(
            "\nWould you like to start Skill Assessment? (yes/no): "
        ).strip().lower()

        if choice in ["yes", "y"]:
            assessment_report = assessment.run_assessment(
                company=company,
                job_role=job_role,
                experience=experience,
                research_data=job_results
            )

            assessment_file = f"{safe_name}_assessment.txt"
            save_text_file(assessment_file, assessment_report)

            print("\nAssessment report saved:", assessment_file)

        else:
            print("\nSkill Assessment skipped.")

        print("\nApplication completed.")

    except ValueError as error:
        print("\nINPUT ERROR:", error)

    except Exception as error:
        print("\nAPPLICATION ERROR:", error)


if __name__ == "__main__":
    main()
