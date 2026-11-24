import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load edge list
df = pd.read_csv("edges2.csv")

# Create directed graph
G = nx.from_pandas_edgelist(df, source='Source', target='Target', create_using=nx.DiGraph())

# Basic info
print("\n--- GRAPH SUMMARY ---")
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

# Metrics
deg = dict(G.degree())
in_deg = dict(G.in_degree())
out_deg = dict(G.out_degree())
bc = nx.betweenness_centrality(G)
cc = nx.closeness_centrality(G)

# Create results table
data = []
for node in G.nodes():
    data.append([
        node,
        deg[node],
        in_deg[node],
        out_deg[node],
        round(bc[node], 4),
        round(cc[node], 4)
    ])

results_df = pd.DataFrame(data, columns=[
    "Node", "Degree", "In-Degree", "Out-Degree",
    "Betweenness Centrality", "Closeness Centrality"
])

# Sort by importance
results_df = results_df.sort_values(by="Betweenness Centrality", ascending=False)

print("\n--- NODE METRICS TABLE ---")
print(results_df.to_string(index=False))

# Save results to CSV (for report)
results_df.to_csv("results.csv", index=False)

# Draw graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)

nx.draw(
    G, pos,
    with_labels=True,
    node_size=600,
    font_size=7,
    arrows=True
)

plt.title("SRS Requirements Graph")
plt.show()