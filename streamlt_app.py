import streamlit as st
import pandas as pd
from PIL import Image
import time
import json
import random
from datetime import datetime
import datetime
import os
import numpy as np
import requests

from tqdm import tqdm
from cred_here import *
from utils import *
import ast

# Tools

import folium
from shapely.geometry import Polygon
import numpy as np
import geojson
import geojson as gpd
from tqdm import tqdm
from shapely.geometry import Polygon
import shapely.wkt
from haversine import haversine, Unit
import random
import time
from pyproj import Geod

from shapely import wkt
from geopandas import datasets, GeoDataFrame, read_file, points_from_xy

from folium.plugins import MeasureControl
from folium.plugins import MarkerCluster

from streamlit_folium import folium_static


#inicio de aplicación
key = st.text_input("Pon un api key de geolocalización")

image = Image.open('perfil.jpg')

st.sidebar.markdown('Nicolas Gutierrez')
st.sidebar.image(image , caption="Aplicación de la gasolinería de aceite más cercana a tí",width = 250)
app_mode = st.sidebar.selectbox("escoge que quieres ver", ["Aplicación","Sobre mí"])


if app_mode == 'Aplicación':

    st.title('Aplicación de la gasolinería de aceite más cercana a tí')
    st.markdown('Aplicación creada para buscar un lugar y ver cuales son las gasolinerías cercanas a tí y que puedas mirar sus precios. :)')

    df_map = pd.read_csv('DF_STATIONS.csv')
    cities =  list(df_map['Municipio'].unique())

    c1,c2,c3,c4,c5 = st.columns((1,6,6,6,1))

    choose_city =  c2.selectbox("Escoge la ciudad:", cities)

    central_location = c2.text_input('Lugar específico', 'unac, Medellín')

    DEVELOPER_KEY = key

    if len(central_location) != 0 :

        R = GetLatLon2(central_location,key)
        geo_source = R[1],R[2]

        unit = 'Km'
        rad = c4.slider('Radius',1,3,1)

        df_city = df_map[df_map['Municipio']==choose_city]
        df_city.reset_index(inplace = True)
        df_city.drop(columns = 'index',inplace = True)

        df_city =  transform_df_map(df_city)

        results = distance_estac(geo_source,df_city,rad,unit)
        results = results.reset_index()
        results = results.drop(columns = 'index')
        products =  list(results['Producto'].unique())

        gdf_stores_results = GeoDataFrame(results,
                                            geometry=points_from_xy(results.LNG,results.LAT))


        choose_products =  c3.selectbox("Choose Oil", products)

        if c3.button('MOSTRAR EL MAPA'):

            gdf_stores_results2 = gdf_stores_results[gdf_stores_results['Producto']==choose_products]
            gdf_stores_results2 = gdf_stores_results2.reset_index()
            gdf_stores_results2 = gdf_stores_results2.drop(columns = 'index')
            icono = "usd"

            m = folium.Map([geo_source[0],geo_source[1]], zoom_start=15)

            # Circle
            folium.Circle(
            radius=int(rad)*1000,
            location=[geo_source[0],geo_source[1]],
            color='green',
            fill='red').add_to(m)

            # Centroid
            folium.Marker(location=[geo_source[0],geo_source[1]],
                                icon=folium.Icon(color='black', icon_color='white',
                                icon="home", prefix='glyphicon')
                                ,popup = "<b>CENTROID</b>").add_to(m)

            marker_rest(gdf_stores_results2,m,unit,choose_products,icono)

            # call to render Folium map in Streamlit
            folium_static(m)
            
elif app_mode == "Sobre mí":
    st.title('Aplicación de la gasolinería de aceite más cercana a tí')
    st.success("Aquí mis redes 👇 ")

    col1,col2,col3,col4 = st.columns((2,1,2,1))
    col1.markdown('* [**LinkedIn**](https://www.linkedin.com/in/nicolas-steven-gutierrez-castiyejo-7a26a3235/)')
    col1.markdown('* [**GitHub**](https://github.com/imnicoo7)')
    col1.markdown('* [**Instagram**](https://www.instagram.com/imnicoo__/)')
    col1.markdown('* [**Twitter**](https://twitter.com/Nicolas76675034)')
    image2 = Image.open('perfil.jpg')
    col3.image(image2,width=230)