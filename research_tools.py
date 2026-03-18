import argparse
import json
from ddgs import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """Searches the web and returns a JSON string of the results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return json.dumps({"message": "No results found for the given query."})

        return json.dumps(results, indent=4)

    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Search CLI Tool")
    parser.add_argument("query", type=str)
    parser.add_argument("--max", type=int, default=5)
    args = parser.parse_args()
    print(search_web(args.query, args.max))
