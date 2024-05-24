# Shazam PDS
## Grado en Ingeniería Informática, Universidad de Granada
### Autores: 
### Tutor: José Andrés González López

## Instalación
**Algoritmo definitivo:**
Recomendable una versión de python entre 3.8 y 3.11
Para iniciar el proceso de reconocimiento de la carpeta fragments (1500 archivos) con la carpeta songs(500), usando el algoritmo más óptimo:

1º.- Cargar la base de datos
`$python3 carga_database.py songs` -> tiempo aproximado 8 minutos

2º.- Ejecutar algoritmo de constelaciones
`$python3 main_constelacion.py fragments` -> tiempo aproximado 10 minutos

3º.- Cálculo de error
`$python3 calculaerror.py` Compara el grado de disparidad entre tablas de datos de fragments.csv y results.csv


**Uso de otros algoritmos:**
Para usar otros algoritmos ejecutar:
`$python3 PruebasPDS.py songs fragments`
Y elegir el modo mediante los inputs del programa.


**Notas:**
-Archivo database.pickle puede ocupar unos 224 megas
-Archivos de canciones 500 megas cada uno
-Se disponen de archivos alternativos de uso de algoritmos para ordenadores de menos capacidad, songs2 y fragments2
