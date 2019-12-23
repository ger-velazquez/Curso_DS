
# coding: utf-8

# Vamos a jugar un poco con python y Pandas.
# 
# Me bajé, del repositorio de datos de la ciudad de Buenos Aires, un listado completo de universidades con sede en CABA y sus unidades académicas: https://data.buenosaires.gob.ar/dataset/universidades
# 
# Vamos a ver qué podemos hacer con eso...

# Primero vamos a importar pandas, para procesar el CSV como dataset

# In[2]:


import pandas as pd


# Vamos a levantar el CSV y a revisar qué tiene...

# In[3]:


universidades_data = pd.read_csv('./universidades.csv')
universidades_data.head()


# Para romper los huevos, veamos de qué tipo es el listado (dataframe, obvio)

# In[37]:


type(universidades_data)


# Dado que cada universidad tiene muchas sedes, vamos a ver dónde tienen sus rectorados

# In[4]:


rectorados = universidades_data[universidades_data['unidad_aca'] == 'Rectorado']
print(rectorados)


# Ya que estamos jugando, vamos a ver cuáles son las universidades

# In[5]:


universidades = universidades_data['universida'].unique()
len(universidades)


# In[6]:


print(universidades)


# Con la información de rectorados, y la de universidades, ahora quiero ver si todas las universidades tienen rectorado. Una forma trucha de hacerlo es verificar que ambos listados tienen la misma longitud:

# In[8]:


if (len(universidades) == len(rectorados)):
  print('Sin iguales')
elif (len(universidades) > len(rectorados)):
  print('Hay universidades que no tienen rectorados')
else:
  print('Alguna universidad tiene más de un rectorado. Raro che.')


# In[9]:


print(len(rectorados))
print(len(universidades))


# Ahora voy a jugar con folium, una librería que encontré que puede servir para mostrar información geolocalizada (el CSV tiene información de latitud y longitud)

# In[10]:


import folium


# Le digo a folium que me cree un mapa, centrado en CABA, y con un toque de zoom para ver bien la ciudad

# In[11]:


map_osm = folium.Map(location=[-34.5941696,-58.4583627], zoom_start=12)

map_osm


# Ahora voy a iterar sobre el listado de universidades, para marcar en el mapa donde están las distintas sedes. Pongo circulitos para las sedes

# In[12]:


universidades_data.apply(lambda row:folium.CircleMarker(location=[row["lat"], 
                                                  row["long"]]).add_to(map_osm),
         axis=1)
map_osm


# Y ahora haré lo mismo con los rectorados, para contrastar donde tienen los rectorados las distintas universidades. Pongo marcadores típicos para los rectorados

# In[13]:


rectorados.apply(lambda row:folium.Marker(location=[row["lat"], 
                                                  row["long"]]).add_to(map_osm),
         axis=1)
map_osm

