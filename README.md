
## Dataset
Para el desarrollo de la actividad, se utilizó un dataset de canciones de Spotify proveniente de Kaggle en formato `csv`, el cual contiene información sobre diferentes canciones, incluyendo sus características musicales y su popularidad. A continuación, se presenta un resumen de las columnas presentes en el dataset y sus tipos; además, se realizó una investigación para entender qué representaba cada columna, obteniendo lo siguiente:
| Columna | Tipo | Descripción |
|--|--|--|
| **track_id** | `str` | Identificador único de la canción dentro de Spotify. Sirve para consultar información adicional mediante la API. |
| **artists** | `str` | Artista(s) que interpretan la canción. En algunos datasets aparecen concatenados en una sola cadena. | 
| **album_name** | `str` | Nombre del álbum al que pertenece la canción. | 
| **track_name** | `str` | Nombre de la canción. | 
| **popularity** | `int64` | Índice de popularidad calculado por Spotify considerando la cantidad y actualidad de las reproducciones. Cuanto mayor sea el valor, más popular es la canción. | 
| **duration_ms** | `int64` | Duración de la canción en milisegundos. | 
| **explicit** | `bool` | Indica si la canción contiene contenido explícito. | 
| **danceability** | `float64` | Qué tan adecuada es la canción para bailar. Se calcula usando tempo, estabilidad del ritmo, intensidad del pulso y regularidad. | 
| **energy** | `float64` | Mide la intensidad y actividad percibida de la canción. Las canciones rápidas, fuertes y ruidosas suelen tener mayor energía. | 
| **key** | `int64` | Tonalidad musical de la canción usando la notación Pitch Class. | 
| **loudness** | `float64` | Volumen promedio de la canción medido en decibelios (dB). Generalmente toma valores negativos. | 
| **mode** | `int64` | Modo musical de la canción. | 
| **speechiness** | `float64` | Detecta la presencia de palabras habladas. | 
| **acousticness** | `float64` | Probabilidad de que la canción sea acústica. | 
| **instrumentalness** | `float64` | Probabilidad de que la canción no tenga voces. | 
| **liveness** | `float64` | Detecta la presencia de público durante la grabación. | 
| **valence** | `float64` | Mide el carácter emocional positivo de la canción. | 
| **tempo** | `float64` | Tempo estimado de la canción. | 
| **time_signature** | `int64` | Compás estimado de la canción, indicando el número de pulsos por compás. | 
| **track_genre** | `int64` | Género musical asociado a la canción en el dataset. Este campo normalmente proviene del conjunto de datos y no es una característica calculada por el objeto de Audio Features. | 

 > El dataset cuenta con 114000 filas y 21 columnas


## Exploración
La exploración de los datos se realizó utilizando la herramienta de Jupyter Lab, donde se realizaron 2 análisis exploratorios con el fin de entender cómo estaban constituidos los datos y cómo organizarlos para el análisis que se requería. Los notebooks se pueden encontrar en la carpeta [notebooks](notebooks/) del proyecto. A continuación, se describen los análisis realizados:
- [Análisis exploratorio 1](notebooks/exploracion_inicial.ipynb)
En este notebook se buscaba entender cómo estaban compuestos y distribuidos, verificando tipos, dimensiones, valores nulos, valores únicos y la distribución por variables categóricas.
- [Análisis exploratorio 2](notebooks/exploracion_agrupacion.ipynb)
Teniendo en cuenta lo explorado anteriormente, se realizaron las primeras pruebas para agrupar los datos según lo analizado y las métricas a obtener.

## Limpieza
Según lo analizado, se tomaron las siguientes decisiones para la limpieza:
- Cast de tipos: Los tipos en el dataset original ya estaban bien tipados, así que se mantuvieron.
- Valores nulos: Se encontró una única fila con algunos valores nulos, por lo que se tomó la decisión de eliminarla, ya que correspondía a un porcentaje ínfimo de los datos y los valores faltantes eran relevantes para los datos.
- Normalización: Se halló que muchas canciones tenían el mismo nombre, pero algunas palabras diferían entre minúscula y mayúscula, por lo que las columnas de `track_name` y `artists` se convirtieron a minúscula.
- Agrupación: Probablemente la decisión más importante de la limpieza; se encontró que muchas canciones tenían el mismo nombre y artista, pero con ID y nombre de álbum diferente, y se llegó a la conclusión de que dificultaría el análisis posterior, por lo que se decidió agrupar los registros por nombre y artista.
- Columnas: Se mantuvieron 19 de las 21 columnas del dataset, eliminando la columna `"Unnamed 0:"` que representaba un índice en el dataset original y la columna  `track_id` que no se vio necesaria incluir en la agrupación.

### Agrupación
Aquí se especifica con detalle la decisión tomada para cada columna tras la agrupación. La agrupación por nombre y artista convirtió los demás valores en objetos (en la prueba exploratoria se convirtieron en lista), por lo que habría que definir qué valor representaría la fila. He aquí la tabla con las decisiones tomadas:
| Columna | Medida | Razón |
|--|--|--|
| **album_name** | `first` | No había forma clara de tomar el nombre "correcto" del álbum, por lo que se tomó la primera ocurrencia. | 
| **popularity** | `max` | Por cómo funciona el algoritmo de Spotify, se decide tomar el máximo valor de popularidad. | 
| **duration_ms** | `median` | Para obtener un valor real de la duración, se escogió la mediana sobre la media, ya que proporcionaba un valor real en comparación con la media, que podía devolver una duración no existente entre los distintos tracks. | 
| **explicit** | `mode` | En general, no había variación de los datos, por lo que el valor más común sería el dato más adecuado. | 
| **danceability** | `mean` | La desviación en los datos era mínima, así que se usa la media. | 
| **energy** | `mean` | Mismo caso que el anterior | 
| **key** | `mode` | Debería ser el mismo independientemente del track, así que el más popular era lo más adecuado. | 
| **loudness** | `median` | Para evitar valores no reales, se usó la mediana. | 
| **mode** | `mode` | No deberían haber variaciones, así que se usa el más popular. | 
| **speechiness** | `mean` | Los valores no suelen variar mucho. | 
| **acousticness** | `mean` | Los valores no suelen variar mucho. | 
| **instrumentalness** | `mean` | Los valores no suelen variar mucho. | 
| **liveness** | `min` | Se priorizó la versión de estudio sobre posibles sesiones en vivo | 
| **valence** | `mean` | Los valores no suelen variar mucho. | 
| **tempo** | `median` | Los valores no suelen variar mucho, pero se priorizó un valor real. | 
| **time_signature** | `mode` | Los valores deberían ser constantes. | 
| **track_genre** | `mode` | Se priorizó la etiqueta de género más popular; en caso de existir más de una, se utiliza el primer índice. | 

Tras la limpieza de los datos, se mantuvieron 81206 registros y 19 columnas.
