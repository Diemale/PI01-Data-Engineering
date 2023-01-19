# <h1 align=center><span style="color:blue"> **PROYECTO INDIVIDUAL Nº1** </span></h1>

## **Introducción**
<p>
Este proyecto forma parte de las prácticas individuales de laboratorios de Henry. En esta instancia de evaluación se nos propuso realizar un pipeline de tratamiento de datos que incluye, extracción de datos, creación de una API web, y deployment de esta en un sitio web. Para comenzar, nuestro insumo estaba formado por cuatro datasets, que contenían los datos de cuatro reconocidas plataformas de servicio de video on-demand(Amazon Prime, Disney, Hulu y Netflix). En segundo lugar, el tratamiento de datos, consistió en una pequeña transformación a pedido del cliente, debido a que le interesaba que los datos nulos no fuesen modificados, excepto aquellos en uno solo de los campos. Para esto utilizamos Python y algunas dependencias especializadas en el tratamiento de datos. En tercer lugar, la creación de la API fue llevada adelante utilizando el framework fastapi y Python como lenguaje de programación. Para finalizar, realizamos el deployment utilizando el sitio web de Deta.
    
</p>
<hr>  

## **Desarrollo del proyecto**

### **ETL**

En  principio, contábamos con cuatro datasets de distintas plataformas de entretenimiento(Amazon Prime, Disney, Hulu y Netflix). Todos los  datasets estaban en formato csv.

<p>En primer lugar, realizamos el proceso de ETL con Jupyter Notebooks ( archivo ETL.ipynb). Optamos por cargar los cuatro datasets y realizar el proceso simultáneamente, en lugar de realizar todos los pasos para un dataset y luego comenzar con el siguiente. 
La transformación debió cumplir con los siguientes requisitos:

- "Generar campo id: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = as123)"

- "Los valores nulos del campo rating deberán reemplazarse por el string “G” (corresponde al maturity rating: “general for all audiences”"

- "De haber fechas, deberán tener el formato AAAA-mm-dd"

- "Los campos de texto deberán estar en minúsculas, sin excepciones"

- "El campo duration debe convertirse en dos campos: duration_int y duration_type. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)" 
<p/>
<p>
Para cumplir con los requisitos planteados solo fueron necesarios las librerías Pandas y Numpy. Además Pandas no solo fue utilizado para la transformación de datos, sino también para su carga y almacenamiento.
</p>


### **Creación de la API**
<p>
El objetivo de este paso era realizar cinco queries desde una web API.
Para cumplir con este punto se escogió FASTAPI.
</p>
La creación de la API consta un solo archivo .py, a saber main.py y algunos archivos __init__ para trabajar el proyecto como un solo paquete. Debido a que no se utilizó una base de datos, no fue necesario crear archivos para el manejo de esta, ni para los modelos de algún ORM que mapeara las tablas relacionales, ni tampoco para los clásicos schemas de PYDANTIC. Las librerías utilizadas
en el script main.py fueron, fastapi, pandas y uvicorn. 

Aclaramos que por una cuestión práctica, todas las funciones fueron nombradas igual que la consulta que llevan adelante. Aunque en un caso real, por cuestiones de seguridad, esta práctica no está aconsejada.

Las consultas a que realiza esta API son:

**1) Cantidad de veces que aparece una substring en el título de peliculas/series, por plataforma:
    El request debe ser: get_word_count(plataforma, palabra)**

Para esta query se creó la función `get_word_count(nombreDePlataforma: str, palabra: str)` que recibe el nombre de la plataforma y la palabra que queremos buscar en los títulos de aquella, además retorna una string con la información solicitada. 


**2) Cantidad de películas por plataforma que superen a un puntaje dado en un determinado año**
    
Esta query se realiza gracias a la función `get_score_count(nombreDePlataforma: str, score: int, year: int)` . Esta recibe como parámetro una string (el nombre  de la compañía), un puntaje(int) y un año(int), luego retorna una string.



**3) La segunda película con mayor score para una plataforma determinada, según     el orden alfabético de los títulos.
    El request debe ser: get_second_score(nombreDePlataforma):**
    
La función encargada de llevar a cabo esta query es `get_second_score(nombreDePlataforma: str)` que recibe una string(nombre de la plataforma) como parámetro y devuelve otra string que tiene el mayor puntaje de la plataforma y que, además, se encuentra segunda en orden alfabético entre todas las películas con mayor puntaje.
    
**4) Película que más duró según año, plataforma y tipo de duración 
    El request es: get_longest(plataforma, medida, year)**
  
 Esta query fue abordada con la función `get_longest(plataforma: str, medida: int, year: int)` que recibe dos strings, plataforma y medida, la primera con el nombre de la plataforma. La segunda, contiene la unidad de medida de la duración de la película. El tercer parámetro es un int, el año solicitado. Esta función retorna una string.
    
**5) Cantidad de películas y series por rating.
    get_rating_count(rating)**
    
Esta query es resuelta por la función `get_rating_count(rating: str)` que recibe una string con el tipo de calificación por edades de la película y retorna una string informando el total de películas con este rating en las cuatro plataformas como conjunto. 

Cabe aclarar que las primeras cuatro funciones cuentan no solo con las restricciones de input de fastapi (que utiliza pydantic y typing-extensions detrás de escenas para esto); sino que también retorna una string, en caso de un ingreso inválido, que avisa al usuario sobre cuáles son los datos aceptados en la query. 


### **Deployment**

Para la última fase de nuestro pipeline, elegimos Deta que es un servicio web que permite construir y almacenar aplicaciones web en la nube. En este paso seguimos las instrucciones de la documentación de fastapi. La dirección web de nuestra api se encuentra en https://ggnii8.deta.dev/docs. En la carpeta infoDeta del proyecto hay información adicional sobre el micro, además del requirements.txt utilizado para la creación de este. 

## **Puntos a mejorar en este proyecto**

Los siguientes son algunos puntos que podrían enriquecer el proyecto:

1) Crear un subdirectorio adicional que contenga al script main y a todos los datasets procesados, de manera de mejorar la organización. 

2) Mejorar las restricciones de los inputs de FASTAPI, en la quinta función

3) Realizar un EDA-ETL en profundidad, dado que no formaba parte de los requisitos del proyecto.

4) Quitar la función de testeo `read_root(nombre)`


## Sitios utilizados para realizar el proyecto

- https://fastapi.tiangolo.com/deployment/deta/
    
- https://www.deta.sh/

## Sitios con información sobre este proyecto

__Deta de la api__
- https://ggnii8.deta.dev/docs

__Repositorio Github__

- https://github.com/Diemale/PI01-Data-Engineering

__Video explicativo__

https://www.youtube.com/watch?v=qhUpNKTPbhA&feature=youtu.be