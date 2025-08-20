from langgraph.graph import StateGraph, START, END
from state import State
from GetQuery import getQuery
from Retrieve import Retrieve
from transformQuery import correctQuery
from CheakResult import cheakResults,route_from_decision
from output import ShowOutput
# from internetSearch import SearchInternet
# import time

# start_time = time.time()
# def debug_node(fn):
#     def wrapper(state: State):
#         result = fn(state)
#         print(f"\n--- Node: {fn.__name__} ---")
#         print("Input state:", state)
#         print("Output:", result)
#         print("----------------------------\n")
#         return result
#     return wrapper
def GraphBuilder():
    graphBuilder=StateGraph(State)
    graphBuilder.add_node("Input",getQuery)
    graphBuilder.add_node("Retrieve",Retrieve)
    graphBuilder.add_node("CheakResults",cheakResults)
    graphBuilder.add_node("TransformQuery",correctQuery)
    graphBuilder.add_node("Output",ShowOutput)

    graphBuilder.add_edge(START,"Input")
    graphBuilder.add_edge("Input","Retrieve")
    graphBuilder.add_edge("Retrieve","CheakResults")
    graphBuilder.add_conditional_edges(
        "CheakResults",route_from_decision,
        {
            "no":"TransformQuery",
            "yes":"Output"
        }
    )
    graphBuilder.add_edge("TransformQuery","Input")
    graphBuilder.add_edge("Output",END)
    return graphBuilder.compile()


# graphBuilder=StateGraph(State)
# graphBuilder.add_node("Input",debug_node(getQuery))
# graphBuilder.add_node("Retrieve",debug_node(Retrieve))
# graphBuilder.add_node("CheakResults",debug_node(cheakResults))
# # graphBuilder.add_node("InternetSearch",debug_node(SearchInternet))
# graphBuilder.add_node("TransformQuery",debug_node(correctQuery))
# graphBuilder.add_node("Output",debug_node(ShowOutput))

# graphBuilder.add_edge(START,"Input")
# graphBuilder.add_edge("Input","Retrieve")
# graphBuilder.add_edge("Retrieve","CheakResults")
# # Conditional edge for CheakResults
# graphBuilder.add_conditional_edges(
#     "CheakResults",route_from_decision,
#     {
#         "no": "TransformQuery",
#         "yes": "Output"
#     }
# )

# # Conditional edge for TransformQuery based on loop count
# def transform_query_condition(state: State) -> str:
#     if len(state.get('transformedQuery', [])) >= 3:
#         return "Output"
#     return "transformedQuery"

# graphBuilder.add_conditional_edges(
#     "CheakResults",
#     transform_query_condition,
#     {
#         "Output": "Output",
#         "transformedQuery": "transformedQuery"
#     }
# )
# graphBuilder.add_edge("TransformQuery","Input")
# graphBuilder.add_edge("InternetSearch", "Output")
# graphBuilder.add_edge("Output",END)

# graph=graphBuilder.compile()

# test_state= {
#     "messages": [
#         {"role": "user", "content": "Machine learning methods for legal information retrieval"}
#     ],
#     "originalQuery": "",
#     "transformedQuery": [],
#     "retrievedDocs": [],
#     "finalOutput": ""
# }

# final_state = graph.invoke(input=test_state)
# print("originalQuery", final_state['originalQuery'])
# print("transformedQuery", final_state['transformedQuery'])
# print("retrievedDocs", final_state['retrievedDocs'])
# print("finalOutput", final_state['finalOutput'])

# end_time = time.time()  # Record end time
# elapsed_time = end_time - start_time
# print(f"Time taken: {elapsed_time:.4f} seconds")
# with open("graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())