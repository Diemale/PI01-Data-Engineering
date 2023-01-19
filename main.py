from fastapi import FastAPI
import pandas as pd
#import uvicorn

# cargar data
dfAmazon = pd.read_csv('Amazon.csv')
dfDisney = pd.read_csv('Disney.csv')
dfHulu = pd.read_csv('Hulu.csv')
dfNetflix = pd.read_csv('Netflix.csv')

dfHulu.duration_int = pd.Series(dfHulu.duration_int, dtype=pd.Int32Dtype())
dfNetflix.duration_int = pd.Series(dfNetflix.duration_int, dtype=pd.Int32Dtype())

# crear  la app
#########################################################
app = FastAPI()
#
### Crear las funciones para realizar las requests

# Test function
@app.get("/")
def read_root(nombre):
    return nombre
#

## Funciones principales
# Estas funciones usan type hints para restringir el tipo de datos utilizado en las queries (por ejemplo
# year: int sinifica que el argumento year no aceptará un tipo de dato que no sea int, en cuyo caso el
# usuario recibirá un mensaje de error intantáneo.).


@app.get("/get_word_count")
def get_word_count(nombreDePlataforma: str, palabra: str):
    # si el nombre de la plataforma es el de la sentencia if( ó elif) toma el campo title y suma las ocurrencias
    # de la palabra buscada, utilizando la función .str.count() de Pandas
    if nombreDePlataforma == 'amazon':
        s = dfAmazon.title
        totalSubstrings = s.str.count(palabra).sum()

    elif nombreDePlataforma == 'disney':
        s = dfDisney.title
        totalSubstrings = s.str.count(palabra).sum()
    elif nombreDePlataforma == 'hulu':
        s = dfHulu.title
        totalSubstrings = s.str.count(palabra).sum()
    elif nombreDePlataforma == 'netflix':
        s = dfNetflix.title
        totalSubstrings = s.str.count(palabra).sum()

    # si el dato ingresado como parámetro no es ninguno de los especificados arriba, retorna un aviso al usuario.
    else:
        return f'Solo los siguientes nombres de plataforma son válidos: amazon disney hulu netflix'
    # si los inputs son válidos devuelve la cantidad de veces que la palabra aparece en los títulos de la plataforma
    return f'La palabra {palabra} aparece {totalSubstrings} veces en los títulos enlistados en {nombreDePlataforma}.'


@app.get("/get_score_count")
def get_score_count(nombreDePlataforma: str, score: int, year: int):
    # si el nombre de la plataforma solicitada es amazon
    if nombreDePlataforma == 'amazon':
        # filtra aquellos registros que cumplan con las siguiente tres condiciones: superar el score del input, que
        # año sea el solicitado y que el tipo de show sea movie. Guarda la cantidad de esos registros como int.
        scoreMayor = dfAmazon[(dfAmazon.score > score) & (dfAmazon.release_year == year) & (dfAmazon.type == 'movie')]
        cuenta = len(scoreMayor)
    # El paso se repite para las otras plataformas
    elif nombreDePlataforma == 'disney':
        scoreMayor = dfDisney[(dfDisney.score > score) & (dfDisney.release_year == year) & (dfDisney.type == 'movie')]
        cuenta = len(scoreMayor)

    elif nombreDePlataforma == 'hulu':
        scoreMayor = dfHulu[(dfHulu.score > score) & (dfHulu.release_year == year) & (dfHulu.type == 'movie')]
        cuenta = len(scoreMayor)

    elif nombreDePlataforma == 'netflix':
        scoreMayor = dfNetflix[(dfNetflix.score > score) & (dfNetflix.release_year == year) & (dfNetflix.type == 'movie')]
        cuenta = len(scoreMayor)
    # si el nombre de la plataforma ingresada es distinto a las esperadas crea un mensaje para el usuario.
    else:
        return f'Solo los siguientes nombres de plataforma son válidos: amazon disney hulu netflix'
    # si todos los inputs son correctos
    return f'Para el año {year}, existen {cuenta} películas en {nombreDePlataforma} con un score mayor que {score}.'


@app.get("/get_second_score")
def get_second_score(nombreDePlataforma: str):

    if nombreDePlataforma == 'amazon':
        # filtrar los registros de películas cuyo score sea el máximo de la plataforma
        maxAmazon = dfAmazon[(dfAmazon.score == dfAmazon.score.max()) & (dfAmazon.type == 'movie')]
        # ordenar los registros según el orden alfabético de la columna 'title'
        maxAmazon = maxAmazon.sort_values('title').reset_index(drop=True)
        # extraer el resultado de la segunda fila bajo el campo 'title'
        resultado = maxAmazon.loc[1,'title']

    elif nombreDePlataforma == 'disney':
        maxDisney= dfDisney[(dfDisney.score == dfDisney.score.max()) & (dfDisney.type == 'movie')]
        maxDisney = maxDisney.sort_values('title').reset_index(drop=True)
        resultado = maxDisney.loc[1,'title']

    elif nombreDePlataforma == 'hulu':
        maxHulu= dfHulu[(dfHulu.score == dfHulu.score.max()) & (dfHulu.type == 'movie')]
        maxHulu = maxHulu.sort_values('title').reset_index(drop=True)
        resultado = maxHulu.loc[1,'title']

    elif nombreDePlataforma == 'netflix':
        maxNetflix= dfNetflix[(dfNetflix.score == dfNetflix.score.max()) & (dfNetflix.type == 'movie')]
        maxNetflix = maxNetflix.sort_values('title').reset_index(drop=True)
        resultado = maxNetflix.loc[1,'title']

    else:
        return f'Solo los siguientes nombres de plataforma son válidos: amazon disney hulu netflix'

    return f'Entre las películas de mayor score de {nombreDePlataforma}, la segunda en orden alfabético es: {resultado}.'

@app.get("/get_longest")
def get_longest(plataforma: str, medida: str, year: int):
    plataformas = ['amazon', 'disney', 'hulu', 'netflix']
    # Las primeras 2 líneas del bloque avisan al usuario,si usó una string incorrecta, cuales son las entradas correctas
    # Debería hacer otro bloque para el año
    if plataforma not in plataformas:
        return f'Solo los siguientes nombres de plataforma son válidos: amazon disney hulu netflix'
    elif medida != 'min':
        return f'Nuestra búsqueda solo soporta minutos como medida de duración, por favor ingrese la palabra min'
    elif plataforma == 'amazon':
            # filtrar por año
            maxDMovie = dfAmazon[(dfAmazon.release_year) == year]

    elif plataforma == 'disney':
        # filtrar por año
        maxDMovie = dfDisney[(dfDisney.release_year) == year]

    elif plataforma == 'hulu':
        # filtrar por año
        maxDMovie = dfHulu[(dfHulu.release_year) == year]

    else:
        maxDMovie = dfNetflix[(dfNetflix.release_year) == year]

    # elegir los registros de duración máxima y su medida en minutos
    registro = maxDMovie[(maxDMovie.duration_int == maxDMovie.duration_int.max()) & (maxDMovie.duration_type == medida)]
    registro = registro.reset_index(drop = True)
    pelicula = registro.loc[0,'title']
    duracion = registro.loc[0,'duration_int']
    med = registro.loc[0,'duration_type']

    return f'La película de mayor duración de {plataforma} en {year} es {pelicula}, con {duracion} minutos.'


@app.get("/get_rating_count")
def get_rating_count(rating: str):
    # abajo utilizamos la función pandas.Series.str.count para contar las apariciones de la string pasada como parámetro
    # en cada una de las columnas 'rating' de los cuatro datafram
    cuenta =  dfAmazon.rating.str.count(rating).sum() + dfDisney.rating.str.count(rating).sum()
    cuenta += + dfHulu.rating.str.count(rating).sum() + dfNetflix.rating.str.count(rating).sum()

    return f'El total de series y películas, de todas las plataformas, con rating {rating} es: {cuenta}'
