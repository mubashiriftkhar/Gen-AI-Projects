from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from graph import GraphBuilder
import time
import random




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    app.state.graph = GraphBuilder()  # compile your LangGraph once
    print("Graph initialized, LLM client ready")
    yield
    # Shutdown code
    print("Shutting down app...")

app = FastAPI(lifespan=lifespan)
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    query: str

def generate_html_response(query: str) -> str:
    """Simulate generating a research report in HTML format"""
    
    # Simulate processing time (1-3 seconds)
    time.sleep(random.uniform(1, 3))
    
    # This would be replaced by your actual research agent logic
    # For demo purposes, we return simulated HTML content
    return f"""
        <h1>Market Research Report: {query}</h1>
        
        <div class="bg-slate-800/50 p-4 rounded-xl my-4">
            <h2>Executive Summary</h2>
            <p>Based on our comprehensive analysis of the market for {query}, we've identified significant growth opportunities and competitive dynamics.</p>
        </div>
        
        <h2>Key Findings</h2>
        <ul>
            <li><strong>Market Size:</strong> Estimated at $12.5B in 2023, projected to reach $18.7B by 2028</li>
            <li><strong>Growth Rate:</strong> CAGR of 8.4% over the next 5 years</li>
            <li><strong>Key Players:</strong> Company A (22% share), Company B (18% share), Company C (15% share)</li>
            <li><strong>Consumer Trends:</strong> Increasing demand for sustainable options and premium features</li>
        </ul>
        
        <h2>Competitive Analysis</h2>
        <div class="overflow-x-auto my-4">
            <table class="min-w-full bg-slate-800/50 rounded-xl">
                <thead>
                    <tr>
                        <th class="py-2 px-4 border-b border-slate-700">Company</th>
                        <th class="py-2 px-4 border-b border-slate-700">Market Share</th>
                        <th class="py-2 px-4 border-b border-slate-700">Key Strengths</th>
                        <th class="py-2 px-4 border-b border-slate-700">Growth Strategy</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="py-2 px-4 border-b border-slate-700">Company A</td>
                        <td class="py-2 px-4 border-b border-slate-700">22%</td>
                        <td class="py-2 px-4 border-b border-slate-700">Brand recognition, Distribution network</td>
                        <td class="py-2 px-4 border-b border-slate-700">Product diversification, International expansion</td>
                    </tr>
                    <tr>
                        <td class="py-2 px-4 border-b border-slate-700">Company B</td>
                        <td class="py-2 px-4 border-b border-slate-700">18%</td>
                        <td class="py-2 px-4 border-b border-slate-700">Innovation, Customer loyalty</td>
                        <td class="py-2 px-4 border-b border-slate-700">Technology partnerships, Premium segment focus</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <h2>Recommendations</h2>
        <ol>
            <li>Focus on developing sustainable product lines to meet growing consumer demand</li>
            <li>Explore partnerships with technology providers to enhance product capabilities</li>
            <li>Target growth in emerging markets where penetration is currently low</li>
        </ol>
        
        <div class="mt-6 p-4 bg-slate-800/30 rounded-xl">
            <h3>Additional Resources</h3>
            <p>For more detailed information, consult these sources:</p>
            <ul>
                <li><a href="#" class="text-blue-400 hover:underline">Global Market Report 2023</a></li>
                <li><a href="#" class="text-blue-400 hover:underline">Consumer Trends Analysis</a></li>
                <li><a href="#" class="text-blue-400 hover:underline">Competitor Financial Reports</a></li>
            </ul>
        </div>
        
        <div class="mt-4 text-sm text-slate-500">
            <p>Report generated on {time.strftime("%B %d, %Y")} by Autonomous Research Agent v1.2</p>
        </div>
    """

@app.post("/research")
async def process_research_query(request: QueryRequest):
    inputState= {
    "messages": [
        {"role": "user", "content": request.query}
    ],
    "originalQuery": "",
    "transformedQuery": [],
    "retrievedDocs": [],
    "finalOutput": ""
}
    response=app.state.graph.invoke(input=inputState)
    return{"inner_html":response['finalOutput']}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)