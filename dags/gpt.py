import openai
import json

openai.api_key = "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"

def analyze_text_with_gpt(content, domain):
    messages = [
        {"role": "system", "content": "Analyze the following text from the website and extract the company's name and any additional valuable information. Return the results in JSON format with keys 'name' and 'additional_info'."},
        {"role": "user", "content": content}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    gpt_response = response.choices[0].message['content'].strip()

    try:
        response_data = json.loads(gpt_response)
        result = {
            "domain": domain,
            "name": response_data.get("name", ""),
            "additional_info": response_data.get("additional_info", "")
        }
    except json.JSONDecodeError:
        result = {
            "domain": domain,
            "name": "",
            "additional_info": ""
        }

    return result