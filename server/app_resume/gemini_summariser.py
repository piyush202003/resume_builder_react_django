from urllib import response

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url=os.environ.get("GEMINI_BASE_URL")
)
gemini_model = os.environ.get('GEMINI_MODEL')

def ai_professional_summary(user_content):
    response = client.chat.completions.create(
        model=gemini_model,
        messages=[
            {   "role": "system",
                "content": "You are an expert in resume writing. Your task is to enhance the professional summary of a resume. The summary should be 1-2 sentences also highlighting key skills, experience, and career objectives. Make it compelling and ATS-friendly. and only return text no options or anything else."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    )

    return response.choices[0].message.content

def ai_job_description(user_content):
    response = client.chat.completions.create(
        model=gemini_model,
        messages=[
            {
                "role": 'system', "content":'You are an expert in resume writing. Your task is to enhance the job description of a resume. The job description should be only in 1-2 sentence also highlighting key responsibilities and achievements. Use action verbs and quantifiable results where possible. Make it ATS-friendly. and return text no options or anything else.'
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    )

    return response.choices[0].message.content