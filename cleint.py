from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
pineconeClient = Pinecone(api_key=os.getenv("pineconeKey"))




openAIClient = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("openRouterKey"),
)