import makarov as m

clima_matrix = [
    [0.7, 0.3],  # Si hoy soleado
    [0.5, 0.5]   # Si hoy lluvioso
]

clima = m.MarkovChain(["soleado", "lluvioso"], clima_matrix)
steady = clima.find_steady_state()

print(steady)

print(steady[0] + steady[1]) #Se cumple ley de probabilidad