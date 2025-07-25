from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = PromptTemplate(
    template = 'Generate 5 interesting facts about {topic}',
    input_variables = ['topic']
)

llm = HuggingFaceEndpoint(
    repo_id= "mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation"  # ✅ Correct task
)

model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic":"cricket"})

print(result)

chain.get_graph().print_ascii()