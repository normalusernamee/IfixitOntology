from flask import Flask, render_template, request, redirect, url_for
from rdflib import Graph
from owlready2 import get_ontology

app = Flask(__name__)

# Load the ontology
onto = get_ontology("updated_cars_trucks_ontology.owl").load()
g = Graph()
g.parse("updated_cars_trucks_ontology.owl", format="xml")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Get all classes and properties from the ontology
    classes = [cls.name for cls in onto.classes()]
    properties = [prop.name for prop in onto.properties()]
    
    if request.method == 'POST':
        search_query = request.form['query']
        print(f"Received query: {search_query}")
        print(f"Number of triples in graph: {len(g)}")
        try:
            results = g.query(search_query)
            print(f"Query executed successfully. Number of results: {len(results)}")
            return render_template('results.html', results=results)
        except Exception as e:
            print(f"Error executing SPARQL query: {e}")
            return render_template('error.html', error=str(e))
    
    # Render the search form with classes and properties
    return render_template('search.html', classes=classes, properties=properties)
@app.route('/execute_query', methods=['POST'])
def execute_query():
    # Get user inputs
    select_clause = request.form['select']
    where_clause = request.form['where']
    additional_conditions = request.form.getlist('condition')  # Get all conditions
    filter_conditions = request.form.getlist('filter')  # Get all filter conditions
    group_by_clause = request.form['groupBy']
    having_clause = request.form['having']

    # Start building the SPARQL query
    sparql_query = f"""
    PREFIX ex: <http://example.org/ifixit.owl#>
    SELECT {select_clause} WHERE {{
        {where_clause} .
    """

    # Add additional conditions,
    if additional_conditions:
        for condition in additional_conditions:
            if condition.strip():  # check the condition is not empty
                sparql_query += f"    {condition.strip()} .\n"

    # Add FILTER conditions
    if filter_conditions:
        for filter_condition in filter_conditions:
            if filter_condition.strip():  # check the filter condition is not empty
                sparql_query += f"    FILTER ({filter_condition.strip()})\n"

    # Close the WHERE clause
    sparql_query += "}"

    # Add GROUP BY if provided
    if group_by_clause.strip():  # check it is not empty
        sparql_query += f"\nGROUP BY {group_by_clause.strip()}"

    # Add HAVING if provided
    if having_clause.strip():  # check it is not empty
        sparql_query += f"\nHAVING ({having_clause.strip()})"

    # Execute the generated query
    try:
        results = g.query(sparql_query)
        print(f"Query executed successfully. Number of results: {len(results)}")
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")  # Log the error
        return render_template('error.html', error=str(e))

    # Render the results
    return render_template('results.html', results=results)




@app.route('/display')
def display_data():
    
    # Get instances for each class
    instances_by_class = {cls.name: list(cls.instances()) for cls in onto.classes()}
    
    return render_template('display.html', ontology=onto, instances_by_class=instances_by_class)

@app.route('/instance/<string:instance_name>')
def instance_details(instance_name):
    query = f"""
    PREFIX ex: <http://example.org/ifixit.owl#>
    SELECT ?property ?value
    WHERE {{
        ex:{instance_name} ?property ?value .
    }}
    """
    # Execute the query on the graph
    results = g.query(query)

    # Extract properties and values
    properties = {}
    for row in results:
        prop = str(row.property)
        value = str(row.value)
        if prop not in properties:
            properties[prop] = []
        properties[prop].append(value)

    return render_template('instance_details.html', instance_name=instance_name, properties=properties)



@app.route('/user_guide')
def user_guide():
    # Logic to display the user guide
    return render_template('user_guide.html')

@app.route('/sparql')
def sparql_queries():
    # Logic to show predefined SPARQL queries
    return render_template('sparql.html')

from rdflib import Literal, URIRef

@app.route('/edit', methods=['GET', 'POST'])
def edit_graph():
    if request.method == 'POST':
        operation = request.form['operation']
        rdf_data = request.form['data']

        try:
            # Parse RDF data into a temporary graph
            temp_graph = Graph()
            temp_graph.parse(data=rdf_data, format="turtle")

            if operation == 'add':
                # Add the data to the main graph
                for triple in temp_graph:
                    g.add(triple)
                message = "Data added successfully."

            elif operation == 'update':
                # Update operation: delete old triples, then add new ones
                for triple in temp_graph:
                    # Remove old triple first (if any), then add the new one
                    g.remove(triple)
                    g.add(triple)
                message = "Data updated successfully."

            elif operation == 'delete':
                # Delete the triples from the graph
                for triple in temp_graph:
                    g.remove(triple)
                message = "Data deleted successfully."

            # Serialize the updated graph back to the ontology file
            g.serialize(destination="updated_cars_trucks_ontology.owl", format="xml")

        except Exception as e:
            message = f"An error occurred: {str(e)}"

        return render_template('edit.html', message=message)

    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)
