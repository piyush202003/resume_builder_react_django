import json

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

def ai_upload_resume(resume_text):

    system_prompt = """
    You are an expert AI agent that extracts structured information
    from resumes.

    Extract the resume into the following JSON structure:

    {
        "personal_info": {
            "full_name": "",
            "profession": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "website": ""
        },
        "professional_summary": "",
        "skills": [
            {
                "type": ""
            }
        ],
        "experiences": [
            {
                "company": "",
                "position": "",
                "start_date": null,
                "end_date": null,
                "description": "",
                "is_current": false
            }
        ],
        "projects": [
            {
                "name": "",
                "project_type": "",
                "description": "",
                "github_url": "",
                "live_url": ""
            }
        ],
        "educations": [
            {
                "institution": "",
                "degree": "",
                "field": "",
                "start_date": null,
                "graduation_date": null,
                "gpa": ""
            }
        ]
    }

    Rules:
    - Return ONLY valid JSON.
    - Do not invent information.
    - Use null when a date is not available.
    - Use empty strings when optional text is not available.
    - Return skills as an array.
    - Return experiences as an array.
    - Return projects as an array.
    - Return educations as an array.
    """
    user_prompt = f'extract data from this resume: {resume_text}'

    response = client.chat.completions.create(
        model=gemini_model,
        messages=[
            {
                "role": 'system', "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format= {"type": 'json_object'}
    )
    
    return json.loads(response.choices[0].message.content)