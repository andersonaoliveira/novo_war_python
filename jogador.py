import exercitos

class Jogador:
    def __init__(self, nome, time):
        self.nome = nome
        self.time = time
        self.paises = []
        self.exercitos = 0
        self.cartas = {
            'azul': 0,
            'verde': 0,
            'vermelha': 0
        }
        
    def adicionar_pais(self, pais):
        self.paises.extend(pais)
        
    def remover_pais(self, pais):
        self.paises.remove(pais)
        
    def adicionar_exercitos(self, quantidade):
        self.exercitos += quantidade
        
    def remover_exercitos(self, quantidade):
        self.exercitos -= quantidade
        
    def quantidade_exercitos(self, exercitos):
        soma_exercitos = sum(exercitos[pais] for pais in self.paises)
        self.exercitos = soma_exercitos
        return self.exercitos
        
    def adicionar_carta(self, cor):
        self.cartas[cor] += 1
        
    def remover_cartas(self, cor):
        self.cartas[cor] -= 1