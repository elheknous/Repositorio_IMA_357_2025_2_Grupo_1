# Repositorio\_IMA\_357\_2025\_2\_Grupo\_1



Guía de Usuario:



La aplicación está dividida en tres secciones principales:



\### Visualización de Datos

Al iniciar la aplicación, el sistema se conectará automáticamente al repositorio y descargará el archivo `cuerpo\\\_documentos\\\_p2\\\_gr\\\_1.csv`.

\* Verás un resumen con el \*\*número total de filas y columnas\*\*.

\* Se mostrara la base de datos cargada.



\### Búsqueda por Palabra Clave

Esta sección permite encontrar qué documento menciona más veces una palabra específica.



1\. Escribe una palabra en el campo de texto: \*\*"Introduzca una palabra"\*\*



Aquí da igual si la palabra esta en mayúsculas o minúsculas, pero si es importante escribir el tilde de cada palabra en caso de lo posea, por ejemplo si el usuario escribe araucania no encontrara nada, lo correcto seria escribir araucanía.





2\. Presiona Enter.





3\. La aplicación mostrará una tabla con los titulares de los documentos donde esa palabra se repite más veces y la frecuencia exacta de aparición.





\### Búsqueda por Frase (Similitud Coseno y TF-IDF)



1\. Ve al campo \*\*"Ingrese una oración"\*\*.



2\. Escriba una frase.



3\. El sistema procesará tu entrada y te devolverá dos resultados:

 

   \* \*\*A. Resultado por Similitud Coseno:\*\*

     Utiliza algoritmos de \*Machine Learning\* (TF-IDF) para encontrar el párrafo que matemáticamente se parece más a tu frase. Te mostrará el \*\*Título\*\*, el \*\*Tópico\*\* y el puntaje de \*\*Similitud\*\* (de 0 a 1).



   \* \*\*B. Resultado por Suma de Frecuencias:\*\*

     Busca qué documento contiene la mayor cantidad de las palabras que están en la frase, ignorando las StopWords (como \*el, la, de, y\*). Muestra el documento con mayor coincidencia.

