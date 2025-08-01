from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableParallel,RunnableBranch,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv imoport load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Literal

load_dotenv()

LLM = HuggingFaceEndpoint(
  repo_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  task = 'text-generation'
)

model = ChatHuggingFace(llm = llm)

parser1 = StrOutputParser()

class Feedback(BaseModel):
  sentiment : Literal['positive','negative'] = Field(description = 'give the sentiment of the feedback')
  
parser2 = PydanticOutputParser(pydantic_object = Feedback)                                                   

prompt1 = PromptTemplate(
  template = 'Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instruction}',
  input_variables = ['feedback'],
  partial_variables = {"format_instruction":parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser2

# result = classifier_chain.invoke({"feedback":"this is a terrible smartphone"})   # -ve

# result = classifier_chain.invoke({"feedback":"this is a wonderful smartphone"}).sentiment   # +ve

# print(result)

prompt2 = PromptTemplate(
  template = 'Write an appropriate response to this positive feedback \n {feedback}',
  input_variable = ['feedback']
)

prompt3 = PromptTemplate(
  template = 'Write an appropriate response to this negative feedback \n {feedback}',
  input_variable = ['feedback']
)

branch_chain = RunnableBranch(
  (lambda x:x.sentiment == 'positive', prompt2 | model | parser1),
  (lambda x:x.sentiment == 'negative',prompt3 | model | parser1),
  RunnableLambda(lambda x:"could not find the sentiment")
)


chain = classifier_chain | branch_chain

print(chain.invoke({"feedback":"this is a terrible phone"}))

chain.get_graph().print_ascii()

