from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate
)
from langchain_core.output_parsers import (
    StrOutputParser
)

from core.config import settings


class ResultFormatterAgent:

    def __init__(self):

        self.llm = ChatOpenAI(
            api_key=settings.MISTRAL_API_KEY,
            base_url="https://api.mistral.ai/v1",
            model="mistral-medium-latest",
            temperature=0.1
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert data analyst.

Your job is to analyze browser automation
results and present them in a concise,
human-friendly format.

Rules:

1. Focus only on information relevant
to the user's request.

2. Ignore:
   - navigation menus
   - headers
   - footers
   - ads
   - irrelevant page text

3. Summarize findings clearly.

4. If products are found:
   - list the most relevant ones
   - mention prices if available

5. If jobs are found:
   - list job titles
   - company names
   - locations

6. If no useful information exists,
say so clearly.

Return readable markdown.
                    """
                ),
                (
                    "user",
                    """
User Request:
{user_prompt}

Workflow Name:
{workflow_name}

Raw Results:
{results}
                    """
                )
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def format(
        self,
        user_prompt: str,
        workflow_name: str,
        results: str
    ):

        return self.chain.invoke(
            {
                "user_prompt": user_prompt,
                "workflow_name": workflow_name,
                "results": results
            }
        )