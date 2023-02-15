import openai
import settings

openai.api_key = settings.OPENAI_API_KEY


def chat_gpt(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.4,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.4,
        presence_penalty=0.2,
    )
    answer = response['choices'][0]['text']
    return answer
