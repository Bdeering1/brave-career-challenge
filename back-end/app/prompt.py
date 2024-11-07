from app import config
from pydantic import BaseModel
from openai import OpenAI


class SurveyQuestion(BaseModel):
    prompt: str
    options: list[str]


def get_question(name, description):
    client = OpenAI(
        organization=config.ORGANIZATION_ID,
        project=config.PROJECT_ID,
        api_key=config.OPENAI_API_KEY
    )

    main_prompt = f'Please generate a multiple choice question with 4 options that could be used to classify visitors of the {name} site based on their interest or industry. '
    desc_prompt = f'The site is self described as follows: {description}. '
    detail = f'Please make the question specifically relevant to {name}, the goal is to classify the intent of their visitors.'

    system_prompt = 'You are an expert customer demographic analyst.'
    user_prompt = f'{main_prompt}{desc_prompt if len(description) != 0 else ''}{detail}'

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format=SurveyQuestion
    )

    return completion.choices[0].message.parsed
