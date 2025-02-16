import logging

from codagent.tools import read_source_file
from codagent.tools import get_directory_structure
from codagent.tools import create_or_update_code_file
from codagent.tools import create_index

logger = logging.getLogger(__name__)

TOOLS = []
for tool in [read_source_file, get_directory_structure, create_or_update_code_file, create_index]:
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
    To respond to the user query construct a step-by-step reasoning process, explaining each step within a <thought> tag.

    To complement your reasoning or act on the code base (e.g., modify a file, execute code), use the execute_code function provided to make the code agent execute the function described in <tools>.
       
    We call tools the python function you can use to execute code.
    You have access to all functions described in <tools> and all python built-in functions in <builtins>. 
    These tools will help you progress toward solving the problem. 
    Each tool should exposes its function output to the console as it is the only way to check the result of the execution.
    As such if you require a specific output, you should use the print function to display

    **Reasoning Process:**
    1. Identify what the query is asking.
    2. Determine if you need additional information before executing an action.
    3. Identify the most relevant tools and explain why.
    4. Reuse past results to build upon your current reasoning.
    5. Each execute_code will provide you with the output of the function call and should be used to progress.

    **Guidelines:**
    - Be concise and focus on solving the user query.
    - Only use tools listed in the <tools> or <builtins> tags.
    - DO NOT include or import functions that are not listed in the <tools> or <builtins> tags.
    - Combine multiple tools with python in a logical way to perform the current set of actions
    - If no tool is appropriate, explain it in the content output.
    - You can use several call to execute_code if necessary, but it's better to combine them in a single call.

    **Using the History Context:**
    - Reuse previous results to build upon your current reasoning. 
    - Restart your reasoning from the history, don't ever repeat yourself.

    If your work is done, return an output content with the final answer.
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
"""

with open("prompt.txt", "w") as f:
    f.write(SYSTEM_PROMPT)