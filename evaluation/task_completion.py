
import sys
from pathlib import Path
from uuid import uuid4

# Add the agent directory to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = PROJECT_ROOT / "agent"

sys.path.insert(0, str(AGENT_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import agent
from dataset import dataset
from groq_judge import eval_model

from deepeval.metrics import TaskCompletionMetric
from deepeval.integrations.langchain import CallbackHandler


SUCCESSFUL_TASK_DESCRIPTION = """
To be successful, the agent must follow these rules:

1. If the user has not provided a username, ask for it before proceeding.
   Do not perform refund actions before identifying the user.

2. If the user provides a username and requests a refund:
   - Check whether the purchase was made within the last 30 days.
   - Refund only the items requested by the user, not all items unless requested.
   - Refund only items actually purchased by that user.

3. Once the required information is available, communicate the refund
   ticket status to the identified user:
   - A refund was issued; or
   - A refund was not issued, with the reason explained.

4. For requests unrelated to refunds, such as asking for information,
   the task is successful if no refund ticket is issued.

5. Never issue a refund before identifying the user and validating
   the applicable purchase and refund conditions.
"""


# Confirm that the custom Groq judge is being used.
print("Judge class:", type(eval_model))
print("Judge model:", eval_model.get_model_name())
print("Judge module:", type(eval_model).__module__)


metrics = [
    TaskCompletionMetric(
        threshold=0.8,
        model=eval_model,
        task=SUCCESSFUL_TASK_DESCRIPTION,
        include_reason=True,
    )
]


for index, golden in enumerate(dataset.evals_iterator(metrics=metrics)):
    print(f"Completed evaluation case {index + 1}")

    # Use a unique thread ID for every test case.
    thread_id = f"refund-eval-{uuid4()}"

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": golden.input,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            },
            "callbacks": [
                CallbackHandler(),
            ],
        },
    )

    print("Agent response:", response)
