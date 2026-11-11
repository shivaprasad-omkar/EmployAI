
import streamlit as st
from pathlib import Path
from datetime import datetime
import re

import app
import assessment


# ==========================================
# EMPLOYAI 2047 - CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="EmployAI | Future Career Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

if "nav_widget" not in st.session_state:
    st.session_state.nav_widget = "Home"

if "company_results" not in st.session_state:
    st.session_state.company_results = []

if "job_results" not in st.session_state:
    st.session_state.job_results = []

if "assessment_questions" not in st.session_state:
    st.session_state.assessment_questions = []

if "assessment_report" not in st.session_state:
    st.session_state.assessment_report = ""

if "briefing_report" not in st.session_state:
    st.session_state.briefing_report = ""

if "research_info" not in st.session_state:
    st.session_state.research_info = {}


# ==========================================
# FUTURISTIC DESIGN SYSTEM
# ==========================================

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
      radial-gradient(ellipse at 10% 5%, #10264a 0%, transparent 35%),
      radial-gradient(ellipse at 90% 20%, #251449 0%, transparent 30%),
      #070b17;
    color: #eef4ff;
    font-family: Inter, sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0d1730,#080d1b);
    border-right: 1px solid #203655;
}

section[data-testid="stSidebar"] * {
    color: #e7efff;
}

.stButton button, .stDownloadButton button {
    background: linear-gradient(100deg,#087fba,#7045cf);
    color: white;
    border: 1px solid #55c9ff;
    border-radius: 12px;
    font-weight: 700;
    transition: 0.25s;
}

.stButton button:hover, .stDownloadButton button:hover {
    border-color: #a8efff;
    box-shadow: 0 0 20px #16b9ef66;
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg,#111f39,#101329);
    border: 1px solid #263e62;
    padding: 18px;
    border-radius: 16px;
}

div[data-testid="stMetricValue"] {
    color: #4edcff;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #101a30;
    color: white;
    border: 1px solid #345174;
    border-radius: 10px;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #101a30;
}

div[data-testid="stExpander"] {
    background: #101a30;
    border: 1px solid #263e62;
    border-radius: 12px;
}

hr {
    border-color: #243956;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 7px;
}

</style>
""")

# ==========================================
# HELPERS
# ==========================================

def go_to(page):
    st.session_state.nav_widget = page


def safe_name(name):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def get_reports():
    files = (
        list(BASE_DIR.glob("*_briefing.txt"))
        + list(BASE_DIR.glob("*_assessment.txt"))
    )
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)


def show_sources(results):
    if not results:
        st.info("No research sources available.")
        return

    for index, item in enumerate(results, 1):
        with st.container(border=True):
            st.markdown(f"**{index}. {item.get('title', 'Untitled')}**")
            st.write(item.get("content", "No summary available."))
            url = item.get("url", "")
            if url.startswith("https://") or url.startswith("http://"):
                st.link_button("Open original source", url)


def show_header(section, description):
    st.markdown(f"## {section}")
    st.caption(description)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:
    st.markdown("# 🚀 EmployAI")
    st.caption("FUTURE CAREER INTELLIGENCE")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Dashboard",
            "Company Intelligence",
            "Interview Studio",
            "My Reports"
        ],
        key="nav_widget"
    )

    st.markdown("---")
    st.markdown("### SYSTEM STATUS")
    st.success("Interface active")
    st.caption("Research engine: Tavily")
    st.caption("Assessment: Keyword prototype")
    st.markdown("---")
    st.caption("EMPLOYAI · VERSION 1.0")


# ==========================================
# HOME
# ==========================================

if page == "Home":

    st.html("""
    <div style="
        padding:55px 35px;
        border:1px solid #28517a;
        border-radius:25px;
        background:
        radial-gradient(circle at 80% 10%,#37216c 0%,transparent 35%),
        linear-gradient(120deg,#101d39,#11152c);
        box-shadow:0 0 45px #087fba22;
        margin-bottom:25px;">
        <div style="color:#4edcff;font-size:12px;letter-spacing:4px;">
        THE FUTURE OF CAREER PREPARATION · 2047
        </div>
        <h1 style="font-size:48px;color:white;margin:20px 0 10px;">
        Research. Prepare.<br>
        <span style="color:#4edcff;">Succeed.</span>
        </h1>
        <p style="color:#a9bbd8;font-size:17px;max-width:650px;">
        Your intelligent career preparation workspace.
        Discover companies, understand job requirements,
        and prepare for important professional meetings.
        </p>
        <div style="margin-top:30px;color:#4edcff;font-size:12px;">
        INTELLIGENCE SYSTEM ONLINE · EMPLOYAI
        </div>
    </div>
    """)

    st.markdown("### YOUR INTELLIGENCE WORKSPACE")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.markdown("### 🔍")
            st.markdown("**Company Intelligence**")
            st.caption("Research company updates and job requirements.")
            st.button(
                "Explore Research",
                key="home_research",
                use_container_width=True,
                on_click=go_to,
                args=("Company Intelligence",)
            )

    with c2:
        with st.container(border=True):
            st.markdown("### 🧠")
            st.markdown("**Interview Studio**")
            st.caption("Practise questions generated from job research.")
            st.button(
                "Open Studio",
                key="home_interview",
                use_container_width=True,
                on_click=go_to,
                args=("Interview Studio",)
            )

    with c3:
        with st.container(border=True):
            st.markdown("### 📊")
            st.markdown("**Dashboard**")
            st.caption("Access your activity and reports.")
            st.button(
                "Open Dashboard",
                key="home_dashboard",
                use_container_width=True,
                on_click=go_to,
                args=("Dashboard",)
            )

    st.markdown("---")
    st.markdown("### HOW EMPLOYAI WORKS")

    st.markdown("""
    1. **Research:** Enter a company and job role.
    2. **Discover:** Tavily gathers relevant information.
    3. **Prepare:** Generate interview questions.
    4. **Evaluate:** Submit answers and receive prototype feedback.
    5. **Save:** Download your briefing and assessment reports.
    """)


# ==========================================
# DASHBOARD
# ==========================================

elif page == "Dashboard":

    show_header(
        "AI COMMAND CENTER",
        "Your EmployAI activity and workspace overview."
    )

    reports = get_reports()
    briefing_count = len(list(BASE_DIR.glob("*_briefing.txt")))
    assessment_count = len(list(BASE_DIR.glob("*_assessment.txt")))

    c1, c2, c3 = st.columns(3)

    c1.metric("Briefing Reports", briefing_count)
    c2.metric("Assessment Reports", assessment_count)
    c3.metric(
        "Current Research",
        "Available" if st.session_state.briefing_report else "Not started"
    )

    st.markdown("### QUICK ACCESS")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("#### 🔍 Company Intelligence")
            st.write("Start a new company research session.")
            st.button(
                "Start Research",
                use_container_width=True,
                on_click=go_to,
                args=("Company Intelligence",)
            )

    with right:
        with st.container(border=True):
            st.markdown("#### 🧠 Interview Studio")
            st.write("Continue your interview preparation.")
            st.button(
                "Open Interview Studio",
                use_container_width=True,
                on_click=go_to,
                args=("Interview Studio",)
            )

    st.markdown("### RECENT REPORTS")

    if reports:
        for file in reports[:5]:
            st.write("📄", file.name)
    else:
        st.info("Your generated reports will appear here.")

    st.button(
        "View All Reports",
        on_click=go_to,
        args=("My Reports",)
    )


# ==========================================
# COMPANY INTELLIGENCE
# ==========================================

elif page == "Company Intelligence":

    show_header(
        "COMPANY INTELLIGENCE",
        "Powered by Tavily research engine."
    )

    st.markdown("### NEW RESEARCH SESSION")

    with st.form("research_form"):

        company = st.text_input(
            "Company / Person Name",
            placeholder="Example: Microsoft"
        )

        job_role = st.text_input(
            "Job Role",
            value="Software Developer"
        )

        experience = st.selectbox(
            "Experience Level",
            ["Fresher", "Experienced"]
        )

        meeting_date = st.date_input(
            "Meeting Date",
            value=datetime.now().date()
        )

        meeting_time = st.time_input(
            "Meeting Time",
            value=datetime.now().time().replace(
                second=0, microsecond=0
            )
        )

        focus = st.selectbox(
            "Preparation Focus",
            ["both", "technical", "hr"]
        )

        submitted = st.form_submit_button(
            "🚀 Start AI Research",
            use_container_width=True
        )

    if submitted:

        if not company.strip():
            st.error("Please enter a company or person name.")

        else:
            try:
                with st.spinner(
                    "Connecting to Tavily and researching..."
                ):

                    client = app.initialize_tavily()

                    company_results = app.research_company(
                        client,
                        company.strip(),
                        meeting_date
                    )

                    job_results = app.research_job_role(
                        client,
                        company.strip(),
                        job_role.strip() or "General",
                        experience
                    )

                    company_results = app.remove_duplicate_sources(
                        company_results
                    )

                    job_results = app.remove_duplicate_sources(
                        job_results
                    )

                    briefing = app.build_briefing(
                        company.strip(),
                        meeting_date,
                        meeting_time.strftime("%H:%M"),
                        job_role.strip() or "General",
                        experience,
                        focus,
                        company_results,
                        job_results
                    )

                    filename = (
                        safe_name(company)
                        + "_briefing.txt"
                    )

                    app.save_text_file(filename, briefing)

                    st.session_state.company_results = company_results
                    st.session_state.job_results = job_results
                    st.session_state.briefing_report = briefing

                    st.session_state.research_info = {
                        "company": company.strip(),
                        "job_role": job_role.strip() or "General",
                        "experience": experience,
                        "focus": focus
                    }

                    st.session_state.assessment_questions = (
                        assessment.generate_questions(
                            job_role.strip() or "General",
                            job_results
                        )
                    )

                    st.session_state.assessment_report = ""

                st.success("Research completed and briefing saved!")

            except Exception as error:
                st.error("Research could not be completed.")
                st.caption(
                    "Check your internet connection, Tavily API key "
                    "and API access."
                )
                st.code(str(error))

    if st.session_state.briefing_report:

        st.markdown("---")
        st.markdown("## RESEARCH RESULTS")

        info = st.session_state.research_info

        st.markdown(
            f"### {info.get('company', 'Company')} "
            f"| {info.get('job_role', '')}"
        )

        a, b = st.columns(2)
        a.metric(
            "Company Updates",
            len(st.session_state.company_results)
        )
        b.metric(
            "Job Research Sources",
            len(st.session_state.job_results)
        )

        with st.expander("Company Developments", expanded=True):
            show_sources(st.session_state.company_results)

        with st.expander("Job Role Research", expanded=True):
            show_sources(st.session_state.job_results)

        with st.expander("Interview Preparation Questions"):
            sections = app.create_interview_questions(
                info.get("job_role", "General"),
                info.get("focus", "both")
            )

            for heading, questions in sections:
                st.markdown(f"**{heading}**")
                for index, question in enumerate(questions, 1):
                    st.write(f"{index}. {question}")

        st.download_button(
            "⬇ Download Briefing Report",
            data=st.session_state.briefing_report,
            file_name="employai_briefing.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.button(
            "Continue to Interview Studio →",
            on_click=go_to,
            args=("Interview Studio",)
        )


# ==========================================
# INTERVIEW STUDIO
# ==========================================

elif page == "Interview Studio":

    show_header(
        "INTERVIEW STUDIO",
        "Practise using questions generated from your job research."
    )

    info = st.session_state.research_info

    if not st.session_state.job_results:
        st.warning(
            "First complete Company Intelligence research "
            "to generate role-based questions."
        )

        st.button(
            "Go to Company Intelligence",
            on_click=go_to,
            args=("Company Intelligence",)
        )

    else:

        st.markdown(
            f"### {info.get('company', 'Company')} · "
            f"{info.get('job_role', 'General')}"
        )

        questions = st.session_state.assessment_questions

        if not questions:
            questions = assessment.generate_questions(
                info.get("job_role", "General"),
                st.session_state.job_results
            )
            st.session_state.assessment_questions = questions

        if questions:

            st.info(
                f"{len(questions)} questions generated from "
                "your job research."
            )

            with st.form("interview_assessment_form"):

                answers = []

                for index, item in enumerate(questions, 1):

                    st.markdown(
                        f"**Question {index}**"
                    )

                    st.write(item["question"])

                    answer = st.text_area(
                        "Your Answer",
                        key=f"interview_answer_{index}",
                        height=120,
                        placeholder="Write your answer here..."
                    )

                    answers.append({
                        "question": item["question"],
                        "answer": answer.strip(),
                        "keywords": item["keywords"]
                    })

                submit_assessment = st.form_submit_button(
                    "Submit Answers & Evaluate",
                    use_container_width=True
                )

            if submit_assessment:

                if not any(item["answer"] for item in answers):
                    st.warning("Please answer at least one question.")

                else:

                    evaluations = assessment.evaluate_answers(
                        answers
                    )

                    report = assessment.create_assessment_report(
                        info.get("company", "Unknown"),
                        info.get("job_role", "General"),
                        info.get("experience", "Fresher"),
                        evaluations
                    )

                    st.session_state.assessment_report = report
                    st.session_state.assessment_evaluations = evaluations

                    filename = (
                        safe_name(info.get("company", "company"))
                        + "_assessment.txt"
                    )

                    app.save_text_file(filename, report)

                    st.success("Assessment completed!")

        if st.session_state.assessment_report:

            st.markdown("---")
            st.markdown("## YOUR ASSESSMENT RESULT")

            evaluations = st.session_state.get(
                "assessment_evaluations", []
            )

            total_score = sum(
                item["score"] for item in evaluations
            )

            maximum_score = len(evaluations) * 10

            percentage = (
                total_score / maximum_score * 100
                if maximum_score else 0
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Score",
                f"{total_score}/{maximum_score}"
            )

            c2.metric(
                "Percentage",
                f"{percentage:.1f}%"
            )

            c3.metric(
                "Questions Answered",
                sum(
                    1 for item in evaluations
                    if item["answer"]
                )
            )

            for index, item in enumerate(evaluations, 1):

                with st.expander(
                    f"Question {index} · {item['score']}/10"
                ):

                    st.write(item["question"])
                    st.write("**Your answer:**")
                    st.write(item["answer"])

                    st.write(
                        "Matched topics:",
                        ", ".join(item["matched"]) or "None"
                    )

                    st.write(
                        "Topics to review:",
                        ", ".join(item["missing"]) or "Review answer depth"
                    )

            st.warning(
                "Prototype limitation: scores use keyword matching. "
                "They do not measure the meaning, accuracy or quality "
                "of an answer and are not hiring decisions."
            )

            st.download_button(
                "⬇ Download Assessment Report",
                data=st.session_state.assessment_report,
                file_name="employai_assessment.txt",
                mime="text/plain",
                use_container_width=True
            )


# ==========================================
# MY REPORTS
# ==========================================

elif page == "My Reports":

    show_header(
        "MY REPORTS",
        "Your saved company briefings and assessment reports."
    )

    reports = get_reports()

    if not reports:
        st.info("No saved reports yet.")
        st.button(
            "Start Your First Research",
            on_click=go_to,
            args=("Company Intelligence",)
        )

    else:

        st.metric("Total Saved Reports", len(reports))

        for file in reports:

            with st.expander(file.name):

                try:
                    content = file.read_text(encoding="utf-8")

                    st.text_area(
                        "Report Preview",
                        content,
                        height=300,
                        key=f"preview_{file.name}"
                    )

                    st.download_button(
                        "Download Report",
                        data=content,
                        file_name=file.name,
                        mime="text/plain",
                        key=f"download_{file.name}"
                    )

                except Exception:
                    st.error("Unable to read this report file.")


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "EMPLOYAI 2047 · Research. Prepare. Succeed. "
    "| AI-powered career preparation workspace"
)
