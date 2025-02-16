# This is a header comment

import os
import sys
import json

from mistralai import Mistral
from rich.console import Console
from rich.syntax import Syntax

from codagent import prompts

from codagent.parser import ModelOutput

from codagent.tools.get_directory_structure import get_directory_structure
from codagent.tools.read_source_file import read_source_file
from codagent.tools.create_or_update_code_file import create_or_update_code_file
from codagent.tools.create_index import create_index

from codagent.code_exec import execute_secure_action

# Retrieve the API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]
# Define the model to use
model = "codestral-latest"
# model = "mistral-large-latest"

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
        else:
            console.print(answer.content)
            break

if __name__ == "__main__":
    main()
