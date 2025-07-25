from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation"  # ✅ Correct task
)

model1 = ChatHuggingFace(llm=llm)


llm1 = HuggingFaceEndpoint(
    repo_id= "mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation"  # ✅ Correct task
)

model2 = ChatHuggingFace(llm=llm1)

