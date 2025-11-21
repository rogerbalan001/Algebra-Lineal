import numpy as np
'''
El makarovChain es un objeto el cual se encarga de realizar la cadena de makarov para 
predecir la evolucion de estados de un sistema con el paso del tiempo.

Esta cadena se realiza de siguiente manera: 
Primero obtenemos los datos a analizar en funcion de los n estados los cuales van a generar 
una matriz estocastica que expresara la transicion de los estados con el paso del tiempo
Esta matriz es llamada, matriz de transicion de makarov

En esta matriz cada columna representa un estado y cada fila su cambio en funcion a si
algun estado es predominante a otro

Luego para poder hallar el estado estacionario del cambio para cada estado debemos de hallar un vector propio
de la matriz de transicion que de como suma de sus componentes 1. cada fila del vector representa la probabilidad 
de que en el futuro se cumplan alguno de los n estados a estudio.


Esta matriz debe de cumplir que
-> Sea cuadrada (nxn)
-> Sea estocastica (suma de los elementos de las filas igual a 1)
-> Todas sus componentes deben de ser positivas (R > 0)
'''

class MarkovChain:
    def __init__(self, states, transition_matrix):
        """
        Inicializa la cadena de Markov
        
        Args:
            states: Lista de nombres de estados ej: ['Soleado', 'Lluvioso']
            transition_matrix: Matriz de transición (cuadrada, filas suman 1 ya que es estocastico)
        """
        self.states = states
        self.P = np.array(transition_matrix)  
        self.validate_matrix()
    
    def validate_matrix(self):
        #Validar que es nxn
        if self.P.shape[0]!= self.P.shape[1]:  #Toma las filas de la matriz y sus columnas y las compara
            raise ValueError("La matriz debe de ser cuadrada") #genera mensaje de error si no se cumple
        
        
        #Verificar que sea estocastica
        row_sums = np.sum(self.P, axis=1)
        if not np.allclose(row_sums, 1.0, atol=1e-10): #Verifica si la suma de cada fila es 1
            print(f"Advertencia: Las filas no suman exactamente 1. Sumas: {row_sums}")
            print("Normalizando automáticamente...")
            self.P = self.P / row_sums[:, np.newaxis] #De no ser normaliza cada fila automaticamente
            
        #Verificar que los elementos de la matriz sean positivos
        if np.any(self.P < 0) or np.any(self.P > 1):
            raise ValueError("Debe ser una matriz de valores positivos")
        
        print("👌 Matriz valida")
    
    
    #Nuestro steady state sera el vector propio generado para nuestro lambda 1    
    def find_steady_state(self):
        """
        Encuentra el estado estacionario usando vectores propios
        
        Returns:
            Vector con probabilidades estacionarias para cada estado
        """
        
        eigenvalues, eigenvectors = np.linalg.eig(self.P.T)
        
        #Encuentra el vector propio con valor propio 1
        idx = np.argmin(np.abs(eigenvalues-1.0))
        steady_vector= np.real(eigenvectors[:, idx])
        
        #Normaliza el vector
        steady_vector  = np.abs(steady_vector) #toma valores absolutos
        steady_vector = steady_vector / np.sum(steady_vector)    
    
        return steady_vector
    
    def simulate_steps(self, initial_state, steps):
        """
        Simula la evolución del sistema paso a paso
        
        Args:
            initial_state: Estado inicial (índice)
            steps: Número de pasos a simular
            
        Returns:
            Lista con la evolución de estados
        """
        current_state = initial_state
        history = [current_state]
        
        for _ in range(steps):
            #Elegir proximo estado basado en probabilidades
            probs = self.P[current_state]
            next_state = np.random.choice(len(self.states), p= probs)
            history.append(next_state)
            
            # --- ¡ESTA ES LA LÍNEA CORREGIDA! ---
            # Actualiza el estado actual para el siguiente ciclo del bucle
            current_state = next_state 
            # -------------------------------------
        
        return history
    
    def multi_day_probabilities(self, days):
        """
        Calcula probabilidades para 'days' días en el futuro
        
        Args:
            days: Número de días en el futuro
            
        Returns:
            Matriz P^days donde P^n[i,j] = P(estar en j después de n días | empezar en i)
            
        Su diferencia es que en el simulate steps calculamos en base a datos alearorios del paso de los dias y
        En este caso calculamos los valores para cada dia usando el modelo y llegando a una predicion para una cantidad de dias que hayan pasado
        """
        
        return np.linalg.matrix_power(self.P, days)



''' Para luego :)!!
def plot_evolution(self, initial_state, steps):
        """
        Grafica la evolución del sistema y el estado estacionario
        """
        # Simular evolución
        history = self.simulate_steps(initial_state, steps)
        
        # Calcular estado estacionario teórico
        steady = self.find_steady_state()
        
        # Calcular frecuencias de la simulación
        freqs = np.bincount(history, minlength=len(self.states)) / len(history)
        
        # Crear gráficos
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Subplot 1: Evolución
        axes[0].plot(history, 'o-', alpha=0.7, markersize=4)
        axes[0].set_yticks(range(len(self.states)))
        axes[0].set_yticklabels(self.states)
        axes[0].set_title(f'Evolución del Sistema ({steps} pasos)')
        axes[0].set_xlabel('Tiempo')
        axes[0].set_ylabel('Estado')
        axes[0].grid(True, alpha=0.3)
        
        # Subplot 2: Estado estacionario vs simulación
        x = np.arange(len(self.states))
        width = 0.35
        
        axes[1].bar(x - width/2, steady, width, label='Teórico', alpha=0.7, color='blue')
        axes[1].bar(x + width/2, freqs, width, label='Simulado', alpha=0.7, color='red')
        
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(self.states)
        axes[1].set_ylabel('Probabilidad')
        axes[1].set_title('Estado Estacionario: Teórico vs Simulado')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for i, (s, f) in enumerate(zip(steady, freqs)):
            axes[1].text(i - width/2, s + 0.01, f'{s:.3f}', ha='center', va='bottom')
            axes[1].text(i + width/2, f + 0.01, f'{f:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        return steady, freq
'''