import json
from owlready2 import *
from rdflib import Graph

# Load the ontology
onto = get_ontology("updated_cars_trucks_ontology.owl").load()

# Initialize an RDFLib Graph
g = Graph()

# Parse the ontology into RDFLib Graph
g.parse("updated_cars_trucks_ontology.owl", format="xml")

# SPARQL Queries
# Find all procedures with more than 6 steps
query1 = """
PREFIX ex: <http://example.org/ifixit.owl#>
SELECT ?procedure
WHERE {
    ?procedure a ex:Procedure .
    ?procedure ex:has_step ?step .
}
GROUP BY ?procedure
HAVING (COUNT(?step) > 6)
"""

# Find all items that have more than 10 procedures written for them
query2 = """
PREFIX ex: <http://example.org/ifixit.owl#>
SELECT ?item
WHERE {
    ?procedure a ex:Procedure .
    ?procedure ex:has_Item ?item .
}
GROUP BY ?item
HAVING (COUNT(?procedure) > 10)
"""

# Find all procedures that include a tool not mentioned in any of their steps
query3 = """

PREFIX ex: <http://example.org/ifixit.owl#>
SELECT ?procedure ?tool
WHERE {
    ?procedure a ex:Procedure .
    ?procedure ex:requires_tool ?tool .
    
    # Find tools required by the procedure
    FILTER NOT EXISTS {
        # Match steps within the procedure
        ?procedure ex:has_step ?step .
        # Match tools used in those steps
        ?step ex:requiresTool ?tool .
    }
}
"""


query4= """
PREFIX ex: <http://example.org/ifixit.owl#>
SELECT ?procedure ?step ?text WHERE {
    ?procedure ex:has_step ?step .
    ?step ex:stepText ?text .
    FILTER (CONTAINS(LCASE(?text), "careful") || CONTAINS(LCASE(?text), "dangerous"))
}
"""


# Execute the queries
results1 = g.query(query1)
results2 = g.query(query2)
results3 = g.query(query3)
results4 = g.query(query4)

# Print results
print("Procedures with more than 6 steps:")
for row in results1:
    print(row)

print("\nItems with more than 10 procedures:")
for row in results2:
    print(row)

print("\nProcedures that include a tool not mentioned in any of their steps:")
for row in results3:
    print(row)


# Print results of the fourth query (Flagged potential hazards in procedures)
print("\nFlagged potential hazards in procedures:")
for row in results4:
    print(row)


