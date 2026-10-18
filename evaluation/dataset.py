from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall

dataset = EvaluationDataset(
    goldens = [
        Golden(
            input = "I am user123, I would like a refund for the book and the pen",
            expected_output = "A refund ticket for 30$ has been issued successfully",
            expected_tools = [
                ToolCall(name = "get_user_purchase_history"),
                ToolCall(name = "calculate_right_refund"),
                ToolCall(name = " issue_refund_ticket"),
                ToolCall(name = "get_today_date")
            ]
        ),
        Golden(
            input = "I am user123, I would like a refund for the book",
            expected_output = "A refund ticket for 23$ has been issued successfully",
            expected_tools = [
                    ToolCall(name = "get_user_purchase_history"),
                    ToolCall(name = "calculate_right_refund"),
                    ToolCall(name = " issue_refund_ticket"),
                    ToolCall(name = "get_today_date")
                    ]
                ),
        Golden(
            input = "I am user123, I would like no refund,, I just want to know what I purchased",
            expected_output = "No refund tickets has been issued, only a list of items they purchased",
            expected_tools = [
                    ToolCall(name = "get_user_purchase_history"),
                    ]
                ),
        Golden(
            input = "I am user999, I would like a refund for the book",
            expected_output = "No username was found in that name and ask for a username again before proceeding for refund",
            expected_tools = [
                    ToolCall(name = "get_user_purchase_history"),
                    ]
                ),
        Golden(
            input = "I am user126, I would like a refund for water bottle",
            expected_output = "No refund given because it has been more than 30 days of purchase",
            expected_tools = [ 
                    ToolCall(name = "get_user_purchase_history"),
                    ToolCall(name = "get_today_date")
                    ]
                ),
        Golden(
            input = "I am user126, I would like a refund for the backpack and water bottle",
            expected_output = "A refund ticket for 45$ has been issued successfully only for backpack. The water bottle is not elligble for refund because it has been more than 30 days since purchased",
            expected_tools = [
                    ToolCall(name = "get_user_purchase_history"),
                    ToolCall(name = "calculate_right_refund"),
                    ToolCall(name = " issue_refund_ticket"),
                    ToolCall(name = "get_today_date")
                    ]
                ),
        Golden(
            input = "I am user126, I would like a refund for the sneakers",
            expected_output = "The customer didn't purchase sneakers so no refund is given",
            expected_tools = [
                    ToolCall(name = "get_user_purchase_history"),
                    ]
                ),
        
    ]
)