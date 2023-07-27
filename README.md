# TwitterBot de analisis de datos sobre F1

Desde la contratacion de Sergio Perez a RedBull, en conjunto con la introduccion de la serie Drive to survive de Netflix, nuevos fans han llegado a la F1, aunque esto implique tambien que el desconocieminto de ciertos temas tecnicos, el no entender el deporte, la falta de experiencia, entre otras cosas sean situaciones un poco mas visibles por obvias razones, ese es el motivo por el cual decidi empezar este proyecto.
<br>

## Tecnologias y librerias utilizadas

- Python 3.10 . Matplotlib
- API Fast F1
- TweetPY
- MongoDB

*El proyecto esta en standby debido a las nuevas reglamentacion de Twitter.*

<br>

## Pagina Twitter:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/Home.png" width=550 height=500 align="middle"></td>
  </tr>
 </table>

<br>

## Tweet comparacion de su vuelta mas rapida en la practica entre Perez y Verstappen:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/Home.png" width=550 height=500 align="middle"></td>
  </tr>
 </table>

<br>

## Ejemplo ritmo de carrera en una practica:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/FP2HUNGRIAracepace.png" width=550 height=500 align="middle"></td>
  </tr>
 </table>
 
 <br>

## Ejemplo simulacion de calificacion en una practica:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/FP3HUNGRIAqualysim.png" width=550 height=500 align="middle"></td>
  </tr>
 </table>
 
 <br>
 
## Ejemplo telemetrai entre 2 vueltas de Perez y Verstappen:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/FP3HUNGRIAtelemetry.png" width=550 height=500 align="middle"></td>
  </tr>
 </table>
 
 <br>
  
## Ejemplo Velocidad maxima en una practica:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/FP3HUNGRIAvelmax.png" width=550 height=500 align="middle"></td>
  </tr>
 </table>
 
 <br>
## Metodologia

**Metodologia Seguida en la investigacion**


**Consultas utilizadas**

Se optó por solamente utilizar consultas de lectura en las pruebas, Se repitió 3 veces la misma consulta y se tomó el promedio, se utilizaron 8 cantidades de resultados diferentes para las mediciones. 

El flujo de trabajo que se utilizó para los conjuntos de datos **Películas** y **Ruta Aviones** fue el siguiente:

- 1,000 resultados
- 10,000 resultados
-	50,000 resultados
-	100,000 resultados
-	200,000 resultados
-	400,000 resultados
-	600,000 resultados
- 800,000 resultados

Mientras que para el conjunto de datos **Denue** se utilizaron solamente 6 cantidades diferentes de resultados para las mediciones:

- 1,000 resultados
- 10,000 resultados
- 50,000 resultados
- 100,000 resultados
- 200,000 resultados
- 300,000 resultados

<br>

**La prueba se realizó de manera local, se utilizaron 2 métodos para hacer las pruebas de las bases de datos:**

*Test en caliente:*
- Las consultas se realizaron de manera consecutiva.

*Test en frío:*
- Las consultas se realizaron apagando el ordenador cada vez que se realizaba una consulta.

<br>

## Resultados

### Resultados Dataset Peliculas 

<table align="middle">
  <tr>
    <td><img src="https://github.com/DanielSaed/Investigacion/blob/main/img-github/pelicula.png" width=500 height=480></td>
    <td><img src="https://github.com/DanielSaed/Investigacion/blob/main/img-github/PeliculasFrio.png" width=500 height=480></td>
  </tr>
 </table>

### Resultados Dataset Ruta Aviones 
