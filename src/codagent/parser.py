# This file is used to parse the output of the model.
# It is used to define the functions that will be used to parse the output of the model.


import re

from pydantic import BaseModel

# Extract all occurences of 
# <thought>...</thought>
# <actions>...</actions>
# <output>...</output>
def extract_thoughts(text: str):
    thoughts = re.findall(r"<thought>(.*?)</thought>", text, re.DOTALL)
    actions = re.findall(r"<actions>(.*?)</actions>", text, re.DOTALL)
    output = re.findall(r"<output>(.*?)</output>", text, re.DOTALL)
    return thoughts, actions, output

class ModelOutput(BaseModel):
    thoughts: list[str]
    actions: list[str]
    output: str | None

    @classmethod
    def from_output(cls, input_str: str):
        thoughts = []
        actions = []
        output = None

        ext_thoughts, ext_actions, ext_output = extract_thoughts(input_str)
        thoughts = [thought.strip() for thought in ext_thoughts]
        
        
        if len(ext_actions) > 0:
            actions = ext_actions
    
        if len(ext_output) > 0:
            output = ext_output[0]
        return cls(thoughts=thoughts, actions=actions, output=output)