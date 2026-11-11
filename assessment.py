
import re
from collections import Counter


STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this",
    "are", "was", "were", "will", "have", "has", "had",
    "you", "your", "their", "they", "them", "about",
    "into", "using", "used", "use", "can", "all", "our",
    "company", "role", "job", "work", "working", "team",
    "skills", "skill", "experience", "required", "requirements",
    "responsibilities", "including", "such", "more", "most",
    "other", "also", "than", "which", "what", "when",
    "where", "how", "who", "why", "its", "been", "being"
}


def extract_keywords(research_data):
    text = " ".join(
        item.get("title", "") + " " + item.get("content", "")
        for item in research_data
    ).lower()

    words = re.findall(r"\b[a-zA-Z][a-zA-Z+#.]{2,}\b", text)

    filtered = [
        word for word in words
        if word not in STOPWORDS and len(word) > 3
    ]

    counts = Counter(filtered)

    return [word for word, count in counts.most_common(15)]


def generate_questions(job_role, research_data):
    keywords = extract_keywords(research_data)

    if len(keywords) < 5:
        keywords.extend([
            "problem-solving",
            "programming",
            "communication",
            "project",
            "technology"
        ])

    selected_topics = keywords[:5]

    questions = []

    for topic in selected_topics:
        questions.append({
            "question": (
                f"What is {topic}, and how is it relevant "
                f"to a {job_role}? Explain with an example."
            ),
            "keywords": [topic]
        })

    return questions


def conduct_assessment(questions):
    answers = []

    print("\nAnswer the following questions.")
    print("Try to explain each answer in your own words.\n")

    for index, item in enumerate(questions, 1):
        print("-" * 55)
        print(f"Question {index}: {item['question']}")

        answer = input("\nYour answer: ").strip()

        answers.append({
            "question": item["question"],
            "answer": answer,
            "keywords": item["keywords"]
        })

    return answers


def evaluate_answers(answers):
    evaluations = []

    for item in answers:
        answer = item["answer"].lower()
        keywords = item["keywords"]

        matched = [
            keyword for keyword in keywords
            if keyword.lower() in answer
        ]

        # Simple prototype scoring based on keyword coverage.
        score = 10 if matched else 0

        if len(answer.split()) < 5:
            score = min(score, 2)

        evaluations.append({
            "question": item["question"],
            "answer": item["answer"],
            "matched": matched,
            "missing": [
                keyword for keyword in keywords
                if keyword not in matched
            ],
            "score": score
        })

    return evaluations


def create_assessment_report(
    company,
    job_role,
    experience,
    evaluations
):
    total_score = sum(item["score"] for item in evaluations)
    maximum_score = len(evaluations) * 10

    percentage = (
        (total_score / maximum_score) * 100
        if maximum_score else 0
    )

    if percentage < 40:
        level = "Beginner"
    elif percentage < 60:
        level = "Developing"
    elif percentage < 80:
        level = "Intermediate"
    else:
        level = "Strong Foundation"

    lines = []

    lines.append("=" * 60)
    lines.append("SKILL ASSESSMENT REPORT")
    lines.append("=" * 60)

    lines.append(f"\nCompany: {company}")
    lines.append(f"Job Role: {job_role}")
    lines.append(f"Experience Level: {experience}")

    lines.append("\n" + "=" * 60)
    lines.append("ASSESSMENT RESULT")
    lines.append("=" * 60)

    lines.append(f"Total Score: {total_score}/{maximum_score}")
    lines.append(f"Percentage: {percentage:.1f}%")
    lines.append(f"Prototype Level: {level}")

    lines.append("\n" + "=" * 60)
    lines.append("QUESTION-WISE FEEDBACK")
    lines.append("=" * 60)

    for index, item in enumerate(evaluations, 1):
        lines.append(f"\nQuestion {index}: {item['question']}")
        lines.append(f"Your Answer: {item['answer']}")
        lines.append(f"Score: {item['score']}/10")
        lines.append(
            "Matched Keywords: "
            + (", ".join(item["matched"]) or "None")
        )
        lines.append(
            "Topics to review: "
            + (", ".join(item["missing"]) or "Review answer depth")
        )

    lines.append("\n" + "=" * 60)
    lines.append("IMPROVEMENT PLAN")
    lines.append("=" * 60)

    lines.append("1. Review the topics listed as missing.")
    lines.append("2. Practise explaining concepts in your own words.")
    lines.append("3. Add examples from projects or practical work.")
    lines.append("4. Practise answering interview questions clearly.")

    lines.append("\n" + "=" * 60)
    lines.append("SCORING LIMITATION")
    lines.append("=" * 60)

    lines.append(
        "This is a basic keyword-matching prototype. "
        "It does not understand the meaning or correctness of an answer. "
        "The score is not a professional assessment or hiring decision."
    )

    lines.append("\n" + "=" * 60)
    lines.append("END OF ASSESSMENT REPORT")
    lines.append("=" * 60)

    return "\n".join(lines)


def run_assessment(company, job_role, experience, research_data):
    print("\nGenerating assessment questions from job research...")

    questions = generate_questions(job_role, research_data)

    if not questions:
        print("Could not generate assessment questions.")
        return "No assessment questions were generated."

    answers = conduct_assessment(questions)
    evaluations = evaluate_answers(answers)

    report = create_assessment_report(
        company,
        job_role,
        experience,
        evaluations
    )

    print("\n" + report)

    return report

