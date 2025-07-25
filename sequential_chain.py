from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

load_dotenv()

prompt1 = PromptTemplate(
    template = "Generate a detailed report on {topic}",
    input_variables = ['topic']
)

prompt2 = PromptTemplate(
    template = "Generate a 5 ponter summary from the following text \n  {text}",
    input_variables = ['text']
)


llm = HuggingFaceEndpoint(
    repo_id= "mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation"  # ✅ Correct task
)

model = ChatHuggingFace(llm=llm)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic':"unemployment in India"})

print(result)

chain.get_graph().print_ascii()