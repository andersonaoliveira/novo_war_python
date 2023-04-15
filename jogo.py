from graphics import *
import random
import time
import fronteiras, continentes, exercitos, posicoes
from sortear_paises import sortear_paises
from sortear_cores import sortear_cores
from alterar_exercitos import inicializar_exercitos, adicionar_exercitos, remover_exercitos
from sortear_ataque import sortear_dados_ataque_defesa, regra_de_conter, regra_de_player, regra_fronteira, regra_exercitos
from jogador import Jogador
from abertura import abertura

#Abertura que define o nome do usuário e a cor escolhida por ele.
usuario = abertura()

#cria o objeto jogador do usuário e define a cor escolhida pelo usuário
jogador_00 = Jogador(f'{usuario[0]}', f'{usuario[1]}')

#sorteia as cores que sobraram para distribuir aos demais usuários
cores = sortear_cores(usuario[1])

#realiza o sorteio dos países
sorteio = sortear_paises()

#define a cor de cada time do computador com base na lista aleatória gerada no método sortear_cores
jogador_01 = Jogador("Time 1", f'{cores[0]}')
jogador_02 = Jogador("Time 2", f'{cores[1]}')
jogador_03 = Jogador("Time 3", f'{cores[2]}')
jogador_04 = Jogador("Time 4", f'{cores[3]}')
jogador_05 = Jogador("Time 5", f'{cores[4]}')

#cria um array com os nomes dos jogadores para poder fazer a iteração
jogadores = [jogador_00, jogador_01, jogador_02, jogador_03, jogador_04, jogador_05]

for i in range(6):
    jogadores[i].adicionar_pais(sorteio[i]['paises'])

exercitos = inicializar_exercitos(exercitos)

def jogo(jogador_00, jogador_01, jogador_02, jogador_03, jogador_04, jogador_05, exercitos):
    win = GraphWin("War", 1000, 600)
    win.setBackground(color_rgb (0,0,0))
    
    fundo = Image(Point(500,300),'fundo.png')
    fundo.draw(win)

    menuJogador = Image(Point(500,556),"MenuJogador.png")
    menuJogador.draw(win)
    
    titulo = Text(Point(500,24),"JOGO WAR")
    titulo.setTextColor(color_rgb(250,250,250))
    titulo.setStyle("bold")
    titulo.setSize(24)
    titulo.draw(win)

    caixaTitulo = Rectangle(Point(0,45),Point(1000,50))
    caixaTitulo.setFill("red")
    caixaTitulo.setOutline("red")
    caixaTitulo.setWidth(3)
    caixaTitulo.draw(win)

    caixaObjetivo = Rectangle(Point(880,550),Point(980,580))
    caixaObjetivo.setFill("green")
    caixaObjetivo.setOutline("green")
    caixaObjetivo.setWidth(3)
    caixaObjetivo.draw(win)

    objetivo = Text(Point(930,565),"OBJETIVO")
    objetivo.setTextColor(color_rgb(250,250,250))
    objetivo.setSize(10)
    objetivo.draw(win)
    
    caixaAtacar = Rectangle(Point(803,462),Point(984,510))
    caixaAtacar.setFill("green")
    caixaAtacar.setOutline("green")
    caixaAtacar.setWidth(3)
    caixaAtacar.draw(win)

    atacar = Text(Point(894,485),"ATACAR")
    atacar.setTextColor(color_rgb(250,250,250))
    atacar.setSize(16)
    atacar.draw(win)

    caixaCartasParaTroca = Rectangle(Point(740,550),Point(870,580))
    caixaCartasParaTroca.setFill("green")
    caixaCartasParaTroca.setOutline("green")
    caixaCartasParaTroca.setWidth(3)
    caixaCartasParaTroca.draw(win)
        
    cartasParaTroca = Text(Point(805,565),"CARTAS TROCA")
    cartasParaTroca.setTextColor(color_rgb(250,250,250))
    cartasParaTroca.setSize(10)
    cartasParaTroca.draw(win) 

    textoJogador = Text(Point(385.5,564),"SEU\nTIME")
    textoJogador.setTextColor("white")
    textoJogador.setSize(10)
    textoJogador.draw(win)
    
    caixaJogador = Rectangle(Point(356,535),Point(415,593))
    caixaJogador.setFill(jogador_00.time)
    caixaJogador.setOutline(jogador_00.time)
    caixaJogador.setWidth(3)
    caixaJogador.draw(win)

    textoJogador = Text(Point(385.5,564),"SEU\nTIME")
    textoJogador.setTextColor("white")
    textoJogador.setSize(10)
    textoJogador.draw(win)
    
    caixaavancar = Rectangle(Point(417,516),Point(644,595))
    caixaavancar.setFill('green')
    caixaavancar.setOutline('black')
    caixaavancar.setWidth(1)
    caixaavancar.draw(win)

    textoavancar = Text(Point(530,555),"AVANÇAR")
    textoavancar.setTextColor("white")
    textoavancar.setSize(18)
    textoavancar.draw(win)
    
    ##################################
    global pais_ataque
    global player_atacante
    global pais_defesa
    global player_defensor
    
    pais_ataque = ""
    player_atacante = ""
    pais_defesa = ""
    player_defensor = ""
    
    # Essas serão as fases do jogo #
    global espera_ativo
    global preparacao_ativo
    global ataque_ativo
    global reposicionamento_ativo
    
    espera_ativo = True
    preparacao_ativo = False
    ataque_ativo = False
    reposicionamento_ativo = False
    
    ##################################
            
    #aqui vai desenhar um círculo em cada país, cada qual com a cor do time que representa
    for pais in posicoes.posicoes:
        pos_x = posicoes.posicoes[pais][0]
        pos_y = posicoes.posicoes[pais][1]
        quant_exercitos = exercitos[f'{pais}']
        jogadores = [jogador_00, jogador_01, jogador_02, jogador_03, jogador_04, jogador_05]
        for jogador in jogadores:
            if pais in jogador.paises:
                cor = jogador.time
        exercitos_por_local(win, cor, pos_x, pos_y, quant_exercitos)
    #---------------------------------------------------------------------------------------  
    while True:
        # MODO ESPERA ATIVO - SIGNIFICA QUE O USUÁRIO SÓ ESPERA AS JOGADAS AUTOMATIZADAS
        while espera_ativo == True:
            clique = win.getMouse()
            x = clique.x
            y = clique.y
            #BOTÃO AVANÇAR
            if x>417 and x<644 and y>516 and y<595:
                print ("Entrar no modo preparacao_ativo")
                espera_ativo = False
                preparacao_ativo = True
                
        # MODO PREPARACAO_ATIVO - SIGNIFICA QUE O USUÁRIO PRECISA POSICIONAR SEUS EXÉRCITOS - É A JOGADA ANTERIOR AO ATAQUE
        while preparacao_ativo == True:
            clique = win.getMouse()
            x = clique.x
            y = clique.y
            #BOTÃO AVANÇAR
            if x>417 and x<644 and y>516 and y<595:
                print ("Entrar no modo ataque_ativo")
                preparacao_ativo = False
                total_paises_antes_da_jogada = len(jogador_00.paises)
                ataque_ativo = True
        
        # MODO REPOSICIONAMENTO ATIVO - SIGNIFICA QUE O USUÁRIO PRECISA REPOSICIONAR SEUS EXÉRCITOS NO FINAL DO ROUND
        while reposicionamento_ativo == True:
            clique = win.getMouse()
            x = clique.x
            y = clique.y
            #BOTÃO AVANÇAR
            if x>417 and x<644 and y>516 and y<595:
                print ("Entrar no modo espera_ativo")
                reposicionamento_ativo = False
                espera_ativo = True     
        
        # MODO DE ATAQUE ATIVO - SIGNIFICA QUE O USUÁRIO PODE ATACAR EXÉRCITOS INIMIGOS EM REGIÃO DE FRONTEIRA AOS SEUS TERRITÓRIOS
        while ataque_ativo == True:
            clique = win.getMouse()
            x = clique.x
            y = clique.y
            #BOTÃO AVANÇAR
            if x>417 and x<644 and y>516 and y<595:
                print ("Entrar no modo reposicionamento_ativo")
                ataque_ativo = False
                #####################################################################################################################################################
                ### Este trecho serve para calcular se foi conquistado algum território e, se sim, é sorteado uma carta ao jogador diretamente na classe Jogador ####
                total_paises_depois_da_jogada = len(jogador_00.paises)
                if total_paises_depois_da_jogada > total_paises_antes_da_jogada:
                    cores_cartas = ['azul','verde','vermelha']
                    random.shuffle(cores_cartas)
                    jogador_00.adicionar_carta(f'{cores_cartas[0]}')
                print (jogador_00.cartas)
                #####################################################################################################################################################
                reposicionamento_ativo = True
                
            #ALVOS PARA VISUALIZAR OS CONTINENTES
            if x>230 and x<250 and y>65 and y<85:
                ampliar = Image(Point(500,300),"america-do-norte.png")
                ampliar.draw(win)
                aumentar(win)
                ampliar.undraw()
            if x>313 and x<332 and y>446 and y<466:
                ampliar = Image(Point(500,300),"america-do-sul.png")
                ampliar.draw(win)
                aumentar(win)
                ampliar.undraw()
            if x>457 and x<476 and y>122 and y<142:
                ampliar = Image(Point(500,300),'europa.png')
                ampliar.draw(win)
                aumentar(win)
                ampliar.undraw()
            if x>477 and x<496 and y>443 and y<463:
                ampliar = Image(Point(500,300),"africa.png")
                ampliar.draw(win)
                aumentar(win)
                ampliar.undraw()
            if x>765 and x<784 and y>303 and y<323:
                ampliar = Image(Point(500,300),"asia.png")
                ampliar.draw(win)
                aumentar(win)
                ampliar.undraw()
            if x>737 and x<756 and y>444 and y<464:
                ampliar = Image(Point(500,300),"oceania.png")
                ampliar.draw(win)
                aumentar(win)
                ampliar.undraw()
                
            #BOTÃO ATACAR
            if x>803 and x<984 and y>462 and y<510:
                if pais_ataque and player_atacante and pais_defesa and player_defensor != "":
                    ################################################ FAZ A JOGADA EM SI ######################################################
                    jogada = sortear_dados_ataque_defesa(fronteiras, exercitos, player_atacante, player_defensor, pais_ataque, pais_defesa)
                    print (jogada)
                    ##########################################################################################################################
                    try:
                        dadosAtaque.undraw()
                        dadosDefesa.undraw()
                    except:
                        None
                    textoExercitosAtaque.undraw()
                    textoExercitosDefesa.undraw()
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')   
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosDefesa.setSize(16)
                    textoExercitosAtaque.draw(win)
                    textoExercitosDefesa.draw(win)
                    try:
                        dados_ataque = jogada[0]
                        dados_defesa = jogada[1]
                        dadosAtaque = Text(Point(844,160),f'{dados_ataque}')
                        dadosDefesa = Text(Point(945,160),f'{dados_defesa}')
                        dadosAtaque.setTextColor("white")
                        dadosDefesa.setTextColor("white")
                        dadosAtaque.setSize(16)
                        dadosDefesa.setSize(16)
                        dadosAtaque.draw(win)
                        dadosDefesa.draw(win)
                    except:
                        print ("não teve jogada de dados") 
                else:
                    None
                
                ############Faz a atualização dos círculos com o respectivo time e exércitos a cada ataque  #####################
                for pais in posicoes.posicoes:
                    pos_x = posicoes.posicoes[pais][0]
                    pos_y = posicoes.posicoes[pais][1]
                    quant_exercitos = exercitos[f'{pais}']
                    jogadores = [jogador_00, jogador_01, jogador_02, jogador_03, jogador_04, jogador_05]
                    for jogador in jogadores:
                        if pais in jogador.paises:
                            cor = jogador.time
                    exercitos_por_local(win, cor, pos_x, pos_y, quant_exercitos)
                ################################################################################################################
                            
            #AMERICA DO SUL
            #seleciona a COLOMBIA
            if x>127 and x<183 and y>314 and y<345:            
                pais_selecionado = 'Colombia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o PERU    
            if x>127 and x<183 and y>347 and y<394:            
                pais_selecionado = 'Peru'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona a ARGENTINA    
            if x>127 and x<183 and y>396 and y<442:            
                pais_selecionado = 'Argentina'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o BRASIL    
            if x>185 and x<274 and y>330 and y<422:            
                pais_selecionado = 'Brasil'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            
            #AMERICA DO NORTE
            #seleciona o ALASCA  
            if x>28 and x<127 and y>87 and y<146:
                pais_selecionado = 'Alasca'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o VANCOUVER
            if x>65 and x<158 and y>148 and y<203:
                pais_selecionado = 'Vancouver'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o CALIFORNIA  
            if x>74 and x<158 and y>205 and y<257:
                pais_selecionado = 'California'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)            
            #seleciona o MEXICO     
            if x>112 and x<183 and y>259 and y<312:         
                pais_selecionado = 'Mexico'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)            
            #seleciona o MACKENZIE    
            if x>129 and x<274 and y>87 and y<146:            
                pais_selecionado = 'Mackenzie'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)  
            #seleciona o OTTAWA    
            if x>160 and x<223 and y>148 and y<203:            
                pais_selecionado = 'Ottawa'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)  
            #seleciona o NOVA IORQUE    
            if x>160 and x<223 and y>205 and y<257:
                pais_selecionado = 'NovaIorque'
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o GROELANDIA    
            if x>276 and x<354 and y>87 and y<142:            
                pais_selecionado = 'Groelandia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o LABRADOR        
            if x>225 and x<282 and y>167 and y<237:            
                pais_selecionado = 'Labrador'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
                    
            #EUROPA
            #seleciona o ISLANDIA
            if x>313 and x<356 and y>144 and y<180:
                pais_selecionado = 'Islandia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o INGLATERRA
            if x>313 and x<356 and y>182 and y<222:
                pais_selecionado = 'Inglaterra'
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o ESPANHA
            if x>313 and x<392 and y>224 and y<258:
                pais_selecionado = 'Espanha'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o SUECIA
            if x>358 and x<434 and y>144 and y<180:
                pais_selecionado = 'Suecia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o ALEMANHA
            if x>358 and x<392 and y>188 and y<222:
                pais_selecionado = 'Alemanha'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o POLONIA
            if x>394 and x<434 and y>182 and y<258:
                pais_selecionado = 'Polonia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o MOSCOU
            if x>436 and x<476 and y>144 and y<251:
                pais_selecionado = 'Moscou'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #ASIA
            #seleciona o OMSK
            if x>478 and x<544 and y>148 and y<210:
                pais_selecionado = 'Omsk'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o ARAL
            if x>478 and x<544 and y>212 and y<251:
                pais_selecionado = 'Aral'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o ORIENTE MEDIO
            if x>454 and x<534 and y>253 and y<293:
                pais_selecionado = 'OrienteMedio'
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o SIBERIA
            if x>546 and x<667 and y>122 and y<168:
                pais_selecionado = 'Siberia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o DUDINKA
            if x>546 and x<600 and y>170 and y<210:
                pais_selecionado = 'Dudinka'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o MONGOLIA
            if x>546 and x<600 and y>212 and y<251:
                pais_selecionado = 'Mongolia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o INDIA
            if x>536 and x<600 and y>253 and y<314:
                pais_selecionado = 'India'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o TCHITA
            if x>601 and x<667 and y>170 and y<210:
                pais_selecionado = 'Tchita'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o CHINA
            if x>601 and x<697 and y>212 and y<282:
                pais_selecionado = 'China'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o VIETNA
            if x>601 and x<666 and y>284 and y<337:
                pais_selecionado = 'Vietna'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o VLADIVOSTOK
            if x>669 and x<770 and y>122 and y<210:
                pais_selecionado = 'Vladivostok'
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o JAPAO
            if x>669 and x<745 and y>212 and y<301:
                pais_selecionado = 'Japao'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #AFRICA
            #seleciona o ARGELIA
            if x>313 and x<383 and y>294 and y<377:
                pais_selecionado = 'Argelia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o EGITO
            if x>385 and x<452 and y>274 and y<309:
                pais_selecionado = 'Egito'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o SUDAO
            if x>385 and x<471 and y>311 and y<357:
                pais_selecionado = 'Sudao'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o CONGO
            if x>385 and x<453 and y>359 and y<394:
                pais_selecionado = 'Congo'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o AFRICA DO SUL
            if x>385 and x<471 and y>396 and y<442:
                pais_selecionado = 'AfricadoSul'
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o MADAGASCAR
            if x>473 and x<512 and y>347 and y<406:
                pais_selecionado = 'Madagascar'
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #OCEANIA
            #seleciona o SUMATRA
            if x>601 and x<656 and y>339 and y<386:
                pais_selecionado = 'Sumatra'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o AUSTRALIA
            if x>627 and x<739 and y>388 and y<442:
                pais_selecionado = 'Australia'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o BORNEU
            if x>658 and x<709 and y>339 and y<386:
                pais_selecionado = 'Borneu'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)
            #seleciona o NOVA GUINE
            if x>711 and x<760 and y>339 and y<386:
                pais_selecionado = 'NovaGuine'            
                if pais_selecionado in jogador_00.paises:
                    try:
                        textoAtacante.undraw()
                        textoExercitosAtaque.undraw()
                    except:
                        None
                    pais_ataque = pais_selecionado        
                    exercitos_ataque = exercitos[f'{pais_ataque}']
                    textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
                    textoAtacante.setTextColor("white")
                    textoAtacante.setSize(10)
                    textoAtacante.draw(win)
                    textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
                    textoExercitosAtaque.setTextColor("white")
                    textoExercitosAtaque.setSize(16)
                    textoExercitosAtaque.draw(win)                
                    player_atacante = verifica_player(pais_ataque)
                    pais_ataque = pais_ataque
                    player_atacante = player_atacante
                    exercitos_ataque = exercitos_ataque
                    print (pais_ataque, player_atacante)
                else:        
                    try:
                        textoDefensor.undraw()
                        textoExercitosDefesa.undraw()
                    except:
                        None
                    pais_defesa = pais_selecionado
                    exercitos_defesa = exercitos[f'{pais_defesa}']
                    textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
                    textoDefensor.setTextColor("white")
                    textoDefensor.setSize(10)
                    textoDefensor.draw(win)
                    textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
                    textoExercitosDefesa.setTextColor("white")
                    textoExercitosDefesa.setSize(16)
                    textoExercitosDefesa.draw(win)
                    player_defensor = verifica_player(pais_defesa)
                    pais_defesa = pais_defesa
                    player_defensor = player_defensor
                    print (pais_defesa, player_defensor)

def aumentar(win):
    caixaPaisesDesseContinente = Rectangle(Point(200,125),Point(800,175))
    caixaPaisesDesseContinente.setFill("black")
    caixaPaisesDesseContinente.setOutline("black")
    caixaPaisesDesseContinente.setWidth(3)    
    caixaPaisesDesseContinente.draw(win)
    paisesDesseContinente = Text(Point(500,150),"PAISES DESSE CONTINENTE")
    paisesDesseContinente.setTextColor(color_rgb(250,250,250))
    paisesDesseContinente.setSize(24)
    paisesDesseContinente.draw(win)    
    win.getMouse()
    caixaPaisesDesseContinente.undraw()
    paisesDesseContinente.undraw()
    
def exercitos_por_local(win, cor, pos_x, pos_y, quant_exercitos):
    marcaPais = Circle(Point(pos_x,pos_y),15)
    marcaPais.setFill(cor)
    marcaPais.setOutline("black")
    marcaPais.draw(win)
    exercitoPais = Text(Point(pos_x,pos_y),quant_exercitos)
    if cor == "yellow":
        exercitoPais.setTextColor("black")
    else:
        exercitoPais.setTextColor("white")
    exercitoPais.setStyle("bold")
    exercitoPais.setSize(10)
    exercitoPais.draw(win)

def verificacao(pais_selecionado, win):    
    if pais_selecionado in jogador_00.paises:              
        pais_ataque = pais_selecionado        
        exercitos_ataque = exercitos[f'{pais_ataque}']
        textoAtacante = Text(Point(844,127.5),f'{pais_ataque}')
        textoAtacante.setTextColor("white")
        textoAtacante.setSize(10)
        textoAtacante.draw(win)
        textoExercitosAtaque = Text(Point(844,400),f'{exercitos_ataque}')
        textoExercitosAtaque.setTextColor("white")
        textoExercitosAtaque.setSize(16)
        textoExercitosAtaque.draw(win)                
        player_atacante = verifica_player(pais_ataque)
        return ("ataque", pais_ataque, player_atacante, exercitos_ataque)
    else:        
        pais_defesa = pais_selecionado
        exercitos_defesa = exercitos[f'{pais_defesa}']
        textoDefensor = Text(Point(945,127.5),f'{pais_defesa}')
        textoDefensor.setTextColor("white")
        textoDefensor.setSize(10)
        textoDefensor.draw(win)
        textoExercitosDefesa = Text(Point(945,400),f'{exercitos_defesa}')
        textoExercitosDefesa.setTextColor("white")
        textoExercitosDefesa.setSize(16)
        textoExercitosDefesa.draw(win)
        player_defensor = verifica_player(pais_defesa)
        return ("defesa", pais_defesa, player_defensor)
    
def verifica_player(pais):
    jogadores = [jogador_00, jogador_01, jogador_02, jogador_03, jogador_04, jogador_05]
    for jogador in jogadores:
        if pais in jogador.paises:
            return jogador
        
jogo(jogador_00, jogador_01, jogador_02, jogador_03, jogador_04, jogador_05, exercitos)