import json
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def evaluate_report():
    report_file = "report.json"

    if not os.path.exists(report_file):
        print(
            "FAILURE\nFeedback: The file 'report.json' was not found. Please use WRITE_REPORT first."
        )
        sys.exit(1)

    try:
        with open(report_file, "r", encoding="utf-8") as f:
            report_data = f.read()
            json.loads(report_data)
    except json.JSONDecodeError:
        print("FAILURE\nFeedback: The file 'report.json' contains invalid JSON syntax.")
        sys.exit(1)

    client = OpenAI(
        base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.environ.get("OPENROUTER_API_KEY"),
    )

    prompt = f"""
    You are a strict but fair VC analyst. Evaluate the following JSON report.
    Grade it from 0 to 100 based strictly on these 4 criteria:
    1. Are the founders identified?
    2. Is the core problem and revenue model present?
    3. Is the investment recommendation logical?
    4. Are any fields empty or "N/A"?

    CRITICAL RULE: If all 4 criteria are met with reasonable detail, you MUST give a score of 100. Do NOT ask for complex financial projections, market analysis, or data that is impossible to find in a quick web search.

    Report to evaluate:
    {report_data}
    
    Return ONLY a valid JSON object with "score" (integer) and "feedback" (string).
    """

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1,
        )

        evaluation = json.loads(response.choices[0].message.content)
        score = evaluation.get("score", 0)
        feedback = evaluation.get("feedback", "Error generating feedback.")

        print(f"--- JUDGE EVALUATION ---")
        print(f"Score: {score}/100")

        if score == 100:
            print("SUCCESS")
            print("Feedback: The report meets all criteria.")
        else:
            print("FAILURE")
            print(f"Feedback: {feedback}")

    except Exception as e:
        print(f"FAILURE\nFeedback: Error contacting Judge API: {str(e)}")


if __name__ == "__main__":
    evaluate_report()
