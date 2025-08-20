from state import State
from cleint import openAIClient


def correctQuery(state:State)->dict:
    if state.get("transformedQuery"):
        query = state["transformedQuery"][-1]
    else:
        query = state["originalQuery"]

    # Build the CoT prompt
    prompt = f"""
You are an expert legal information retrieval assistant.
Your task is to take the following user query and transform it
into a more precise, normalized, and semantically rich query
for better hybrid search results. Follow these steps:

1. Analyze the original query and understand its intent.
2. Identify key legal concepts, entities, and actions.
3. Remove unnecessary words but keep numbers and legal references.
4. Keep the language formal and precise for document retrieval.
5. Provide the final query in a single line.

Query: "{query}"
Transformed Query:"""

    # Generate the transformed query
    response = openAIClient.chat.completions.create(
        model="google/gemma-3n-e4b-it:free",
        messages=[
            # {"role": "system", "content": "You are a legal AI query transformer."},
            {"role": "user", "content": prompt}
        ]
    )

    transformed_query = response.choices[0].message.content.strip()

    # Update the state
    state['transformedQuery'].append(transformed_query)
    state["retrievedDocs"].clear()
    state['decision']=''
    return state
        # "transformedQuery": transformed_query
    