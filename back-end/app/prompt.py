from app import config
from app.db import SurveyQuestion
from openai import OpenAI


def get_question(name, description, offerings):
    client = OpenAI(
        organization=config.ORGANIZATION_ID,
        project=config.PROJECT_ID,
        api_key=config.OPENAI_API_KEY
    )

    main_prompt = f"Please generate a multiple choice question with 4 options that could be used to classify visitors of the '{name}' site based on their interest or industry. "
    desc_prompt = '' if len(description) == 0 else f'The site is self described as follows: "{description}" '
    offerings_prompt = ''if len(offerings) == 0 else f'Some of the products/services offered by this site include: {', '.join(offerings)}. '
    detail = f'Please make the question specifically relevant to {name}, feel free to use prior knowledge to make the question more targeted.'

    system_prompt = 'You are an expert customer demographic analyst.'
    user_prompt = f'{main_prompt}{desc_prompt}{offerings_prompt}{detail}'

    print(f'AI Prompt:\n{user_prompt}', flush=True)

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
