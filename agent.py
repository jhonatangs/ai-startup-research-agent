import os
import re
import sys
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL = "meta-llama/llama-3.3-70b-instruct"
VENV_PYTHON = "./venv/bin/python"

client = OpenAI(
    base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def run_command(command_list):
    print(f"  [System] Executing: {' '.join(command_list)}")
    try:
        result = subprocess.run(
            command_list, capture_output=True, text=True, check=False
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


def write_file(filename, content):
    print(f"  [System] Writing file: {filename}")
    try:
        clean_content = re.sub(
            r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(clean_content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def run_autonomous_loop(startup_name):
    print(f"\n--- Starting Autonomous ReAct Agent for: {startup_name} ---\n")

    with open("program.md", "r") as f:
        directives = f.read()

    history = [
        {"role": "system", "content": directives},
        {"role": "user", "content": f"Begin research on: {startup_name}"},
    ]

    iteration = 0
    while iteration < 20:  # Limit to 20 iterations to prevent infinite loops
        iteration += 1
        print(f"[Loop {iteration}] Agent is thinking...")

        response = client.chat.completions.create(
            model=MODEL, messages=history, temperature=0, stop=["Observation:"]
        )

        response_text = response.choices[0].message.content
        print(f"\n{response_text}\n")
        history.append({"role": "assistant", "content": response_text})

        if "FINAL_SUCCESS" in response_text:
            print("\n✅ [Agent] Task completed successfully!")
            break

        match = re.search(r"Action:\s*(\w+)\|(.*)", response_text, re.DOTALL)
        observation = ""

        if match:
            action_type = match.group(1).strip()
            action_input = match.group(2).strip()

            if action_type == "RUN_SEARCH":
                observation = run_command(
                    [VENV_PYTHON, "research_tools.py", action_input]
                )
            elif action_type == "WRITE_REPORT":
                observation = write_file("report.json", action_input)
            elif action_type == "RUN_EVALUATOR":
                observation = run_command([VENV_PYTHON, "evaluate.py"])
            else:
                observation = f"Unknown action: {action_type}"
        else:
            observation = "Error: Invalid format. Use 'Action: TYPE|input'."

        if observation:
            print(f"  [System] Observation captured.\n")
            history.append({"role": "user", "content": f"Observation: {observation}"})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent.py "Startup Name"')
        sys.exit(1)
    run_autonomous_loop(sys.argv[1])
