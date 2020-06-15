
import folium
import pandas


# Building a function that according to elevation data in Castles.txt creates different color markers (line 33).
def color_differentiation(elevation):
    if elevation < 50:
        return "green"
    elif 50 <= elevation < 200:
        return "orange"
    elif 200 <= elevation:
        return "red"
    else:
        return "black"


#Create a base WebMap with a map object (default source of the object is openstreet maps).
BaseMap = folium.Map(location=[50.26, 9.33], zoom_start= 2, tiles="Mapbox Bright")

# Importing the data from the txt file in a dataframe.
data = pandas.read_csv("Castles.txt")
# Extracting the wanted content/information from the data dataframe to lists.
location = list(data["Castle"])
lon = list(data["Longitude"])
lat = list(data["Latitude"])
elev = list(data["Elevation"])


# Creating a group of features/objects just to be more organized and easy to implement them.
fga = folium.FeatureGroup(name="Markers")
# Adding to this group multiple features.
for loc, ln, lt, el in zip(location, lon, lat, elev):
    fga.add_child(folium.CircleMarker(location=[lt,ln], radius=6, popup=loc+", "+str(el)+" m",
    fill=True, fill_opacity= 0.9, fill_color=color_differentiation(el), color="grey"))

fgb = folium.FeatureGroup(name="Polygons")
# Adding a polygon layer with <<folium.GeoJson()>> function.
import io # Without io, the encoding argument inside open function, does not get recognized.
fgb.add_child(folium.GeoJson(data=io.open('world.json', 'r', encoding='utf-8-sig').read(),
style_function = lambda x: {'fillColor': 'black' if x['properties']['POP2005'] < 1000000 # With argument style_function we can play with the content of opened json file.
else 'green' if 1000000 <= x['properties']['POP2005'] < 10000000
else 'yellow' if 10000000 <= x['properties']['POP2005'] < 20000000
else 'orange' if 20000000 <= x['properties']['POP2005'] < 30000000
else 'red'}))

# Adding objects on the existing map object with .add_child() function.
BaseMap.add_child(fgb)
BaseMap.add_child(fga)

# Creating a layer controller.
BaseMap.add_child(folium.LayerControl())

# Save and translate the map object as html file.
BaseMap.save("MyMap1.html")
