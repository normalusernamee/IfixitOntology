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
    group_by_clause = request.form['groupBy']
    having_clause = request.form['having']

    # Start building the SPARQL query
    sparql_query = f"""
    PREFIX ex: <http://example.org/ifixit.owl#>
    SELECT {select_clause} WHERE {{
        {where_clause} .
    """

    # Add additional conditions, ensuring proper formatting
    if additional_conditions:
        for condition in additional_conditions:
            if condition.strip():  # Ensure the condition is not empty
                sparql_query += f"    {condition.strip()} .\n"

    # Close the WHERE clause
    sparql_query += "}"

    # Add GROUP BY if provided
    if group_by_clause.strip():  # Ensure it is not empty
        sparql_query += f"\nGROUP BY {group_by_clause.strip()}"

    # Add HAVING if provided
    if having_clause.strip():  # Ensure it is not empty
        sparql_query += f"\nHAVING ({having_clause.strip()})"

    # Execute the generated query
    try:
        results = g.query(sparql_query)
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



@app.route('/user_guide')
def user_guide():
    # Logic to display the user guide
    return render_template('user_guide.html')

@app.route('/sparql')
def sparql_queries():
    # Logic to show predefined SPARQL queries
    return render_template('sparql.html')

@app.route('/edit')
def edit_graph():
    # Logic for editing the knowledge graph (add, update, delete entries)
    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)
