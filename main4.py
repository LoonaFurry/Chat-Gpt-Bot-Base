import discord
import requests
import openai

openai.api_key = "your-token-here"
openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1/models"

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

model_name = "gpt-3.5-turbo-16k"  # Specify the model name here

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        content = message.content.replace(client.user.mention, "").strip()

        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "prompt": content,
            "max_tokens": 100,
            "n": 1,
            "stop": None,
            "temperature": 0.7,
            "model": model_name  # Specify the model name in the API request
        }

        response = requests.post(f"{openai.api_base}/engines/davinci-codex/completions", headers=headers, json=data)
        response_json = response.json()

        print(response_json)  # Print the response JSON for debugging

        if "choices" in response_json:
            generated_text = response_json["choices"][0]["text"].strip()
            await message.channel.send(generated_text)
        else:
            await message.channel.send("Failed to generate a response.")

client.run("your-token-here")