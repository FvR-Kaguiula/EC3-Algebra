import networkx as nx
import matplotlib.pyplot as plt
import time 
import numpy as np
from social_network_model import create_adjacency_matrix, calculate_paths, interpret_results, Colors 

# --- 1. DEFINICIÓN DE LA RED SOCIAL ---
NODES = ['Alex', 'Brenda', 'Carlos', 'Daniel', 'Eva', 'Felipe', 'Gala']
NUM_NODES = len(NODES) 

EDGES = [
    ('Alex', 'Brenda'),
    ('Alex', 'Carlos'),
    ('Brenda', 'Eva'),
    ('Carlos', 'Daniel'),
    ('Daniel', 'Felipe'),
    ('Eva', 'Felipe'),
    ('Brenda', 'Gala') 
]

def main():
    # Encabezado (Pausas ligeramente más largas)
    print(f"\n{Colors.RED}===================================================={Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.GREEN}📊 SIMULADOR: Algoritmo de Conexión de Amistades 🤝{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.RED}===================================================={Colors.ENDC}")
    time.sleep(1)

    # Explicación Inicial
    print(f"\n{Colors.BLUE}Este programa analiza la red social usando Álgebra Lineal (M^K) para descubrir conexiones.{Colors.ENDC}")
    time.sleep(1)

    # --- 2. PREPARACIÓN MATEMÁTICA ---
    print(f"\n{Colors.BLUE}[PASO 1] 💾 Leyendo la Red Social...{Colors.ENDC}")
    time.sleep(0.5)
    M_matrix, node_index = create_adjacency_matrix(NODES, EDGES)

    print(f"[PASO 1] {Colors.GREEN}✅ Red de {NUM_NODES} Nodos cargada.{Colors.ENDC}")
    time.sleep(0.5)

    # Mapeo de Personas
    print(f"\n{Colors.RED}--- Mapeo de Personas a Índices ---{Colors.ENDC}")
    time.sleep(0.5)
    mapeo_ordenado = '\n'.join([f"| {i+1}. {nombre:10s} (Índice: {indice:2d}) |" for i, (nombre, indice) in enumerate(node_index.items())])
    print(mapeo_ordenado)
    time.sleep(0.5)
    print(f"{Colors.RED}-----------------------------------{Colors.ENDC}")
    time.sleep(1)

    # Impresión de la Matriz M
    print(f"\n{Colors.RED}--- Matriz de Adyacencia (M) - K=1 (Amigos Directos) ---{Colors.ENDC}")
    time.sleep(0.5)
    print(M_matrix)
    time.sleep(0.5)
    print(f"\n{Colors.BLUE}[EXPLICACIÓN]: M(i, j) = 1 si son amigos directos.{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.RED}------------------------------------------------------{Colors.ENDC}")
    time.sleep(1)

    # --- 3. INTERACCIÓN (Restricción K a 1, 2, 3) ---
    print(f"\n{Colors.BLUE}[PASO 2] ⚙️ Seleccione el Nivel de Profundidad (K) para el análisis:{Colors.ENDC}")
    time.sleep(0.5)
    
    opciones = {
        1: "1: Amistad Directa (M^1)",
        2: "2: Amigos de Amigos / Amigos en Común (M^2)",
        3: "3: Conexiones Indirectas Extendidas (M^3)"
    }
    print('\n'.join(opciones.values()))

    while True:
        try:
            k = int(input(f">>> Ingrese K (1, 2, o 3): "))
            if k in opciones:
                break
            else:
                 print(f"{Colors.RED}ERROR: Por favor, ingrese 1, 2, o 3.{Colors.ENDC}")
                 time.sleep(0.5)
        except ValueError:
            print(f"{Colors.RED}ERROR: Entrada inválida. Debe ingresar un número entero.{Colors.ENDC}")
            time.sleep(0.5)
    
    print(f"\n{Colors.GREEN}ANÁLISIS SELECCIONADO:{Colors.ENDC} {opciones[k]}")
    time.sleep(1)

    # --- 4. CÁLCULO DEL ÁLGEBRA LINEAL ---
    M_k_result = calculate_paths(M_matrix, k) 
    
    print(f"\n{Colors.RED}--- RESULTADO: Matriz de Caminos M^{k} ---{Colors.ENDC}")
    time.sleep(0.5)
    print(M_k_result)
    time.sleep(0.5)
    
    print(f"\n{Colors.BLUE}[EXPLICACIÓN]: M^{k}(i, j) = NÚMERO TOTAL de caminos de {k} pasos entre i y j.{Colors.ENDC}")
    time.sleep(0.5)
    print(f"{Colors.RED}----------------------------------------------------{Colors.ENDC}")
    time.sleep(1.5)

    # --- 5. INTERPRETACIÓN DE RESULTADOS ---
    print(f"\n{Colors.BLUE}[PASO 3] 🔍 Ranking de Conexiones Indirectas...{Colors.ENDC}")
    time.sleep(0.5)
    
    # IMPORTANTE: Pasamos M_matrix para filtrar solo las puramente indirectas (M[i, j] == 0)
    results = interpret_results(M_k_result, M_matrix, NODES, k)
    
    print(f"\n{Colors.GREEN}✅ TOP CONEXIONES (Ordenado por fuerza):{Colors.ENDC}")
    time.sleep(0.5)
    
    ranked_results = sorted(results, key=lambda x: int(x.split(' ')[2]), reverse=True)
    
    if ranked_results:
        for i, res in enumerate(ranked_results):
            print(f"🔗 {Colors.RED}({i+1}){Colors.ENDC} {res}")
            time.sleep(0.2)
    else:
        print(f"{Colors.RED}❌ No se encontraron caminos puramente indirectos de longitud {k} en esta red.{Colors.ENDC}")
    time.sleep(1)

    # --- 6. VISUALIZACIÓN (CORRECCIÓN FINAL DE LÍNEAS VERDES) ---
    print(f"\n{Colors.BLUE}[PASO 4] 📈 Generando Gráfico de la Red...{Colors.ENDC}")
    time.sleep(0.5)
    
    G = nx.Graph()
    G.add_nodes_from(range(NUM_NODES)) 
    
    # 1. Añadir las aristas originales (para el cálculo de pos y para el primer dibujo)
    original_edges_idx = [(node_index[u], node_index[v]) for u, v in EDGES]
    G.add_edges_from(original_edges_idx) 

    pos = nx.spring_layout(G, seed=42) 

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(f"Red Social ({opciones[k]})", fontsize=14, fontweight='bold')
    
    COLOR_DIRECTO = '#2ecc71' 
    COLOR_INDIRECTO = '#3498db' 
    
    indirect_only_edges_for_coloring = [] 

    for i in range(NUM_NODES):
        for j in range(i + 1, NUM_NODES): 
            es_directa = (M_matrix[i, j] == 1)
            tiene_caminos_k = (M_k_result[i, j] > 0)
            
            u, v = i, j 
            
            if tiene_caminos_k and not es_directa:
                 indirect_only_edges_for_coloring.append((u, v))
            elif k == 1 and es_directa: # Si K=1, la única conexión que se dibuja es la directa (verde)
                 indirect_only_edges_for_coloring.append((u, v))

    
    # 1. Dibujar las aristas indirectas (AZULES DISCONTINUAS) GRUESAS PRIMERO (si K>1)
    if k > 1 and indirect_only_edges_for_coloring:
        nx.draw_networkx_edges(G, pos, edgelist=indirect_only_edges_for_coloring, width=3.0, edge_color=COLOR_INDIRECTO, alpha=0.7, style='dashed', ax=ax) 

    # 2. Dibujar las aristas directas (VERDES) DELGADAS ENCIMA (o si K=1, dibujar las verdes gruesas)
    if k == 1:
        # Si K=1, solo dibujamos las aristas directas (el contenido de indirect_only_edges_for_coloring es solo directo)
        nx.draw_networkx_edges(G, pos, edgelist=indirect_only_edges_for_coloring, width=3.0, edge_color=COLOR_DIRECTO, alpha=1.0, ax=ax)
    else:
        # Si K > 1, dibujamos el esqueleto (Verde) delgado debajo del Azul para contexto
        nx.draw_networkx_edges(G, pos, edgelist=original_edges_idx, width=1.5, edge_color=COLOR_DIRECTO, alpha=1.0, ax=ax)


    # 3. Dibujar Nodos y Etiquetas 
    labels = {i: NODES[i] for i in range(NUM_NODES)} 
    
    nx.draw_networkx_nodes(G, pos, node_color='#e74c3c', node_size=2000, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_color='white', font_weight='bold', font_size=10, ax=ax)

    # --- GLOSARIO DE CONEXIONES (LIMPIO) ---
    glosario = f"""
    [GLOSARIO]
    - Nodos: Personas en la Red.
    - Línea Verde Continua: Amistad Directa (K=1).
    - Línea Azul Discontinua: Conexión Indirecta (K={k}).
    """
    ax.text(0.5, -0.05, glosario.strip(),
             horizontalalignment='center', fontsize=10, 
             bbox=dict(facecolor='white', alpha=0.9, boxstyle='round'),
             transform=ax.transAxes)
    
    print(f"\n{Colors.RED}===================================================={Colors.ENDC}")
    time.sleep(0.5)
    print(">>> Gráfico generado. Cierre la ventana para finalizar. <<<")
    time.sleep(0.5)
    print(f"{Colors.RED}===================================================={Colors.ENDC}")
    plt.show()

if __name__ == "__main__":
    main()