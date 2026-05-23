from openai import OpenAI
import json
import os

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", "sk-9a1e478270a24ac9af1fab8b7151e2c3"),
    base_url="https://api.deepseek.com"
)

def skill_parse_jd(jd_text: str) -> dict:
    """Skill 1: 结构化解析JD"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are a job description analyst. Return only valid JSON, no explanation or markdown. All values must be in English."
            },
            {
                "role": "user",
                "content": f"""Analyze this job description and extract structured information. Return this exact JSON format:
{{
  "company": "company name",
  "position": "job title",
  "location": "work location",
  "skills_required": ["skill1", "skill2", "skill3"],
  "priority_requirements": "top 2-3 must-have requirements in one sentence",
  "hidden_signals": "subtle culture hints implied in the JD, e.g. fast-paced, no hand-holding, self-starter",
  "risk_flags": "ambiguous or concerning points worth clarifying before applying"
}}

Job Description:
{jd_text}"""
            }
        ],
        max_tokens=800
    )
    result_text = response.choices[0].message.content.strip()
    result_text = result_text.replace("```json", "").replace("```", "").strip()
    return json.loads(result_text)


def skill_action_plan(jd_text: str) -> dict:
    """Skill 2: 生成可执行建议"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are a career coach. Return only valid JSON, no explanation or markdown. All values must be in English."
            },
            {
                "role": "user",
                "content": f"""Based on this job description, generate a concrete action plan for the applicant. Return this exact JSON format:
{{
  "what_to_prepare": ["specific thing 1", "specific thing 2", "specific thing 3"],
  "what_to_emphasize": "what skills or experiences to highlight in the application",
  "questions_to_ask": ["smart question 1", "smart question 2"],
  "gap_warning": "what the applicant might be missing based on the JD"
}}

Job Description:
{jd_text}"""
            }
        ],
        max_tokens=800
    )
    result_text = response.choices[0].message.content.strip()
    result_text = result_text.replace("```json", "").replace("```", "").strip()
    return json.loads(result_text)


def parse_jd(jd_text: str) -> dict:
    """合并两个Skill的结果"""
    parsed = skill_parse_jd(jd_text)
    action = skill_action_plan(jd_text)
    return {**parsed, **action}