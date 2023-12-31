import openai
import constants
#import os
#from dotenv import load_dotenv
from dotenv import dotenv_values

#load_dotenv()
config = dotenv_values(".env")

openai.api_key = config['openai_key']

messages = [
  {"role": "system", "content": constants.sys_content},
]

def ai_chat(content):
  messages.append({"role": "user", "content": content})
  completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=500, temperature=0.4)
  #completion = openai.ChatCompletion.create(model="gpt-4", messages=messages, max_tokens=500, temperature=0.6)
  response = completion.choices[0].message.content
  messages.append({"role": "assistant", "content": response})
  return response

def ai_img(content):
  completion = openai.Image.create(prompt=content, n=1, size="1024x1024")
  response = completion['data'][0]['url']
  return response