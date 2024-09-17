from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Edge(BaseModel):
    source: str
    target: str

class Node(BaseModel):
    id: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


def is_dag(nodes, edges):
    graph = {}
    for node in nodes:
        graph[node['id']] = []
    
    # adding edges to the graph
    for edge in edges:
        graph[edge['source']].append(edge['target'])
    
    # function to check for cycles starting from a given node
    def has_cycle(start_node):
        stack = [(start_node, [start_node])]
        visited = set()

        while stack:
            node, path = stack.pop()
            
            if node not in visited:
                visited.add(node)
                
                for neighbor in graph[node]:
                    if neighbor in path:
                        return True  # Cycle detected
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))
        
        return False  # No cycle found

    for node in graph:
        if has_cycle(node):
            return False  # Graph is not a DAG
    
    return True  # Graph is a DAG

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post('/pipelines/parse') 
def parse_pipeline(pipeline: str = Form(...)):
    import json

    pipeline_data = json.loads(pipeline)
    nodes = pipeline_data["nodes"]
    edges = pipeline_data["edges"]

    num_nodes = len(nodes)
    num_edges = len(edges)
    is_dag_result = is_dag(nodes, edges)

    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag_result}