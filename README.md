# 📊 SIMULADOR: Algoritmo de Conexión de Amistades 🤝

Este proyecto es un simulador interactivo que analiza una red social utilizando **Álgebra Lineal** (específicamente la matriz de adyacencia elevada a la potencia $K$, es decir, $M^K$) para descubrir conexiones directas e indirectas entre personas. Adicionalmente, genera una visualización gráfica de la topología de la red mediante grafos.

---

## 🛠️ Requisitos del Sistema y Preparación

Para ejecutar este código en otra máquina, necesitas tener instalado **Python 3.8 o superior** y las librerías de terceros especificadas en las importaciones.

### 1. Clonar o Copiar los Archivos Locales
Asegúrate de que los siguientes archivos estén ubicados en el mismo directorio de trabajo:
*   `main_app.py` *(el script principal que proporcionaste)*
*   `social_network_model.py` *(módulo local obligatorio que contiene las funciones de la matriz y la clase `Colors`)*

> ⚠️ **Importante:** Si no incluyes `social_network_model.py` en la misma carpeta, el programa lanzará un error de tipo `ModuleNotFoundError`.

### 2. Instalación de Dependencias

#### Opción A: Instalación rápida por consola
Abre la terminal o línea de comandos en la ruta del proyecto y ejecuta:
```bash
pip install -r requirements.txt