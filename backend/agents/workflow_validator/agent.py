from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from core.config import settings


class WorkflowValidatorAgent:

    def __init__(self):

        self.llm = ChatOpenAI(
            api_key=settings.MISTRAL_API_KEY,
            base_url="https://api.mistral.ai/v1",
            model="mistral-medium-latest",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a workflow validation agent.

Validate the workflow JSON.

Checks:

1. workflow_name exists.

2. execution_type exists and is:
   - instant
   - scheduled

3. steps exists and contains at least
   one action.

4. Allowed actions:

   - goto
   - click
   - fill
   - wait
   - search
   - extract

5. If execution_type is scheduled,
   schedule must exist.

6. If action is goto,
   url must exist.

7. If action is search,
   query must exist.

8. If action is fill,
   selector and value must exist.

9. If action is click,
   selector must exist.

10. If action is wait,
    duration must exist.

11. If action is extract and limit
    is missing, automatically set:

    {{
        "limit": 5
    }}

12. Fix minor issues if possible.

Return ONLY JSON.

Format:

{{
    "valid": true,
    "message": "",
    "workflow": {{}}
}}
                    """
                ),
                ("user", "{workflow}")
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | JsonOutputParser()
        )

    def validate(
        self,
        workflow: dict
    ):

        return self.chain.invoke(
            {
                "workflow": workflow
            }
        )