from langchain.tools import tool 
from data import users_data 
from dotenv import load_dotenv 
import logging 
from objects import PurchaseItem 
from datetime import date 

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

@tool 
def get_user_purchase_history(user:str) -> dict:
    """this tools takes the user name and return a dictionary of what the user purchased"""
    
    logging.info(f"using get_user_purchase_history tool on user:{user}")
    if users_data.get(user):
        return users_data[user]
    return {"status":"there was no username found"}

@tool
def calculate_right_refund(user:str,items:list[PurchaseItem]) -> str:
    """this tools take a list of the items to be returned and the username
    and will return how much the refund is."""
    
    logging.info(f"using calculate_right_refund tool to get the user's : {user} refund amount.")
    
    if users_data.get(user):
        total_refund = 0 
        for item in items:
            if users_data[user].get(item.name):
                total_refund += users_data[user][item.name]["price"]
                
        return f"the value of the refund is : {total_refund}"
    
    return {"status":"there was no username found."}

@tool
def issue_refund_ticket(user:str,refund_amount:int) -> str:
    """this tool will send a ticket to the right team to return the refund."""
    logging.info(f"using issue_refund_ticket tool for user : {user}")
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}."
 
@tool 
def get_today_date(user:str) -> str:
    """This tool will return today's date"""
    logging.info("f using get_today_date tool")
    return date.today()

    
    