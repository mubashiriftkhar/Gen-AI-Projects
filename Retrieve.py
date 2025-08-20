from state import State
from cleint import pineconeClient




dense_index = pineconeClient.Index(host="https://legal-tech-dense-for-hybrid-search-crs8ha4.svc.aped-4627-b74a.pinecone.io")
sparse_index =pineconeClient.Index(host="https://legal-tech-sparse-for-hybrid-search-crs8ha4.svc.aped-4627-b74a.pinecone.io")
def Retrieve(state:State)->dict:
    if state.get("transformedQuery"):
        query = state["transformedQuery"][-1]
    else:
        query = state["originalQuery"]

    dense_results = dense_index.search(
    namespace="all-over-world",
    query={
        "top_k": 10,
        "inputs": {
            "text": query
        }
    }
)
    sparse_results = sparse_index.search(
    namespace="all-over-world",
    query={
        "top_k": 10,
        "inputs": {
            "text": query
        }
    }
)

    merged_results = merge_chunks(sparse_results, dense_results)
    reranked_docs = Rerank(query, merged_results)
    state['retrievedDocs'].append(reranked_docs)
    return {
        "state": state,
        "retrievedDocs":reranked_docs
        }


def merge_chunks(h1, h2):
    """Get the unique hits from two search results and return them as single array of {'_id', 'text'} dicts, printing each dict on a new line."""
    deduped_hits = {hit['_id']: hit for hit in h1['result']['hits'] + h2['result']['hits']}.values()
    sorted_hits = sorted(deduped_hits, key=lambda x: x['_score'], reverse=True)
    result = [{'_id': hit['_id'], 'chunk_text': hit['fields']['text']} for hit in sorted_hits]
    return result


def Rerank(query,merged_results):
    docs=[]
    result = pineconeClient.inference.rerank(
        model="bge-reranker-v2-m3",
        query=query,
        documents=merged_results,
        rank_fields=["chunk_text"],
        top_n=5,
        return_documents=True,
        parameters={
            "truncate": "END"
        }
    )
    for row in result.data:
        docs.append(row['document']['chunk_text'])
    return docs

