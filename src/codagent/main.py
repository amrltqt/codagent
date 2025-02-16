
import os
import sys

from mistralai import Mistral
from rich.console import Console
from rich.syntax import Syntax
from rich.progress import Progress

from codagent import prompts

from codagent.parser import ModelOutput

from codagent.tools.get_directory_structure import get_directory_structure
from codagent.tools.read_source_file import read_source_file
from codagent.tools.update_code_file import update_code_file

from codagent.code_exec import execute_secure_action

# Retrieve the API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]
# Define the model to use
model = "codestral-latest"

# Initialize the Mistral client with the API key
client = Mistral(api_key=api_key)

def execute_query(query: str, history_list: list[str]):
    # Join the history list into a single string
    history = "\n".join(history_list)
    # Send a chat completion request to the Mistral model
    chat_response = client.chat.complete(
        model= model,
        temperature=0,
        messages = [
            {
                "role": "system",
                "content": prompts.SYSTEM_PROMPT % (history, query),
            }
        ]
    )
    # Extract the answer from the chat response
    answer = chat_response.choices[0].message.content
    # Return the parsed model output
    return ModelOutput.from_output(answer)

def main():
    # Get the query from command line arguments
    query = sys.argv.pop(1)

    # Initialize an empty history list
    history = []
    # Initialize the console for output
    console = Console()

    # Loop for a maximum of 5 iterations
    for step_index in range(5):
        console.print(f"[bold green]Step: {step_index}[/bold green]")
        # Execute the query and get the output
        output = execute_query(query, history)

        if output.output is not None:
            console.print(output.output)
            break  # Stop dès qu'un output final est produit

        # Process each thought in the output
        for thought in output.thoughts:
            # Append the thought to the history
            history.append(
                f"<thought>{thought}</thought>\n"
            )
            # Print the thought to the console
            console.print(thought)

        # Process each action in the output
        for action in output.actions:
            # Print the action syntax to the console
            syntax = Syntax(action, "python", theme="monokai", line_numbers=True)
            console.print(syntax)

            result, error_flag = execute_secure_action(action, allowed_globals={
                "get_directory_structure": get_directory_structure,
                "read_source_file": read_source_file,
                "update_source_file": update_code_file,
            })

            if error_flag:
                history.append("<error>true</error>\n")
            
            # Append the result to the history
            history.append(
                f"<action>{action}</action>\n<result>{result}</result>\n"
            )
            # Print the result to the console
            # console.print(result)


if __name__ == "__main__":
    main()
