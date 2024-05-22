import logging

import openai
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

from utils.evaluation import static_essay_assessment_criteria

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))


async def evaluate_document_stream(subject, file_content):
    if subject == "Essay-Writing":
        return evaluate_essay_stream(file_content)
    else:
        return evaluate_subject_stream(subject, file_content)

# def evaluate_document(subject, file_content):
#     if subject == "Essay Writing":
#         return evaluate_essay(file_content)
#     else:
#         return evaluate_subject(subject, file_content)


async def evaluate_essay_stream(content):
    prompt = (f"Evaluate this essay based on the following criteria: {static_essay_assessment_criteria()} \n\n"
              f"Essay: {content}"
              f"\n\n"
              f"Towards the end give a 'Overall Rating' based on the evaluation criteria. It should be out of 5"
              f"It should clearly say something like Final Rating 4.5/5 under a separate heading 'Overall Rating'"
              )
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an essay evaluator."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    async for chunk in stream:
        yield chunk.choices[0].delta.content

# def evaluate_essay(content):
#     prompt = f"Evaluate this essay based on the following criteria: {static_assessment_criteria()} \n\nEssay: {content}"
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are an essay evaluator."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message['content']


async def evaluate_subject_stream(subject, content):
    prompt = f"Evaluate this {subject} document based on predefined rubric metrics. \n\nDocument: {content}"
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a {subject} evaluator."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    async for chunk in response:
        yield chunk['choices'][0]['delta']['content']


def evaluate_subject(subject, content):
    prompt = f"Evaluate this {subject} document based on predefined rubric metrics. \n\nDocument: {content}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a {subject} evaluator."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']
