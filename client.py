from openai import OpenAI

client = OpenAI(
    api_key="Use your API Key here",
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="Llama-4-Maverick-17B-128E-Instruct",
    messages=[{"role":"user","content":[{"type":"text","text":"What do you see in this image"},{"type":"image_url","image_url":{"url":"<image_in_base_64>"}}]}],
    temperature=0.1,
    top_p=0.1
)


print(response.choices[0].message.content)
