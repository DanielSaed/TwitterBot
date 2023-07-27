# Test de rendimiento bases de datos Nosql

Desarrollar y utilizar las nuevas aplicaciones de la actualidad ha creado nuevas necesidades en la arquitectura de las bases de datos NoSQL, estas tienen que ser cada vez más ágiles, también requieren un desarrollo cada vez más enfocado a los datos en tiempo real, al igual que cada vez es más necesario que esta tecnología pueda procesar cómodamente impredecibles niveles de escala, velocidad y variabilidad de datos, agregando a todo esto la necesidad de las empresas y organizaciones de innovar rápidamente, operar a cualquier escala, además de cumplir la demanda principal que es la experiencia de usuario.

<br>

## Bases de datos NoSql utilizadas

- MongoDB
- Couchbase
- Azure CosmoDB

*Todas la bases de datos anteriores utilizan el patron de arquitectura de datos por documentos.*

Las pruebas se hicieron mediante la interfaz de cada base de datos.

- MongoDB:  MongoDB Compass.
- En Azure CosmosDB: Azure Cosmos DB Emulator
- Couchbase: Dashboard de Couchbase Community Server.

<br>

## Características Computador:

●	Procesador: Ryzen 7 5800H
●	Ram: 16GB DDR4 3200Mhz
●	Almacenamiento: 512 GB SSD 3000 mb\s

<br>

## Datasets utilizados:

 <table align="middle">
  <tr align="middle">
    <td><img src="https://github.com/DanielSaed/TwitterBot/blob/main/img/FP2HUNGRIAracepace.png" width=650 height=325 align="middle"></td>
  </tr>
 </table>
 
 <br>
 
## Metodologia

**Metodologia Seguida en la investigacion**

<table align="middle">
  <tr>
    <td><img src="https://github.com/DanielSaed/Investigacion/blob/main/img-github/diagrama.png" width=650 height=325></td>
  </tr>
 </table>
 
 <br>

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
