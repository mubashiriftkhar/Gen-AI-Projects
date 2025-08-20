from state import State
from cleint import openAIClient


def ShowOutput(state:State)->dict:
    if state.get("transformedQuery") and len(state.get("transformedQuery"))<3:
        query = state["transformedQuery"][-1]
    else:
        query = state["originalQuery"]

    all_docs = state.get('retrievedDocs', [])
    if len(all_docs) == 0:
        prompt=f"""Explain this Topic little bit and tell this is irrelevent topic to discuss
        Topic:{query}
        Format the result in Inner HTML using only tags like <h1> to <h6> ,<p>, <strong>, <b>, <ul>, <li> etc., without <html> or <body> tags."""
    else: 
        retrieved_docs = all_docs[-1] if all_docs else []
        prompt = f"""
You are a legal AI assistant.

This is the User's query: "{query}"

These are the Retrieved Documents:
{retrieved_docs}

Step 1: 
  Analyze the Retrieved Documents and give answer to the User's Query from only retrieved Documents.
  Explain the answer according to User's Query.
Step 2:
   After Consing the Results convert the answer into inner html Format.
   Format the result in Inner HTML using only tags like <h1> to <h6> ,<p>, <strong>, <b>, <ul>, <li> etc., without <html> or <body> tags.
"""

   

    # Call OpenAI Chat Completion
    completion = openAIClient.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant that answers queries using retrieved documents."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return the raw HTML content (innerHTML)
    html_content = completion.choices[0].message.content
    return {"finalOutput":html_content}