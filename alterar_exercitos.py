import exercitos

def inicializar_exercitos(exercitos):
    exercitos = exercitos.exercitos
    for pais in exercitos:
        exercitos[pais] = 5
    return exercitos

def adicionar_exercitos(exercitos, pais, quantidade):
    exercitos[pais] += quantidade
    return exercitos
    
    
def remover_exercitos(exercitos, pais, quantidade):
    exercitos[pais] -= quantidade
    return exercitos
