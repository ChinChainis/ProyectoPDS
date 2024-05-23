# Asegúrate de tener instaladas en tu ordenador estas librerías.
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def custom_confusion_matrix(ground_truth, predicted, confusion_matrix_type='relative'):    
    # Inicializar la matriz de confusión
    confusion_matrix = np.zeros(5)
    
    # Caso 1: Canciones bien identificadas
    confusion_matrix[0] = np.sum((ground_truth == predicted) & (ground_truth.str.startswith('song_')))
    
    # Caso 2: Fragmentos NOT_FOUND bien identificados
    confusion_matrix[1] = np.sum((ground_truth == predicted) & (ground_truth == 'NOT_FOUND'))

    # Caso 2: Canciones incorrectamente identificadas por otra canción
    confusion_matrix[2] = np.sum((ground_truth.str.startswith('song_')) & (predicted.str.startswith('song_')) & (ground_truth != predicted))

    # Caso 3: Canciones incorrectamente identificadas y asignadas la etiqueta NOT_FOUND
    confusion_matrix[3] = np.sum((ground_truth.str.startswith('song_')) & (predicted == 'NOT_FOUND'))

    # Caso 4: Fragmentos de canción marcados en el ground_truth como 'NOT_FOUND' pero identificados como canciones
    confusion_matrix[4] = np.sum((ground_truth == 'NOT_FOUND') & (predicted.str.startswith('song_')))
    
    # Normalizamos por el número de fragmentos en cada condición
    if confusion_matrix_type == 'relative':
        num_fragment_songs = np.sum(ground_truth.str.startswith('song_'))  # Fragmentos pertenecientes a canciones
        num_fragment_nf = np.sum(ground_truth == 'NOT_FOUND')  # Fragmentos pertenecientes a canciones NOT_FOUND
        norm_factor = np.zeros(5)
        norm_factor[0] = num_fragment_songs
        norm_factor[1] = num_fragment_nf
        norm_factor[2] = num_fragment_songs
        norm_factor[3] = num_fragment_songs
        norm_factor[4] = num_fragment_nf
    else:
        # Normalizamos por el número total de fragmentos, sin discernir entre clases
        norm_factor = len(ground_truth)
    
    # Pasamos los valores a porcentajes
    return (100.0 * confusion_matrix)/norm_factor


def calculate_error_rate(ground_truth_file, results_file, confusion_matrix_type='relative'):
    # Cargar los datos de los ficheros CSV
    ground_truth_df = pd.read_csv(ground_truth_file)
    results_df = pd.read_csv(results_file)

    # Unir los datos en función del fragmento para comparar las predicciones con los resultados reales
    merged_df = pd.merge(ground_truth_df, results_df, on='fragment', suffixes=('_truth', '_predicted'))

    # Calcular la tasa de error
    error_rate = 1 - accuracy_score(merged_df['song_truth'], merged_df['song_predicted'])

    # Calcular la matriz de confusión
    confusion = custom_confusion_matrix(merged_df['song_truth'], merged_df['song_predicted'], confusion_matrix_type)
    confusion_matrix = pd.DataFrame(confusion, columns=['Percentage'])
    confusion_matrix.index = ['Correct (Song->Song)', 'Correct (NF->NF)', 'Incorrect (Song->Song)', 'Incorrect (Song->NF)', 'Incorrect (NF->Song)']

    return error_rate, confusion_matrix

GROUND_TRUTH_FILE = 'fragments.csv'   # Fichero CSV que venía con el dataset de canciones que os pasé
RESULTS_FILE = 'result.csv'   # <<<--- Aseguraos de modificar esto con el nombre del fichero CSV generado por vuestro programa

# Calcular las métricas
error_rate, confusion_df = calculate_error_rate(GROUND_TRUTH_FILE, RESULTS_FILE, 'relative')
print(f"TASA DE ERROR: {100*error_rate:.2f}%")

print("RESULTADOS GLOBALES: ", confusion_df)


# Ploteamos la matriz de confusión como un gráfico de barras
confusion_df.plot.bar(legend=False)
plt.title('Resultados globales', fontsize=16)
# plt.xlabel('Condiciones', fontsize=14)
plt.ylabel('%', fontsize=14)
plt.xticks(rotation=0, fontsize=6)
plt.yticks(fontsize=12)
plt.ylim(0, 100)
plt.tight_layout()
plt.show()
