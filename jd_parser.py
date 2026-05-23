from openai import OpenAI
import json

def parse_jd(jd_text: str) -> dict:
    client = OpenAI(
        api_key="sk-9a1e478270a24ac9af1fab8b7151e2c3",
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are a job application assistant. Return only valid JSON, no explanation or markdown."
            },
            {
                "role": "user",
                "content": f"""Extract key information from the job description below and return in this exact JSON format:
{{
  "company": "company name",
  "position": "job title",
  "requirements": "2-3 sentence summary of core requirements",
  "location": "work location"
}}
If a field is not found, use "Unknown".

Job Description:
{jd_text}"""
            }
        ],
        max_tokens=500
    )

    result_text = response.choices[0].message.content.strip()
    return json.loads(result_text)