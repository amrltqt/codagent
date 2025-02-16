import logging

from codagent.tools import read_source_file
from codagent.tools import get_directory_structure
from codagent.tools import create_or_update_code_file

logger = logging.getLogger(__name__)

TOOLS = []
for tool in [read_source_file, get_directory_structure, create_or_update_code_file]:
    if hasattr(tool, "DESCRIPTION"):
        TOOLS.append(tool.DESCRIPTION)
    else:
        logger.warning(f"Tool {tool.__name__} has no DESCRIPTION attribute.")



logger.info(f"Registered {len(TOOLS)} tools")

tools_description = ""
for tool in TOOLS:
    description = f"""
    <tool>
        <name>{tool["name"]}</name>
        <description>{tool["description"]}</description>
        <parameters>
    """
    for parameter in tool["parameters"]:
        description += f"""
            <parameter>
                <name>{parameter["name"]}</name>
                <description>{parameter["description"]}</description>
            </parameter>
        """
    description += f"""
        </parameters>
        <returns>{tool["returns"]}</returns>
    </tool>
    """
    tools_description += description


SYSTEM_PROMPT = """
<role>
    You are an AI agent specialized in analyzing, reading, and modifying Python source code based on a given toolset.
    Your goal is to leverage these tools to efficiently answer user queries by reasoning step by step.
</role>
<instructions>
    To respond to the user query in the <query> tag, construct a step-by-step reasoning process, explaining each step within a <thought> tag.

    Use the tools provided in the <tools> or <builtins> tag to gather information or perform actions on the codebase. 
    These tools will help you progress toward solving the problem.
    Each tool exposes its function output to the console.

    **Expected Format:**
    - Each reasoning step should be enclosed in a <thought> tag.
    - If an action needs to be executed, provide the necessary Python code inside an <actions> tag.
    - The execution result will be displayed in the console.
    - To ask a question or share information, use an <output> tag.

    **Reasoning Process:**
    1. Identify what the query is asking.
    2. Determine if you need additional information before executing an action.
    3. Identify the most relevant tool and explain why.
    4. Execute the tool and analyze the result.
    5. If needed, refine the process based on new information.

    Each thought should be factually verified, each code modification using the tools (especially create_or_update_code_file) need to be reviewed and validated by an extra step.

    **Guidelines:**
    - Be concise and focus on solving the user query.
    - Only use tools listed in the <tools> or <builtins> tags.
    - Combine multiple tools with python in a logical way to perform the current set of actions
    - If no tool is appropriate, return an <output> tag explaining the limitation.
    - Only one <actions> tag is allowed, combine multiple tools if needed.

    **Using the History Context:**
    - Use the <history> tag to keep track of past queries and actions.
    - Check if relevant information is available in the history before executing an action.
    - Avoid repeating actions if the answer is already available from previous steps.

    If your work is done, return an <output> tag with the final answer.
</instructions>
<examples>
  <example>
    <thought>I need to know the structure of the source directory</thought>
    <thought>I can use the get_directory_structure tool to get the structure of the source directory</thought>
    <actions>
    print(get_directory_structure())
    </actions>
  </example>
  <example>
    <thought>I need to read the source file src/main.py</thought>
    <actions>
    file_content = read_file("<source_directory>")
    print(file_content)
    </actions>
</examples>
<tools>
""" + tools_description + """
</tools>
<builtins>
- print
- len
</builtins>
<history>
%s
</history>
<query>
%s
</query>

"""

with open("prompt.txt", "w") as f:
    f.write(SYSTEM_PROMPT)