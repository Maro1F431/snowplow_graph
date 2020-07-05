# Snowplow - Path calculator

## Dependancies
- `pip` requirements in the `requirements.txt` file
- `libspatialindex`, used to run `osmnx`. If you install it via `pip`

## Usage

Load the library with `import snowymontreal.snowymontreal`.
Inside the library you will find a function `montreal_snow_path` that takes as arguments :
- `district`, the name of one of Montreal's districts, which can be any of those:
    - Ahuntsic-Cartierville
    - Anjou
    - Côte-des-Neiges–Notre-Dame-de-Grâce
    - Lachine
    - LaSalle
    - Le Plateau-Mont-Royal
    - Le Sud-Ouest
    - L'Île-Bizard–Sainte-Geneviève
    - Mercier–Hochelaga-Maisonneuve
    - Montréal-Nord
    - Outremont
    - Pierrefonds-Roxboro
    - Rivière-des-Prairies–Pointe-aux-Trembles
    - Rosemont–La Petite-Patrie
    - Saint-Laurent
    - Saint-Léonard
    - Verdun
    - Ville-Marie
    - Villeray–Saint-Michel–Parc-Extension
- `is_directed`, a boolean to choose if the path has to computed from the point of view
of a flying vehicle (undirected), or on ground(directed)

This function will create a file path.csv in the current path containing the coordinates of each of the point to follow to go through
all of the streets of the district.
The function will also return the number of coordinates.

The second function that is accessible from the library is `solve`.
It takes as arguments
- `is_oriented` A boolean that states if the graph is oriented or not
- `num_vertices` The total number of vertices in the graph
- `edge_list` A list of tuples containing for each edge its source, destination and weight

And returns a list specifying the index of the edges in the list that have to be traversed in order to go through all of the edges.
