from state import State
from cleint import openAIClient


def cheakResults(state:State)->dict:
    query = state['originalQuery']
    retrieved_docs = state.get('retrievedDocs', [])

    # Chain-of-thought style prompt
    system_message = (
        "You are an assistant that analyzes retrieved documents for a user's query. "
        "Retrieved Documents are Given to you Your task is to analyze the doucments and decide wheather it is correct for user query or not."
        "Return only 'yes' if the Retrieved Documents has sufficient information about User Query, If Retrieved Documents does not have sufficient information about User Query then Return 'no'."
    )

    user_message = (
        f"User Query: {query}\n\n"
        f"Top Retrieved Documents:\n{retrieved_docs}\n\n"
        "Answer 'yes' or 'no':"
    )

    completion = openAIClient.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    decision=completion.choices[0].message.content
    if 'yes' in decision.lower():
        finalDicision="yes"
    elif 'no' in decision.lower():
        finalDicision="no"

    state["decision"]=finalDicision    
    return state


def route_from_decision(state: State) -> str:
    if len(state.get('transformedQuery', [])) >= 3:
        state["retrievedDocs"].clear()
        return "yes"
    return state["decision"]
    