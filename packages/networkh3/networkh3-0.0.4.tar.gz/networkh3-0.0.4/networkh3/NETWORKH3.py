import pandas as pd
import numpy as np
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import box
import osmnx as ox
import h3
import h3pandas
import contextily as cx


def get_h3(area, network_type, resolution, network_kwargs={}, h3_kwargs={}, basemap_kwargs={}):
    global network
    defaultnetwork_kwargs = {'node_size': 0, 'edge_color': 'white', 'edge_linewidth': 0.2}
    network_kwargs = {**defaultnetwork_kwargs, **network_kwargs}
    defaulth3_kwargs = {'facecolor': 'black', 'alpha': 0.6}
    h3_kwargs = {**defaulth3_kwargs, **h3_kwargs}
    defaultbasemap_kwargs = {'zoom':'auto'}
    basemap_kwargs = {**defaultbasemap_kwargs, **basemap_kwargs}

    network = ox.graph_from_place(str(area), str(network_type))
    x_coords = []
    y_coords = []

    # Returning the lat/long coordinates for each node in the network
    for i in list(network.nodes):
        node_id = (network.nodes)[i]
        for t in node_id:
            x = node_id['x']
            y = node_id['y']
            x_coords.append(x)
            y_coords.append(y)

    # Assigning each to a new dataframe
    x_coords = pd.DataFrame(x_coords, columns=['x_coords'])
    y_coords = pd.DataFrame(y_coords, columns=['y_coords'])

    # Merging the x_coords and y_coords dataframes made above
    coordinates = x_coords.merge(y_coords, right_index=True, left_index=True)

    # Converting the coordinates dataframe to a geodataframe
    coordinates_gdf = geopandas.GeoDataFrame(
        coordinates, geometry=geopandas.points_from_xy(
            coordinates.x_coords, coordinates.y_coords), crs="EPSG:4326")

    xmin, ymin, xmax, ymax = coordinates_gdf.total_bounds

    bounds = box(*coordinates_gdf.total_bounds)

    bounds_gdf = geopandas.GeoDataFrame(
        index=[0], crs='EPSG:4326', geometry=[bounds])
    bounds_hex = bounds_gdf.h3.polyfill_resample(resolution)  # Change to desired resolution
    #####
    outline_network = ox.geocoder.geocode_to_gdf(area)

    # Setting the outline
    outline_network['outline'] = 1

    # Dissolving the network by the outline
    outline_network = outline_network.dissolve(by='outline')

    hexagons_clip = geopandas.clip(bounds_hex, outline_network)

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    hexagons_clip.plot(ax=ax, aspect=1, **h3_kwargs)

    cx.add_basemap(
        ax, crs=hexagons_clip.crs, **basemap_kwargs)

    ox.plot_graph(
        network, ax=ax, **network_kwargs)

    global h3
    h3 = hexagons_clip