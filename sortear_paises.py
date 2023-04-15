import random

def sortear_paises():
    # lista de países disponíveis para serem sorteados
    paises_disponiveis = ['Brasil','Argentina','Colombia','Peru','Mexico','California','NovaIorque','Labrador','Ottawa','Vancouver','Mackenzie','Alasca','Groelandia','Islandia','Inglaterra','Suecia','Alemanha','Espanha','Polonia','Moscou','Argelia','Egito','Congo','Sudao','Madagascar','AfricadoSul','OrienteMedio','Aral','Omsk','Dudinka','Siberia','Tchita','Mongolia','Vladivostok','China','India','Japao','Vietna','Borneu','Sumatra','NovaGuine','Australia']
    
    # criar uma lista para cada time (incluindo o time do usuário)
    times = [{'nome': 'Time do usuário', 'paises': []}, {'nome': 'Time 1', 'paises': []}, {'nome': 'Time 2', 'paises': []}, {'nome': 'Time 3', 'paises': []}, {'nome': 'Time 4', 'paises': []}, {'nome': 'Time 5', 'paises': []}]
            
    # sortear países até que todos os países tenham sido distribuídos
    while paises_disponiveis:
        # para cada time, sorteie um país e adicione-o à lista de países do time
        for time in times:
            if paises_disponiveis:
                pais_sorteado = random.choice(paises_disponiveis)
                time['paises'].append(pais_sorteado)
                paises_disponiveis.remove(pais_sorteado)
        
    # retornar a lista de times com os países sorteados
    return times