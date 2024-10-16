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
    if request.method == 'POST':
        search_query = request.form['query']  # Get the query from the form
        print(f"Received query: {search_query}")
        print(f"Number of triples in graph: {len(g)}")  # Check the number of triples
        try:
            results = g.query(search_query)
            print(f"Query executed successfully. Number of results: {len(results)}")
            return render_template('results.html', results=results)
        except Exception as e:
            print(f"Error executing SPARQL query: {e}")  # Log the error
            return render_template('error.html', error=str(e))
    else:
        # Optionally handle GET request by rendering a search form
        return render_template('search.html')  # Render a template with the search form


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
