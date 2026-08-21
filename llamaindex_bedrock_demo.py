from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.bedrock import Bedrock
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 🔹 Set local embedding model

# 🔹 Bedrock LLM
llm = Bedrock(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1"
)

documents = SimpleDirectoryReader("data").load_data()
print("\n Loaded Documents:\n", documents)
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(llm=llm)

query = input("Ask something: ")
response = query_engine.query(query)

print("\n Answer:\n")
print(response)