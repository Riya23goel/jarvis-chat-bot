from openai import OpenAI
client = OpenAI(
    api_key="API_KEY"
)

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
            {"role": "user", "content": "what is coding"}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("Error:", e)