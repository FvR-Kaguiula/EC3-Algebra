import networkx as nx
import matplotlib.pyplot as plt
import time 
import numpy as np
from social_network_model import create_adjacency_matrix, calculate_paths, interpret_results, Colors 

# --- NOMBRES REALES PARA LOS 20 NODOS ---
NOMBRES_PERSONAS = [
    'Sofía', 'Alejandro', 'Valentina', 'Mateo', 'Isabella', 
    'Sebastián', 'Camila', 'Nicolás', 'Luciana', 'Diego', 
    'Mariana', 'Daniel', 'Victoria', 'Adrián', 'Gabriela', 
    'Felipe', 'Emilia', 'Pablo', 'Paula', 'Javier' 
]
NUM_NODES = len(NOMBRES_PERSONAS)
NODES = NOMBRES_PERSONAS

# Generar una red aleatoria (Grafo de Erdős-Rényi)
G_RANDOM = nx.fast_gnp_random_graph(n=NUM_NODES, p=0.3, seed=42) 

# Extraer las aristas (conexiones) del grafo generado aleatoriamente
EDGES = []
for u, v in G_RANDOM.edges():
    EDGES.append((NODES[u], NODES[v]))

def main_large_scale_example():
    # Pausa tras el encabezado
    print(f"\n{Colors.RED}================================================================{Colors.ENDC}")
    time.sleep(0.1)
    print(f"{Colors.GREEN}🌐 EJEMPLO A ESCALA: ANÁLISIS DE RED SOCIAL ({NUM_NODES} NODOS) 📊{Colors.ENDC}")
    time.sleep(0.1)
    print(f"{Colors.RED}================================================================{Colors.ENDC}")
    time.sleep(1.5)

    # --- 2. PREPARACIÓN MATEMÁTICA ---
    print(f"\n{Colors.BLUE}[PASO 1] 💾 Leyendo la estructura de la Red de {NUM_NODES} Nodos...{Colors.ENDC}")
    time.sleep(1)
    M_matrix, node_index = create_adjacency_matrix(NODES, EDGES)

    print(f"[PASO 1] {Colors.GREEN}✅ Red de {NUM_NODES} Nodos y {len(EDGES)} Conexiones Cargada.{Colors.ENDC}")
    time.sleep(1)

    # IMPRESIÓN DE TODOS LOS NODOS CON NOMBRES REALES
    print(f"\n{Colors.RED}--- Mapeo Completo de Personas a Índices (Filas/Columnas) ---{Colors.ENDC}")
    time.sleep(0.5)
    
    # Imprime línea por línea el mapeo con pausas
    mapeo_ordenado_lines = [f"| {i+1:02d}. {nombre:10s} (Índice: {indice:2d}) |" for i, (nombre, indice) in enumerate(node_index.items())]
    for line in mapeo_ordenado_lines:
        print(line)
        time.sleep(0.05) 
        
    print(f"{Colors.RED}----------------------------------------------------------------{Colors.ENDC}")
    time.sleep(1.0)
    
    # Imprimir la Matriz M (Solo una indicación)
    print(f"\n{Colors.BLUE}Matriz M de {NUM_NODES}x{NUM_NODES} lista para el cálculo.{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.BLUE}Se ha creado una matriz de {NUM_NODES} filas y {NUM_NODES} columnas.{Colors.ENDC}")
    time.sleep(1.0)

    # --- 3. INTERACCIÓN (Fijamos K=2 para la demostración de Amigos en Común) ---
    k = 2 
    print(f"\n{Colors.BLUE}[PASO 2] ⚙️ Configuración del Análisis: Se fijó Profundidad K={k}{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.GREEN}ANÁLISIS SELECCIONADO:{Colors.ENDC} Se calculará M^{k} (Amigos en Común).")
    time.sleep(2)

    # --- 4. CÁLCULO DEL ÁLGEBRA LINEAL ---
    M_k_result = calculate_paths(M_matrix, k) 
    
    print(f"\n{Colors.RED}--- RESULTADO: Matriz de Caminos M^{k} (Extracto 5x5) ---{Colors.ENDC}")
    time.sleep(0.5)
    print(M_k_result[:5, :5]) 
    time.sleep(0.5)
    
    print(f"\n{Colors.BLUE}[EXPLICACIÓN MATRIZ M^K]:{Colors.ENDC}")
    time.sleep(0.5)
    print("   El valor M^2(i, j) indica el NÚMERO TOTAL de 'Amigos en Común' entre i y j.")
    time.sleep(0.5)
    print(f"{Colors.RED}----------------------------------------------------------------{Colors.ENDC}")
    time.sleep(2.5)

    # --- 5. INTERPRETACIÓN DE RESULTADOS ---
    print(f"\n{Colors.BLUE}[PASO 3] 🔍 Interpretación y Análisis de Conexiones...{Colors.ENDC}")
    time.sleep(1.5)
    results = interpret_results(M_k_result, NODES, k)
    
    print(f"\n{Colors.GREEN}✅ TOP 10 CONEXIONES INDIRECTAS ENCONTRADAS (Ranking por N° de Caminos):{Colors.ENDC}")
    time.sleep(0.5)
    
    ranked_results = sorted(results, key=lambda x: int(x.split(' ')[2]), reverse=True)
    
    if ranked_results:
        for i, res in enumerate(ranked_results[:10]): 
            print(f"🔗 {Colors.RED}({i+1:02d}){Colors.ENDC} {res}")
            time.sleep(0.2) 
    else:
        print(f"{Colors.RED}❌ No se encontraron caminos de longitud {k} en esta red. Prueba con otro valor de K.{Colors.ENDC}")
    time.sleep(1.5)

    # --- 6. VISUALIZACIÓN ---
    print(f"\n{Colors.BLUE}[PASO 4] 📈 Generando Gráfico de la Red de {NUM_NODES} nodos...{Colors.ENDC}")
    time.sleep(1.5)
    
    G = G_RANDOM
    pos = nx.spring_layout(G, seed=42, k=0.5) 

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_title(f"Red Aleatoria de {NUM_NODES} Nodos - Análisis de Profundidad K={k}", fontsize=14, fontweight='bold')
    
    COLOR_DIRECTO = '#2ecc71' 
    COLOR_INDIRECTO = '#3498db' 
    
    original_edges_idx = list(G.edges())
    indirect_only_edges_for_coloring = [] 

    for i in range(NUM_NODES):
        for j in range(i + 1, NUM_NODES): 
            es_directa = (M_matrix[i, j] == 1)
            tiene_caminos_k = (M_k_result[i, j] > 0)
            
            u, v = i, j 
            
            if tiene_caminos_k and not es_directa:
                 indirect_only_edges_for_coloring.append((u, v))

    
    # 1. Dibujar TODAS las aristas originales (VERDE y DELGADAS)
    nx.draw_networkx_edges(G, pos, edgelist=original_edges_idx, width=2.0, edge_color=COLOR_DIRECTO, alpha=1.0, ax=ax)


    # 2. Dibujar las aristas indirectas (AZULES DISCONTINUAS) GRUESAS ENCIMA
    if indirect_only_edges_for_coloring:
        nx.draw_networkx_edges(G, pos, edgelist=indirect_only_edges_for_coloring, width=1.5, edge_color=COLOR_INDIRECTO, alpha=0.7, style='dashed', ax=ax) 

    # 3. Dibujar Nodos y Etiquetas 
    labels = {i: NODES[i] for i in range(NUM_NODES)}

    nx.draw_networkx_nodes(G, pos, node_color='#e74c3c', node_size=500, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_color='white', font_weight='bold', font_size=8, ax=ax)

    # --- GLOSARIO DE CONEXIONES ---
    glosario = f"""
    [GLOSARIO]
    - Nodos: Las {NUM_NODES} personas de la simulación.
    - Línea Verde Continua: Amistad Directa (K=1).
    - Línea Azul Discontinua: Conexión Indirecta (K={k}).
    """
    ax.text(0.5, -0.05, glosario.strip(),
             horizontalalignment='center', fontsize=10, 
             bbox=dict(facecolor='white', alpha=0.9, boxstyle='round'),
             transform=ax.transAxes)
    
    # Pausa final
    print(f"\n{Colors.RED}================================================================{Colors.ENDC}")
    time.sleep(0.1)
    print(">>> La ventana del gráfico a escala se ha generado. Cierre la ventana para finalizar. <<<")
    time.sleep(0.1)
    print(f"{Colors.RED}================================================================{Colors.ENDC}")
    plt.show()

if __name__ == "__main__":
    main_large_scale_example()