import random
import fronteiras, continentes, exercitos, posicoes
from jogador import Jogador

def sortear_dados_ataque_defesa(fronteiras, exercitos, atacante, defensor, pais_ataque, pais_defesa):       
    n_ataque = exercitos[f'{pais_ataque}']
    n_defesa = exercitos[f'{pais_defesa}']
    
    if regra_de_conter(atacante, defensor, pais_ataque, pais_defesa) == False:
        return
    if regra_de_player(atacante, defensor) == False:
        return    
    if regra_fronteira(fronteiras, pais_ataque, pais_defesa) == False:
        return
    if regra_exercitos(exercitos, pais_ataque) == False:
        return
        
    # Verificar limites de dados de ataque e defesa
    if n_ataque <= 3 and n_ataque > 1:
        n_ataque -= 1
    if n_ataque > 3:
        n_ataque = 3
    if n_defesa > 3:
        n_defesa = 3

    # Gerar listas aleatórias de dados de ataque e defesa
    dados_ataque = sorted(random.sample(range(1, 7), n_ataque), reverse=True)
    dados_defesa = sorted(random.sample(range(1, 7), n_defesa), reverse=True)

    # Calcular perdas de exércitos
    perdas_ataque = 0
    perdas_defesa = 0
    for i in range(min(n_ataque, n_defesa)):
        if dados_ataque[i] > dados_defesa[i]:
            perdas_defesa += 1
        else:
            perdas_ataque += 1    
    
    exercitos[f'{pais_ataque}'] -= perdas_ataque
    exercitos[f'{pais_defesa}'] -= perdas_defesa
    print (pais_defesa)
    
    if exercitos[f'{pais_defesa}'] == 0:
        exercitos[f'{pais_ataque}'] -= 1
        exercitos[f'{pais_defesa}'] += 1
        defensor.paises.remove(f'{pais_defesa}')
        atacante.paises.append(f'{pais_defesa}')
    print(dados_ataque, dados_defesa, perdas_ataque, perdas_defesa)
    return (dados_ataque, dados_defesa, perdas_ataque, perdas_defesa)

#teste se o time atacante possui o pais selecionado e se o país atacado possui o país selecionado
def regra_de_conter(atacante, defensor, pais_ataque, pais_defesa):
    if pais_ataque in atacante.paises:
        print ("país de ataque pertence ao usuário atacante")
        if pais_defesa in defensor.paises:
            print ("país de defesa pertence ao usuário defensor")
        else:
            return False
    else:
        return False

#teste de ataque ao exército do mesmo time
def regra_de_player(atacante, defensor):
    if atacante == defensor:
        print ('Você não pode atacar seu próprio território.')
        return False

#teste de fronteira
def regra_fronteira(fronteiras,pais_ataque, pais_defesa):
    if f'{pais_defesa}' in fronteiras.fronteiras[f'{pais_ataque}']:
        None
    else:
        print (f'{pais_ataque} não faz fronteira com {pais_defesa}.')
        return (False)
    
#teste de quantidade de exércitos
def regra_exercitos(exercitos,pais_ataque):
    print ("chegou aqui na regra_exercitos")
    if exercitos[f'{pais_ataque}'] <= 1:
        print (f'{pais_ataque} não tem exércitos suficientes para atacar.')
        return (False)