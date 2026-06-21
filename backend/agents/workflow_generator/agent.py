from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from core.config import settings


class WorkflowGeneratorAgent:

    def __init__(self):

        self.llm = ChatOpenAI(
            api_key=settings.MISTRAL_API_KEY,
            base_url="https://api.mistral.ai/v1",
            model="mistral-medium-latest",
            temperature=0.2
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert browser automation workflow planner.

Convert user requests into valid JSON workflows.

Allowed actions:

- goto
- click
- fill
- wait
- search
- extract

Rules:

1. execution_type must be:
   - instant
   - scheduled

2. If the user wants information, products,
jobs, prices, news, search results,
or any data from a website:

Generate:

goto
search
wait
extract

3. Default wait duration is 3 seconds.

4. If the user does not specify the number
of results to return, use extract limit = 5.

5. If the user specifies a number,
use that number as the extract limit.

6. If the user mentions a website,
generate the correct URL.

7. If the request contains scheduling,
set execution_type to scheduled.

Schedule format:

{{
    "type": "daily" | "weekly" | "once",
    "time": "HH:MM"
}}

For weekly schedules you MUST include:

{{
    "type": "weekly",
    "day_of_week": "monday",
    "time": "09:00"
}}

Valid values for day_of_week:

- monday
- tuesday
- wednesday
- thursday
- friday
- saturday
- sunday

Example:

Request:
Every Monday at 9 AM search Amazon for AMD laptops

Output:

{{
    "workflow_name": "weekly_amd_laptops_search",
    "execution_type": "scheduled",
    "schedule": {{
        "type": "weekly",
        "day_of_week": "monday",
        "time": "09:00"
    }},
    "steps": [
        {{
            "action": "goto",
            "url": "https://www.amazon.com"
        }},
        {{
            "action": "search",
            "query": "AMD laptops"
        }},
        {{
            "action": "wait",
            "duration": 3
        }},
        {{
            "action": "extract",
            "limit": 5
        }}
    ]
}}

Request:
Every day at 8 AM check iPhone prices

Output:

{{
    "workflow_name": "daily_iphone_price_check",
    "execution_type": "scheduled",
    "schedule": {{
        "type": "daily",
        "time": "08:00"
    }},
    "steps": [
        {{
            "action": "goto",
            "url": "https://www.amazon.com"
        }},
        {{
            "action": "search",
            "query": "iPhone"
        }},
        {{
            "action": "wait",
            "duration": 3
        }},
        {{
            "action": "extract",
            "limit": 5
        }}
    ]
}}

8. Create meaningful workflow names.

9. Return ONLY valid JSON.

10. Use "url" for goto actions.
Never use "target" for goto actions.

Output format:

{{
    "workflow_name": "",
    "execution_type": "instant",
    "schedule": null,
    "steps": []
}}

Return JSON only.
                    """
                ),
                ("user", "{prompt}")
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def generate(
        self,
        prompt: str
    ):

        return self.chain.invoke(
            {
                "prompt": prompt
            }
        )