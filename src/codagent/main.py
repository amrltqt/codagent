# This file is the entry point of the codagent application.
# It is used to define the main function that will be executed when the application is run.

import re
import os
import sys
import json

import requests
from mistralai import Mistral
from rich.console import Console
from rich.syntax import Syntax
from duckduckgo_search import DDGS
from markdownify import markdownify

from codagent import prompts

from codagent.tools.get_directory_structure import get_directory_structure
from codagent.tools.read_source_file import read_source_file
from codagent.tools.create_or_update_code_file import create_or_update_code_file
from codagent.tools.create_index import create_index

from codagent.code_exec import execute_secure_action

# Retrieve the API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]
# Define the model to use
# model = "codestral-latest"
model = "mistral-large-latest"

# Initialize the Mistral client with the API key
client = Mistral(api_key=api_key)


def main():
    # Get the query from command line arguments
    query = sys.argv.pop(1)

    # Initialize the console for output
    console = Console()

    messages = [
        {
            "role": "system",
            "content": prompts.SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": query,
        }
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "execute_code",
                "description": "Execute a piece of Python code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Code to be executed",
                        }
                    },
                },
                "required": ["code"],
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_on_internet",
                "description": "Search by keywords on the internet",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "Keywords to search for",
                        }
                    },
                },
                "required": ["keywords"],
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_webpage_content",
                "description": "Get the content of a webpage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the webpage",
                        }
                    },
                }
            }
        }
    ]


    # Loop for a maximum of 5 iterations
    for step_index in range(10):
        console.print(f"[bold green]Step: {step_index}[/bold green]")
        # Execute the query and get the output
        # Send a chat completion request to the Mistral model
        chat_response = client.chat.complete(
            model=model,
            temperature=0,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        answer = chat_response.choices[0].message

        if answer.tool_calls  and len(answer.tool_calls) > 0:
            messages.append(answer)
            for tool_call in answer.tool_calls:
                id = tool_call.id
      
                if tool_call.function.name == "execute_code":

                    code = json.loads(tool_call.function.arguments)["code"]

                    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
                    console.print(syntax)

                    result, error_flag = execute_secure_action(code, allowed_globals={
                        "get_directory_structure": get_directory_structure,
                        "read_source_file": read_source_file,
                        "create_or_update_code_file": create_or_update_code_file,
                        "create_index": create_index,
                    })

                    console.print(result)

                    messages.append({
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": result,
                        "tool_call_id": id,
                    })
                elif tool_call.function.name == "search_on_internet":
                    keywords = json.loads(tool_call.function.arguments)["keywords"]

                    console.print(f"Searching the internet for: {keywords}")
                    results = DDGS().text("python programming", max_results=5)
                    postprocessed_results = [f"[{result['title']}]({result['href']})\n{result['body']}" for result in results]
                    messages.append({
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": "## Search Results\n\n" + "\n\n".join(postprocessed_results),
                        "tool_call_id": id,
                    })

                elif tool_call.function.name == "get_webpage_content":
                    url = json.loads(tool_call.function.arguments)["url"]

                    console.print(f"Getting the content of the webpage: {url}")
            
                    response = requests.get(url, timeout=20)
                    response.raise_for_status()

           
                    markdown_content = markdownify(response.text).strip()
                    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
                    
                    messages.append({
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": markdown_content[:10000],
                        "tool_call_id": id,
                    })
        else:
            console.print(answer.content)
            break

if __name__ == "__main__":
    main()
