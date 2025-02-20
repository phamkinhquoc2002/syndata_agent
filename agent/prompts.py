SYSTEM_PROMPT ="""
You are an advanced synthetic data generator, engineered to produce high-quality, task-specific synthetic datasets. Your mission is to generate data samples in formats that precisely adhere to the requirements provided.
"""

SFT = """
You must strictly follow the below format for this task:
[
  {
    "prompt": "Your generated prompt",
    "completion": "Your completion text"
  },
  ...
]

Notes:
- Both "prompt" and "completion" fields must be non-empty.
- Each sample must be a JSON dictionary with two keys: "prompt" and "completion".
"""

DPO = """
You must strictly follow the below format for this task:
[
  {
    "prompt": "Your generated prompt",
    "chosen": "Chosen completion text",
    "rejected": "Rejected completion text"
  },
  ...
]

Notes:
- Both "prompt", "chosen" and "rejected" fields must be non-empty.
- Each sample must be a JSON dictionary with two keys: "prompt" and "completion".
"""

CONVERSATION = """
You must strictly follow the below format for this task:
[
  {
    "dialogue": [
      {
        "role": "user",
        "content": "User message"
      },
      {
        "role": "system",
        "content": "System response"
      },
      ...
    ]
  },
  ...
]

Notes:
- Both "role" and "content" fields must be non-empty.
- Each sample must be a JSON dictionary with a single key: "dialogue".
"""