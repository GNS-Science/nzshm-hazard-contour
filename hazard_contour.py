#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
# import folium
import branca
# from folium import plugins
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import geojsoncontour
import scipy as sp
import scipy.ndimage

# Setup
debug=False
vmin=0
vmax=10.0

# Setup colormap
colors = ['#d7191c',  '#fdae61',  '#ffffbf',  '#abdda4',  '#2b83ba']
levels = len(colors)
cm     = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)

def as_geojson(table):

    df = pd.DataFrame(table['rows'], columns=table['column_headers'])

    # select just one iml_period, with only the cols of interest, converting types to numeric
    df = df[df.iml_period=='0.5'].filter(['lon', 'lat', 'PofET 0.02']).apply(pd.to_numeric)

    # The original data
    x_orig = np.asarray(df['lon'].tolist())
    y_orig = np.asarray(df['lat'].tolist())
    z_orig = np.asarray(df['PofET 0.02'].tolist())

    # Make a grid
    x_arr          = np.linspace(np.min(x_orig), np.max(x_orig), 500)
    y_arr          = np.linspace(np.min(y_orig), np.max(y_orig), 500)
    x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

    # Grid the values
    z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='linear')

    # Gaussian filter the grid to make it smoother
    sigma = [5, 5]
    z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode='constant')

    # Create the contour
    contourf = plt.contourf(x_mesh, y_mesh, z_mesh, levels, alpha=0.5, colors=colors, linestyles='None', vmin=vmin, vmax=vmax)

    # Convert matplotlib contourf to geojson
    geojson = geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        min_angle_deg=3.0,
        ndigits=5,
        stroke_width=1,
        fill_opacity=0.5)

    return geojson