import json


def parse_workflow(response: str):

    try:

        response = response.strip()

        if response.startswith("```json"):
            response = response.replace(
                "```json",
                ""
            )

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        return json.loads(response)

    except Exception as e:

        return {
            "error": str(e),
            "raw_response": response
        }