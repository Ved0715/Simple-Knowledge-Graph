import spacy
import textacy
import csv
from py2neo import Graph, Node, Relationship
import pandas as pd

text = """
Elon Musk, a South African-born American entrepreneur, is renowned for founding and leading several groundbreaking companies. In 2002, Musk founded SpaceX (Space Exploration Technologies Corp.) in Hawthorne, California with the aim of reducing space transportation costs and enabling the colonization of Mars. SpaceX developed the Falcon 1, Falcon 9, and Falcon Heavy launch vehicles, as well as the Dragon spacecraft. It became the first private company to send a spacecraft to the International Space Station (ISS). SpaceX is also responsible for the Starlink satellite internet constellation.

In addition to his work with SpaceX, Musk is the CEO and product architect of Tesla Inc., a company he joined in 2004, though it was originally founded by Martin Eberhard and Marc Tarpenning. Tesla, headquartered in Austin, Texas, specializes in electric vehicles, battery energy storage, and solar energy through its acquisition of SolarCity in 2016. Tesla’s major products include the Model S, Model 3, Model X, Model Y, and Cybertruck. Tesla operates Gigafactories in Nevada, Berlin, Shanghai, and Texas.

In 2015, Elon Musk, along with researchers like Sam Altman, co-founded OpenAI, an AI research and deployment company with a mission to ensure that artificial general intelligence (AGI) benefits all of humanity. OpenAI started as a nonprofit but later shifted to a "capped-profit" model in order to attract investment and scale. In 2019, Microsoft invested $1 billion in OpenAI, forming a strategic partnership that included access to Azure cloud services. Sam Altman became the CEO of OpenAI after Musk stepped down from the board in 2018 due to potential conflicts of interest with Tesla’s own AI work.

Musk is also behind the Boring Company, founded in 2016 to develop underground transportation systems like Hyperloop and Loop. He envisions a future where traffic congestion is solved by high-speed underground travel.

In 2017, he launched Neuralink, a neurotechnology company focused on developing brain-computer interfaces (BCIs). The goal of Neuralink is to enable direct communication between the brain and computers, which could help people with neurological diseases and eventually merge human cognition with AI.

In 2022, Musk acquired Twitter Inc. for approximately $44 billion, renaming it to X Corp in 2023. His aim was to transform it into an “everything app” — combining social networking, payments, and entertainment.

Elon Musk’s influence extends into renewable energy, transportation, finance, and AI ethics. He is a vocal proponent of carbon neutrality, free speech, and regulation of artificial intelligence.

In 2023, Tesla announced plans to expand into India, with discussions involving the Indian government around setting up manufacturing facilities and research centers. Tesla Energy, a division of Tesla, has installed Powerwall and Powerpack systems across several continents, helping homes and industries adopt renewable energy.

Meanwhile, SpaceX continues to develop its Starship vehicle for missions to the Moon and Mars, under contracts with NASA and international space agencies. The Starbase facility in Boca Chica, Texas has become a major hub of operations, hosting frequent launches and tests.

Musk’s ventures are tightly interconnected. Tesla’s AI expertise supports autonomous driving and energy optimization; SpaceX’s satellite infrastructure supports OpenAI and Neuralink's research, while X Corp serves as a communication layer across platforms.

Outside of his companies, Musk frequently collaborates with other entrepreneurs and thought leaders. He has participated in public discussions with Lex Fridman, Joe Rogan, and Jack Dorsey, often discussing futuristic technologies and existential risks.

Elon Musk’s net worth fluctuates with Tesla stock but often places him among the world’s richest individuals, along with Jeff Bezos, Bernard Arnault, and Bill Gates.
"""


nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

triplets = list(textacy.extract.subject_verb_object_triples(doc))

for s, v, o in triplets:
    print(f"({s}, {v}, {o})")

with open('triplets.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Subject', 'Verb', 'Object'])  # Header
    for s, v, o in triplets:
        writer.writerow([s[0], v[0], o[0]])


graph = Graph("neo4j://127.0.0.1:7687", auth=("neo4j", "teykg@123"))
graph.delete_all()

df = pd.read_csv("triplets.csv")


for _, row in df.iterrows():
    subject_text = str(row['Subject']).strip()
    verb_text = str(row['Verb']).strip().upper().replace(" ", "_")  # Neo4j relation names can't have spaces
    object_text = str(row['Object']).strip()

    # Create nodes
    subject_node = Node("Entity", name=subject_text)
    object_node = Node("Entity", name=object_text)

    # Merge nodes
    graph.merge(subject_node, "Entity", "name")
    graph.merge(object_node, "Entity", "name")

    # Create and merge relationship
    relationship = Relationship(subject_node, verb_text, object_node)
    graph.merge(relationship)

print("✅ Knowledge graph created successfully!")