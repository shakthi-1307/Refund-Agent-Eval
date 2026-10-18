from pydantic import BaseModel,Field

class Answer(BaseModel):
    answer:str = Field(description="the answer for the user query")
    conversation:bool = Field(description="the agent decides whether to continue the conversation or not",default = True)
    
class PurchaseItem(BaseModel):
    name:str = Field(description="name of the item purchased") 
    