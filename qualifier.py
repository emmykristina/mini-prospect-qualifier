from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os


load_dotenv()


class CompanyQualification(BaseModel):
    description: str
    industry: str
    company_size: str
    outreach_score: int = Field(ge=1, le=5)
    reason: str


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def qualify_company(text):
    prompt = f"""
    Analyze the company based only on the homepage text below.

    Return:
    - what the company does in one sentence
    - industry
    - estimated company size
    - a score from 1 to 5 for how likely the company is to buy LinkedIn outreach services
    - a one-line reason for the score

    Homepage text:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CompanyQualification,
        ),
    )

    return CompanyQualification.model_validate_json(response.text)