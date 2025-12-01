import numpy as np
import time

# Códigos ANSI para colores de terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m' # Código para resetear el color

# --- 1. FUNCIÓN PARA CREAR LA MATRIZ DE ADYACENCIA ---
def create_adjacency_matrix(nodes, edges):
    """
    [Cerebro Matemático] Crea la matriz de adyacencia (M) a partir de los nodos y las aristas.
    El elemento M[i, j] = 1 si hay conexión, 0 si no hay.
    """
    n = len(nodes)
    M = np.zeros((n, n), dtype=int)
    node_index = {name: i for i, name in enumerate(nodes)}

    for start, end in edges:
        i = node_index[start]
        j = node_index[end]
        M[i, j] = 1
        M[j, i] = 1 # Amistad bidireccional

    return M, node_index

# --- 2. FUNCIÓN PARA CALCULAR LA POTENCIA DE LA MATRIZ ---
def calculate_paths(M, k):
    """
    [Cerebro Matemático] Calcula la k-ésima potencia de la matriz M (M^k).
    """
    print(f"\n{Colors.BLUE}[PROCESO] Iniciando cálculo matricial para caminos de longitud K...{Colors.ENDC}")
    time.sleep(1.5) 
    
    M_k = np.linalg.matrix_power(M, k)
    
    print(f"{Colors.BLUE}[PROCESO] Cálculo finalizado. Matriz M^k generada.{Colors.ENDC}")
    time.sleep(1)
    return M_k

# --- 3. FUNCIÓN PARA INTERPRETAR Y FORMATEAR LOS RESULTADOS ---
def interpret_results(M_k, M_matrix, nodes, k):
    """
    Traduce los números de la matriz M^k a frases entendibles, filtrando
    solo las conexiones puramente indirectas (M[i, j] debe ser 0).
    """
    results = []
    n = len(nodes)
    for i in range(n):
        for j in range(n):
            num_caminos = M_k[i, j]
            es_directa = (M_matrix[i, j] == 1)

            # 1. La conexión debe existir (num_caminos > 0)
            # 2. No debe ser la misma persona (i != j)
            # 3. NO debe ser una amistad directa (es_directa debe ser False, o M[i, j] == 0)
            if i != j and num_caminos > 0 and not es_directa: 
                # El resto de la lógica de plurales y la construcción de la frase se mantiene.
                plural_o_singular = "camino" if num_caminos == 1 else "caminos"
                pasos = "paso" if k == 1 else "pasos"
                
                results.append(f"{nodes[i]} tiene {num_caminos} {plural_o_singular} indirectos (de {k} {pasos}) con {nodes[j]}.")
    return results