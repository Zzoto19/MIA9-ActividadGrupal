#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:21:08 2024

@author: hiperion
"""

# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

git add requirements.txt
git commit -m "Añadiendo el archivo requirements.txt con las dependencias"
git push origin main

# Función principal de la app
def main():
    st.title('Aplicación Interactiva de Visualización de Datos')
    st.write('Carga tu dataset y explora los datos de forma interactiva.')

    # Cargar datos
    data = cargar_datos()

    if data is not None:
        # Vista previa de los datos
        st.subheader('Vista previa de los datos')
        st.write(data.head())

        # Resumen estadístico
        st.subheader('Resumen Estadístico')
        st.write(data.describe())

        # Información del dataset
        st.subheader('Información del Dataset')
        buffer = io.StringIO()
        data.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        # Visualizaciones
        st.subheader('Visualizaciones')
        all_columns = data.columns.tolist()
        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Histograma', 'Gráfico de barras', 'Gráfico de dispersión'])
        columna_seleccionada = st.selectbox('Selecciona la columna', all_columns)

        if tipo_grafico == 'Histograma':
            fig, ax = plt.subplots()
            ax.hist(data[columna_seleccionada], bins='auto')
            st.pyplot(fig)

        if tipo_grafico == 'Gráfico de barras':
            conteo = data[columna_seleccionada].value_counts()
            st.bar_chart(conteo)

        if tipo_grafico == 'Gráfico de dispersión':
            x_axis = st.selectbox('Selecciona la variable X', all_columns)
            y_axis = st.selectbox('Selecciona la variable Y', all_columns)
            fig, ax = plt.subplots()
            ax.scatter(data[x_axis], data[y_axis])
            st.pyplot(fig)

        # Mapa interactivo
        if 'latitude' in data.columns and 'longitude' in data.columns:
            st.subheader('Mapa Interactivo')
            st.map(data[['latitude', 'longitude']])
        else:
            st.info('El dataset no contiene datos geoespaciales.')

        # Filtrar datos
        st.subheader('Filtrar Datos')
        filtro_columna = st.selectbox('Selecciona la columna para filtrar', all_columns)
        valores_unicos = data[filtro_columna].unique()
        valor_seleccionado = st.multiselect('Selecciona los valores', valores_unicos)
        data_filtrada = data[data[filtro_columna].isin(valor_seleccionado)]
        st.write(data_filtrada)

        # Matriz de correlación
        st.subheader('Matriz de Correlación')
        corr_matrix = data.corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, ax=ax, annot=True)
        st.pyplot(fig)

# Función para cargar los datos
def cargar_datos():
    uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success('Datos cargados correctamente!')
        return data
    else:
        st.warning('Por favor, carga un archivo CSV.')
        return None

# Ejecutar la aplicación
if __name__ == '__main__':
    main()
