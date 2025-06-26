from py2neo import Graph, Node, Relationship
import pandas as pd

graph = Graph("neo4j://127.0.0.1:7687", auth=("neo4j", "teykg@123"))

graph.delete_all()

df = pd.read_csv("movies.csv")

for _, row in df.iterrows():
    # Create nodes
    movie = Node("Movie", name=row['movie'], genre=row['genre'])
    actor = Node("Actor", name=row['actor'])
    director = Node("Director", name=row['director'])
    company = Node("Company", name=row['company'])
    country = Node("Country", name=row['country'])

    # Merge entities
    graph.merge(movie, "Movie", "name")
    graph.merge(actor, "Actor", "name")
    graph.merge(director, "Director", "name")
    graph.merge(company, "Company", "name")
    graph.merge(country, "Country", "name")

    # Merge relationships
    graph.merge(Relationship(actor, "ACTED_IN", movie))
    graph.merge(Relationship(director, "DIRECTED", movie))
    graph.merge(Relationship(company, "PRODUCED", movie))
    graph.merge(Relationship(movie, "RELEASED_IN", country))

print("✅ Knowledge graph created successfully!")
