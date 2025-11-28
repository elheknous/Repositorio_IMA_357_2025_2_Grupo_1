import streamlit as st
import pandas as pd
import re
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')

st.set_page_config(
    page_title="Repositorio IMA 357 - Grupo 1",
    layout="wide"
)


# Funcion para calcular similud Coseno entre listas
def sim_coseno(vec1, vec2):
    if len(vec1) != len(vec2):
        return 0
        
    dot_prod = 0
    for i, v in enumerate(vec1):
        dot_prod += v * vec2[i]
        
    norm1 = math.sqrt(sum([x**2 for x in vec1]))
    norm2 = math.sqrt(sum([x**2 for x in vec2]))

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_prod / (norm1 * norm2)
    

def contar_frecuencia_exacta(texto, palabra):
    return len(re.findall(r'\b'+ re.escape(palabra)+r'\b', texto.lower()))

#----------------- CARGAR DATOS ----------------

st.title("Aplicación Grupo 1 IMA-357")
st.subheader("Visualización de Datos")

REPO_URL = "https://raw.githubusercontent.com/elheknous/Repositorio_IMA_357_2025_2_Grupo_1/main/cuerpo_documentos_p2_gr_1.csv"

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv(REPO_URL)
        return df
    except:
        return None

st.subheader("Contenido del archivo: cuerpo_documentos_p2_gr_1.csv extraido desde GitHub")

with st.spinner('Conectando con GitHub y descargando datos...'):
    df = cargar_datos()

if df is not None:
    
    # Mostrar tabla inicial
    col1, col2 = st.columns(2)
    col1.metric("Filas totales", df.shape[0])
    col2.metric("Columnas", df.shape[1])
    
    st.dataframe(df, use_container_width=True)
    st.success("Datos cargados exitosamente.")

#----------------- BUSQUEDA POR PALABRA ----------------

    st.divider()
    
    # Ingresar palabra
    palabra_input = st.text_input("Introduzca una palabra:", key="input_word")
    
    palabra_limpia = palabra_input.strip().lower()
    
    if 'texto' in df.columns:
        # Calculamos frecuencia
        lista_frecuencias = []

        for texto in df['texto']:
            frecuencia = contar_frecuencia_exacta(texto, palabra_limpia)
            lista_frecuencias.append(frecuencia)

        # Columna nueva al DataFrame que gurada la frecuencia de la palabra solicitada
        df['Frecuencia'] = lista_frecuencias


        
        max_val = df['Frecuencia'].max()
        df_ganadores = df[df['Frecuencia'] == max_val]
        st.write(f"Resultados para '{palabra_input}':")
        
        if max_val > 0:
            #res_df = df_ganadores[['titular', 'Frecuencia']].copy()
            st.dataframe(df_ganadores[["titular","Frecuencia"]])
        else:
            st.warning(f"La palabra '{palabra_input}' no aparece en el documento.")


#----------------- BUSQUEDA POR FRASE ----------------

    st.write("") 
    oracion_input = st.text_input("Ingrese una oración:", key="input_sentence")
    
    if oracion_input:
                
        # Crear lista de todos los párrafos en el csv
        lista_parrafos = []
        for idx, row in df.iterrows():
            if pd.notna(row['texto']):
                # Dividimos por saltos de línea
                parrafos = str(row['texto']).split('\n')
                for p in parrafos:
                    p = p.strip()
                    lista_parrafos.append({
                        'texto_parrafo': p,
                        'titular': row['titular'],
                        'topico': row['topico']
                        })
        
        # Vectorizar 
        textos_a_vectorizar = [d['texto_parrafo'] for d in lista_parrafos] + [oracion_input]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(textos_a_vectorizar)
        
        dense_matrix = tfidf_matrix.toarray()
        vec_oracion = dense_matrix[-1]       
        vec_parrafos = dense_matrix[:-1]     
        
        mejor_similitud = -1
        idx_mejor = -1
        
        for i, vec_p in enumerate(vec_parrafos):
            sim = sim_coseno(vec_p, vec_oracion) 
            if sim > mejor_similitud:
                mejor_similitud = sim
                idx_mejor = i
        
        if idx_mejor != -1:
            ganador = lista_parrafos[idx_mejor]
            st.write(f"Documento con mayor similitud según Coseno")
            st.markdown(f"* **Título**: {ganador['titular']}")
            st.markdown(f"* **Tópico**: {ganador['topico']}")
            st.markdown(f"* **Similitud Coseno**: {mejor_similitud:.4f}")

        # Suma de frecuencia
        import nltk
        tokens_busqueda = re.findall(r'\w+', oracion_input.lower())
        stopwords = nltk.corpus.stopwords.words('spanish') # quitar stopword

        tokens_busqueda = [x for x in tokens_busqueda if x not in stopwords]

        def sumar_tokens(txt):
            txt_lower = txt.lower() 
            suma = 0
            for t in tokens_busqueda:
                suma += len(re.findall(r'\b' + re.escape(t) + r'\b', txt_lower))
            return suma
            
        df['suma_frec'] = df['texto'].apply(sumar_tokens)
        max_suma = df['suma_frec'].max()
        idx_suma = df['suma_frec'].idxmax()
        doc_suma = df.loc[idx_suma]
        
        st.write("")
        st.write(f"Mayor coincidencia para suma de frecuencias (Sin StopWords): {max_suma} apariciones totales")
        st.markdown(f"* **Título**: {doc_suma['titular']}")
        st.markdown(f"* **Tópico**: {doc_suma['topico']}")
        st.markdown(f"* **Suma Frecuencias**: {max_suma}")

else:
    st.error("No se pudo cargar el archivo.")
    st.code(REPO_URL, language='text')