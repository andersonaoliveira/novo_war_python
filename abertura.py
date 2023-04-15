from graphics import *

def abertura():
    win = GraphWin("War", 800, 600)
    win.setBackground(color_rgb (0,0,0))
    
    jogar = Text(Point(400,50),"JOGO WAR")
    jogar.setTextColor(color_rgb(250,250,250))
    jogar.setStyle("bold")
    jogar.setSize(24)
    jogar.draw(win)
    
    caixaNome = Rectangle(Point(200,120),Point(600,240))
    caixaNome.setFill("white")
    caixaNome.setOutline("white")
    caixaNome.setWidth(3)
    caixaNome.draw(win)

    mensagemNome = Text(Point(400,140),"Insira seu nome e pressione ENTER")
    mensagemNome.setTextColor(color_rgb(0,0,0))
    mensagemNome.setStyle("bold")
    mensagemNome.setSize(12)
    mensagemNome.draw(win)

    campoNome = Entry(Point(400,190), 30)
    campoNome.setSize(16)
    campoNome.setFill("white")
    campoNome.draw(win)
    
    global listaDeCores
    listaDeCores = ["blue", "black", "purple", "red", "yellow", "green"]

    esperaEnter = "a"
    while esperaEnter != "Return":
        esperaEnter = win.getKey()
        global nomeDoJogador
        nomeDoJogador = campoNome.getText()

    mensagemNome.undraw()
    campoNome.undraw()
    caixaNome.undraw()

    caixaBoasVindas = Rectangle(Point(200,100),Point(600,140))
    caixaBoasVindas.setFill("white")
    caixaBoasVindas.setOutline("white")
    caixaBoasVindas.setWidth(3)
    caixaBoasVindas.draw(win)

    boasVindas = Text(Point(400,120),"Seja Bem Vindo {}".format(nomeDoJogador.upper()))
    boasVindas.setTextColor(color_rgb(0,0,0))
    boasVindas.setStyle("bold")
    boasVindas.setSize(16)
    boasVindas.draw(win)

    caixaEscolhaCor = Rectangle(Point(200,200),Point(600,500))
    caixaEscolhaCor.setFill("white")
    caixaEscolhaCor.setOutline("white")
    caixaEscolhaCor.setWidth(3)
    caixaEscolhaCor.draw(win)

    escolhaCor = Text(Point(400,220),"ESCOLHA A COR DO TEU EXERCITO")
    escolhaCor.setTextColor(color_rgb(0,0,0))
    escolhaCor.setStyle("bold")
    escolhaCor.setSize(12)
    escolhaCor.draw(win)

    caixaAzul = Rectangle(Point(225,250),Point(325,350))
    caixaAzul.setFill("blue")
    caixaAzul.setOutline("blue")
    caixaAzul.setWidth(3)
    caixaAzul.draw(win)

    caixaPreta = Rectangle(Point(350,250),Point(450,350))
    caixaPreta.setFill("black")
    caixaPreta.setOutline("black")
    caixaPreta.setWidth(3)
    caixaPreta.draw(win)

    caixaRoxa = Rectangle(Point(475,250),Point(575,350))
    caixaRoxa.setFill("purple")
    caixaRoxa.setOutline("purple")
    caixaRoxa.setWidth(3)
    caixaRoxa.draw(win)

    caixaVermelha = Rectangle(Point(225,370),Point(325,470))
    caixaVermelha.setFill("red")
    caixaVermelha.setOutline("red")
    caixaVermelha.setWidth(3)
    caixaVermelha.draw(win)

    caixaAmarela = Rectangle(Point(350,370),Point(450,470))
    caixaAmarela.setFill("yellow")
    caixaAmarela.setOutline("yellow")
    caixaAmarela.setWidth(3)
    caixaAmarela.draw(win)

    caixaVerde = Rectangle(Point(475,370),Point(575,470))
    caixaVerde.setFill("green")
    caixaVerde.setOutline("green")
    caixaVerde.setWidth(3)
    caixaVerde.draw(win)

    esperaClique = "a"
    global exercito_cor
    while esperaClique == "a":
        p = win.getMouse()
        x = p.x
        y = p.y
        if x>225 and x<325 and y>250 and y<350:
            exercito_cor = "blue"
            esperaClique = 0
        if x>350 and x<450 and y>250 and y<350:
            exercito_cor = "black"
            esperaClique = 0
        if x>475 and x<575 and y>250 and y<350:
            exercito_cor = "purple"
            esperaClique = 0
        if x>225 and x<325 and y>370 and y<470:
            exercito_cor = "red"
            esperaClique = 0
        if x>350 and x<450 and y>370 and y<470:
            exercito_cor = "yellow"
            esperaClique = 0
        if x>475 and x<575 and y>370 and y<470:
            exercito_cor = "green"
            esperaClique = 0

    p = 0
    x = 0
    y = 0
    caixaAzul.undraw()
    caixaPreta.undraw()
    caixaRoxa.undraw()
    caixaVermelha.undraw()
    caixaAmarela.undraw()
    caixaVerde.undraw()
    escolhaCor.undraw()

    corEscolhida = Text(Point(400,220),f'VOCE JOGARA COM O EXERCITO {exercito_cor.upper()}.')
    corEscolhida.setTextColor(color_rgb(0,0,0))
    corEscolhida.setStyle("bold")
    corEscolhida.setSize(12)
    corEscolhida.draw(win)

    caixaIniciar = Rectangle(Point(330,300),Point(470,360))
    caixaIniciar.setFill("green")
    caixaIniciar.setOutline("green")
    caixaIniciar.setWidth(3)
    caixaIniciar.draw(win)

    textoIniciar = Text(Point(400,330),"INICIAR")
    textoIniciar.setTextColor(color_rgb(0,0,0))
    textoIniciar.setStyle("bold")
    textoIniciar.setSize(20)
    textoIniciar.draw(win)

    iniciar = 0

    while iniciar == 0:
        p = win.getMouse()
        x = p.x
        y = p.y
        if x>350 and x<450 and y>300 and y<360:
            iniciar = 1            
            win.close()
            return (nomeDoJogador, exercito_cor)