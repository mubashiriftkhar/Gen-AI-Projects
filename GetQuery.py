import spacy
from state import State

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def getQuery(state:State):

  if state.get("transformedQuery"):
    query = state["transformedQuery"][-1]
  else:     
    query=state['messages'][-1].content
  doc = nlp(query.lower())  # Lowercase before processing
    
  tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
  if state.get("transformedQuery"):
      state["transformedQuery"][-1]=" ".join(tokens)
  else:
     state["originalQuery"]=" ".join(tokens)
     
  return state
   
