from openai import OpenAI
from dotenv import load_dotenv
import json


load_dotenv()

client = OpenAI() 


def get_weather(city: str) -> str:
  return "31 degree celsius, sunny"


system_prompt = """ 
You are a helpful AI Assistant who is specilized in resolving user query.
You work on start, plan, action observe mode.
For the given user query and available tools, plan  the step by step execution , based on the planning, select the relevent tool from the available tools. ans based on the tool selection you perform an action to call the tool.
Wait for the observation and based on the oberservation from the tool call resolve the user query.

Rules:
- Follow the steps strictly in the order: plan -> action -> observe -> output
- Use the available tools only.
- Always provide the final answer in the output step.
- Do not skip any steps.
- Always think about the user query before planning.

Output JSON Format:

{{
  "step": "plan",
  "content": "string",
  "function": "The name of the function to call, if the step is action",
  "input" : " The input parameters for the function,
}}
Example:
user Query: Whta is the weather in New York City?
Output: {{ "step" : "plan", "content": "The user is interested in weather data of new york city."}}
Output: {{ "step" : "plan", "content": "From the available tools I should call get_weather "}}
Output: {{ "step" : "action", "function": "get_weather", "input" : "New York "}}
Output: {{ "step" : "observe", "output": "12 degree celsius, cloudy"}}
Output: {{ "step" : "output", "content": "The current weather in New York City is 12 degree celsius and cloudy."}}


"""


response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": "What is the current weather of Berani?"},
      
      # Assistant Response:
      {"role": "assistant", "content" : json.dumps({ "step" : "plan", "content": "The user is interested in the current weather of Berani, which requires accessing weather data."})},
      {"role": "assistant", "content" : json.dumps({"step": "plan", "content": "From the available tools, I should call get_weather to retrieve the current weather information for Berani."})},
      {"role": "assistant", "content" : json.dumps({"step": "action", "function": "get_weather", "input": "Berani"})},
      {"role": "assistant", "content" : json.dumps({"step": "observe", "output": "31 degree celsius, sunny"})},
      
      
    ]
)


print(response.choices[0].message.content)