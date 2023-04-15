import random

def sortear_cores(cor_escolhida):
    cores_disponiveis = ['blue','black','red','yellow','green','purple']
    cores_disponiveis.remove(f'{cor_escolhida}')
    random.shuffle(cores_disponiveis)
    
    return cores_disponiveis