import pytest

from codagent.parser import ModelOutput

def test_parse_action():
    output = """
    <root>
        <thought>I need to read the source file src/main.py</thought>
        <actions>
        [
            {
                "name": "test_action",
                "parameters": {
                    "param1": "value1",
                    "param2": "value2"
                }
            }
        ]
        </actions>
    </root>
    """

    model_output = ModelOutput.from_output(output)
    assert model_output.thoughts[0] == "I need to read the source file src/main.py"
    assert len(model_output.actions) == 1
    assert model_output.actions[0].name == "test_action"
    assert model_output.actions[0].parameters == {"param1": "value1", "param2": "value2"}

if __name__ == "__main__":
    pytest.main()