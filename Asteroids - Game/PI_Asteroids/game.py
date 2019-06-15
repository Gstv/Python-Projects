"""
REFERENCIAS:
Bordas - https://www.youtube.com/watch?v=jUct8hqAb9U&list=PLzn2mIpnKXEo0iiFrlqv-fFAbRd0cjDLe&index=7
Score - https://www.youtube.com/watch?v=rYhi-74kELw&list=PLzn2mIpnKXEo0iiFrlqv-fFAbRd0cjDLe&index=13
Classes - As classes foram uma adptação do código Asteroids_master anexado na pasta de referencia,
assim como alguns trechos de codigo usados para funcionamento das mesmas
Interface Geral (Playlist inteira) - https://www.youtube.com/watch?v=ujOTNg17LjI&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO&index=1
"""

import pygame
import math
import random
from pygame import mixer

# CORES
verde = (0, 255, 0)
branco = (255, 255, 255)
branco2 = (200, 200, 200)
preto = (0, 0, 0)
azul = (0, 200, 200)
vermelho = (255, 0, 0)

# TELA
largura = 800
altura = 600

# INICIALIZACOES
jogador_tam = 10
fd_fric = 0.5
bd_fric = 0.1
velocidade_max = 10
velocidade_bala = 18
rotacao_max = 10
vel_OVNI = 5
mira_OVNI = 10
usprite = pygame.image.load("ufo.png")
boom = pygame.image.load("ex2.png")
power = pygame.image.load("power.png")
boom = pygame.transform.scale(boom, [35,35])

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Asteroids")
frames = pygame.time.Clock()

def limiteX(x):
    if x > largura:
        x = 0
    if x < 0:
        x = largura
    return x

def limiteY(y):
    if y > altura:
        y = 0
    if y < 0:
        y = altura
    return y

def scores(texto):
    font = pygame.font.Font("Square.ttf", 22) #importa fonte
    texto1 = font.render(str(texto), True, branco) #Converte int para String, define cor...
    texto2 = font.render("Score:", True, branco)
    tela.blit(texto2, [18, 5])
    tela.blit(texto1, [95, 5]) #imprime Texto

def colisao(x, y, xTo, yTo, tam):
    if x > xTo - tam and x < xTo + tam and y > yTo - tam and y < yTo + tam:
        return True
    return False

def colisaoCirculo(x,y, xTo, yTo, raio, raioTo):
    distancia = math.sqrt(math.pow((x-xTo),2)+math.pow((y-yTo),2))
    if distancia < raio + raioTo:
        return True
    return False

#Classes extraidas do projeto
class Asteroid:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        if t == "Grande":
            self.tam = 22
        elif t == "Normal":
            self.tam = 12
        else:
            self.tam = 7
        self.t = t

        self.velocidade = random.uniform(1, (40 - self.tam) * 4 / 15)
        self.angulo = random.randrange(0, 360) * math.pi / 180

    def atualizaAsteroid(self):
        self.x += self.velocidade * math.cos(self.angulo)
        self.y += self.velocidade * math.sin(self.angulo)

        self.x = limiteX(self.x)
        self.y = limiteY(self.y)

        pygame.draw.circle(tela, branco, [int(self.x),int(self.y)],self.tam,1)

class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.tempo = 30

    def atualizaTiro(self):
        self.x += velocidade_bala * math.cos(self.angulo * math.pi / 180)
        self.y += velocidade_bala * math.sin(self.angulo * math.pi / 180)

        pygame.draw.rect(tela, branco, [int(self.x), int(self.y), 3, 3])

        self.x = limiteX(self.x)
        self.y = limiteY(self.y)
        self.tempo -= 1

class Ovnis:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = "Morto"
        self.type = "Grande"
        self.dirchoice = ()
        self.bullets = []
        self.cd = 0
        self.bdir = 0
        self.soundDelay = 0

    def atualizaOvni(self):
        # Move player
        self.x += vel_OVNI * math.cos(self.dir * math.pi / 180)
        self.y += vel_OVNI * math.sin(self.dir * math.pi / 180)

        # Choose random direction
        if random.randrange(0, 100) == 1:
            self.dir = random.choice(self.dirchoice)

        # Wrapping
        self.y = limiteY(self.y)
        if self.x < 0 or self.x > largura:
            self.state = "Morto"

        # Shooting
        if self.type == "Grande":
            self.bdir = random.randint(0, 360)
        if self.cd == 0:
            self.bullets.append(Tiro(self.x, self.y, self.bdir))
            self.cd = 30
        else:
            self.cd -= 1

    def criaOvni(self):
        # cria ovni
        # define estado

        self.state = "Vivo"

        # envia para posicao aleatoria
        self.x = random.choice((0, largura))
        self.y = random.randint(0, altura)

        # define tipo aleatorio
        if random.randint(0, 1) == 0:
            self.type = "Grande"
            self.size = 20
        else:
            self.type = "Pequeno"
            self.size = 10

        # cria direcao aleatoria
        if self.x == 0:
            self.dir = 0
            self.dirchoice = (0, 45, -45)
        else:
            self.dir = 180
            self.dirchoice = (180, 135, -135)

        # reseta disparos
        self.cd = 0


    def desenhaOvni(self):
        # Desenha ovnis
        ufo = pygame.draw.rect(tela, preto, [self.x, self.y, self.size, self.size])
        tela.blit(usprite, ufo)


class Jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.angulo = -90
        self.rotacao = 0
        self.arrasto = False

    def atualizaJogador(self):
        # Move player
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.arrasto:
            if speed + fd_fric < velocidade_max:
                self.hspeed += fd_fric * math.cos(self.angulo * math.pi / 180)
                self.vspeed += fd_fric * math.sin(self.angulo * math.pi / 180)
            else:
                self.hspeed = velocidade_max * math.cos(self.angulo * math.pi / 180)
                self.vspeed = velocidade_max * math.sin(self.angulo * math.pi / 180)
        else:
            if speed - bd_fric > 0:
                change_in_hspeed = (bd_fric * math.cos(self.vspeed / self.hspeed))
                change_in_vspeed = (bd_fric * math.sin(self.vspeed / self.hspeed))
                if self.hspeed != 0:
                    if change_in_hspeed / abs(change_in_hspeed) == self.hspeed / abs(self.hspeed):
                        self.hspeed -= change_in_hspeed
                    else:
                        self.hspeed += change_in_hspeed
                if self.vspeed != 0:
                    if change_in_vspeed / abs(change_in_vspeed) == self.vspeed / abs(self.vspeed):
                        self.vspeed -= change_in_vspeed
                    else:
                        self.vspeed += change_in_vspeed
            else:
                self.hspeed = 0
                self.vspeed = 0
        self.x += self.hspeed
        self.y += self.vspeed

        # Check for wrapping
        self.x = limiteX(self.x)
        self.y = limiteY(self.y)

        # Rotate player
        self.angulo += self.rotacao

    def desenhaJogador(self):

        a = math.radians(self.angulo)
        x = self.x
        y = self.y
        s = jogador_tam
        calda = self.arrasto
        # Draw player
        pygame.draw.line(tela, branco,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(tela, branco,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                          y + (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(tela, branco,
                         (x - (s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                          y - (s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                         (x - (s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                          y + (s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))
        if calda:
            pygame.draw.line(tela, branco,
                             (x - s * math.cos(a),
                              y - s * math.sin(a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(a + math.pi / 6),
                              y - (s * math.sqrt(5) / 4) * math.sin(a + math.pi / 6)))
            pygame.draw.line(tela, branco,
                             (x - s * math.cos(-a),
                              y + s * math.sin(-a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(-a + math.pi / 6),
                              y + (s * math.sqrt(5) / 4) * math.sin(-a + math.pi / 6)))


class Escudo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 60 #Tempo definido pela multiplicação do clock do jogo pela quantia de segundos
        self.raio = 15

    def atualizaEscudo(self, x, y):
        self.x = x
        self.y = y
        self.altura = 30
        self.largura = 30

        self.x = limiteX(self.x)
        self.y = limiteY(self.y)

        pygame.draw.circle(tela, azul, [int(self.x), int(self.y)], self.raio, 1)

        self.time -= 1

class Buffs:
    def __init__(self):
        self.x = random.randint(20, largura-20)
        self.y = -20
    def atualizaBuff(self):
        sp = pygame.draw.rect(tela, preto, [self.x, self.y,20,20])
        tela.blit(power, sp)
        self.y += 3

def buttonOptions(action, x0, xf, y0, yf, funcao):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    optionsFont = pygame.font.Font("Square.ttf", 40)
    t = optionsFont.render(action, True, branco)

    if xf > mouse[0] > x0 and yf > mouse[1] > y0:
        t = optionsFont.render(action, True, verde)
        if click[0] == 1 and action == "CONTINUE":
            return "unpause"
        elif click[0] == 1 and action == "BACK":
            return "back"
        elif click[0] == 1 and action == "HIGH SCORES":
            return "on"
        elif click[0] == 1 and action == "CONTROLS":
            return "sim"
        elif click[0] == 1 and action == "SOUNDS":
            return "sim"
        elif click[0] == 1 and action == "YES":
            return "sim"
        elif click[0] == 1 and action == "NO":
            return "nao"
        elif click[0] == 1 and action == "EASY":
            return 1
        elif click[0] == 1 and action == "MEDIUM":
            return 3
        elif click[0] == 1 and action == "HARD":
            return 6
        elif click[0] == 1 and action == "1º WASD AND ENTER":
            return "sim"
        elif click[0] == 1 and action == "2º ARROWS AND SPACE":
            return "sim"
        elif click[0] == 1:
            funcao()

    tela.blit(t, [x0, y0])

def gameOver():
    gameOver = True

    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        tela.fill(preto)
        titleFont = pygame.font.Font("Square.ttf", 120)

        titulo = titleFont.render("GAME OVER", True, branco)
        tela.blit(titulo, [104, 55])

        buttonOptions("PLAY AGAIN", 300, 500, 300, 335, gameLoop)
        buttonOptions("MAIN MENU", 310, 500, 350, 385, game_Intro)

        pygame.display.update()

def efeitosSonoros(ligado, origem):
    somColisao = mixer.Sound('colisao.ogg')
    somTiro = mixer.Sound('tiro.ogg')
    somPower = mixer.Sound('extra.wav')

    if ligado == "sim":
        if origem == "colisao":
            somColisao.play()
        if origem == "tiro":
            somTiro.play()
        if origem == "power":
            somPower.play()


def game_Intro():
    intro = True
    highscore = ""
    back = ""

    pygame.mixer.music.load('musicamenu.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        tela.fill(preto)
        titleFont = pygame.font.Font("Square.ttf", 120)

        # TELA INICIAL

        titulo = titleFont.render("ASTEROIDS", True, branco)
        tela.blit(titulo, [104, 55])

        buttonOptions("PLAY", 355, 445, 305, 340, gameLoop)
        highscore = buttonOptions("HIGH SCORES", 285, 510, 355, 390, highscore)
        buttonOptions("QUIT", 358, 435, 405, 440, quit)


        #TELA HIGH SCORE

        while highscore == "on":
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                if back == "back":
                    highscore = "off"

            tela.fill(preto)
            titleFont = pygame.font.Font("Square.ttf", 120)
            optionsFont = pygame.font.Font("Square.ttf", 40)

            titulo = titleFont.render("HIGH SCORE", True, branco)
            num = optionsFont.render("Nº", True, branco)
            name = optionsFont.render("NAME", True, branco)
            score = optionsFont.render("SCORE", True, branco)

            tela.blit(titulo, [95, 55])
            tela.blit(num, [98, 205])
            tela.blit(name, [180, 205])
            tela.blit(score, [590, 205])

            pygame.draw.line(tela, branco, (92, 250), (710, 250), 4) #Linha topo horizontal
            pygame.draw.line(tela, branco, (92, 520), (710, 520), 4) #Linha bot horizontal
            pygame.draw.line(tela, branco, (92, 250), (92, 520), 4) #Linha esq vertical
            pygame.draw.line(tela, branco, (710, 250), (710, 520), 4) #Linha dir vertical

            back = buttonOptions("BACK", 354, 450, 530, 565, back)

            pygame.display.update()

        pygame.display.update()

def gameLoop():

    jogo = True
    select= True
    wasd = False
    player_state = "Vivo"
    next_level_delay = 0
    tiros_max = 5
    tiros = []
    asteroids = []
    escudo = False
    triplo = False
    easy = 0
    medium = 0
    hard = 0
    fase = 1
    mostraFase = 1
    buffTiro = 0
    shield = []
    score = 0
    effects = "sim"
    vidas = 2
    dificuldade = 0
    jogador = Jogador(largura / 2, altura / 2)
    ovni = Ovnis()
    powerUp = []


    while select:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if easy == 1 or medium == 3 or hard == 6:
                select = False

        tela.fill(preto)
        titleFont = pygame.font.Font("Square.ttf", 120)

        titulo = titleFont.render("DIFFICULTY", True, branco)
        tela.blit(titulo, [105, 55])

        easy = buttonOptions("EASY", 355, 445, 350, 385, easy)
        medium = buttonOptions("MEDIUM", 335, 470, 400, 435, medium)
        hard = buttonOptions("HARD", 358, 455, 450, 485, hard)

        if easy == 1:
            fase = easy
        if medium == 3:
            fase = medium
        if hard == 6:
            fase = hard

        pygame.display.update()

    while jogo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F5:
                    if wasd:
                        wasd = False
                    else:
                        wasd = True
                if wasd:
                    if e.key == pygame.K_w:
                        jogador.arrasto = True
                    if e.key == pygame.K_a:
                        jogador.rotacao = -rotacao_max
                    if e.key == pygame.K_d:
                        jogador.rotacao = rotacao_max
                    if e.key == pygame.K_RETURN and len(tiros) < tiros_max:
                        if triplo:
                            efeitosSonoros(effects, "tiro")
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo + 25))
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo))
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo - 25))
                        else:
                            efeitosSonoros(effects, "tiro")
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo))

                else:
                    if e.key == pygame.K_UP:
                        jogador.arrasto = True
                    if e.key == pygame.K_LEFT:
                        jogador.rotacao = -rotacao_max
                    if e.key == pygame.K_RIGHT:
                        jogador.rotacao = rotacao_max
                    if e.key == pygame.K_SPACE and len(tiros) < tiros_max:
                        if triplo:
                            efeitosSonoros(effects, "tiro")
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo + 25))
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo))
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo - 25))
                        else:
                            efeitosSonoros(effects, "tiro")
                            tiros.append(Tiro(jogador.x, jogador.y, jogador.angulo))

                    if e.key == pygame.K_e:
                        shield.append(Escudo(jogador.x, jogador.y))
                        escudo = True
                    if e.key == pygame.K_t:
                        triplo = True
                        buffTiro = 90  # Tempo do buff

                if e.key == pygame.K_ESCAPE:
                    pause = True
                    paused = ""
                    backPause = ""
                    backControls = ""
                    backSounds = ""
                    controle = ""
                    sounds = ""
                    masterYes = ""
                    masterNo = ""
                    musicYes = ""
                    musicNo = ""
                    effectsYes = ""
                    effectsNo = ""
                    wasdT = ""
                    setasT = ""

                    #TELA DE PAUSE

                    while pause:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                quit()
                            if e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_ESCAPE:
                                    pause = False
                            if controle == "wasd":
                                wasd = True
                            if paused == "unpause":
                                pause = False
                            if backPause == "back":
                                jogo = False
                                pause = False

                        tela.fill(preto)
                        titleFont = pygame.font.Font("Square.ttf", 120)

                        titulo = titleFont.render("PAUSE", True, branco)
                        tela.blit(titulo, [225, 55])

                        paused = buttonOptions("CONTINUE", 315, 485, 300, 335, paused)
                        sounds = buttonOptions("SOUNDS", 332, 470, 350, 385, sounds)
                        controle = buttonOptions("CONTROLS", 308, 495, 405, 440, controle)
                        backPause = buttonOptions("BACK", 358, 450, 455, 490, backPause)

                        pygame.display.update()

                        # TELA DE CONTROLE

                        loopControls= None
                        if controle == "sim":
                            loopControls = True

                        while loopControls:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    quit()
                                if backControls == "back":
                                    loopControls = False

                            tela.fill(preto)
                            titleFont = pygame.font.Font("Square.ttf", 120)

                            titulo = titleFont.render("CONTROLS", True, branco)
                            tela.blit(titulo, [124, 55])

                            wasdT = buttonOptions("1º WASD AND ENTER", 204, 575, 290, 325, wasdT)
                            setasT = buttonOptions("2º ARROWS AND SPACE", 204, 600, 350, 385, setasT)
                            backControls = buttonOptions("BACK", 354, 450, 500, 535, backControls)

                            if wasdT == "sim":
                                wasd = True
                            if setasT == "sim":
                                wasd = False

                            if wasd:
                                pygame.draw.circle(tela, verde, (154, 310), 9, 0)
                            else:
                                pygame.draw.circle(tela, verde, (154, 370), 9, 0)

                            pygame.display.update()


                        #TELA DE SOUNDS
                        master = True
                        music = True
                        effect = True

                        loopSounds = None
                        if sounds == "sim":
                            loopSounds = True

                        while loopSounds:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    quit()
                                if backSounds == "back":
                                    loopSounds = False

                            tela.fill(preto)
                            titleFont = pygame.font.Font("Square.ttf", 120)
                            optionsFont = pygame.font.Font("Square.ttf", 40)

                            titulo = titleFont.render("SOUNDS", True, branco)
                            masterT = optionsFont.render("MASTER VOLUME", True, branco)
                            musicT = optionsFont.render("MUSIC VOLUME", True, branco)
                            effectsT = optionsFont.render("SOUNDS EFFECTS", True, branco)

                            tela.blit(titulo, [194, 55])
                            tela.blit(masterT, [110, 255])
                            tela.blit(musicT, [110, 305])
                            tela.blit(effectsT, [110, 355])

                            # QUADRADOS DE INTERACAO COM A ESCOLHA

                            if master:
                                pygame.draw.rect(tela, branco2, [490, 255, 75, 40])
                            else:
                                pygame.draw.rect(tela, branco2, [610, 255, 75, 40])

                            if music:
                                pygame.draw.rect(tela, branco2, [490, 305, 75, 40])
                            else:
                                pygame.draw.rect(tela, branco2, [610, 305, 75, 40])

                            if effect:
                                pygame.draw.rect(tela, branco2, [490, 355, 75, 40])
                            else:
                                pygame.draw.rect(tela, branco2, [610, 355, 75, 40])


                            masterYes = buttonOptions("YES", 490, 560, 255, 290, masterYes)
                            masterNo = buttonOptions("NO", 620, 665, 255, 290, masterNo)
                            musicYes = buttonOptions("YES", 490, 560, 305, 340, musicYes)
                            musicNo = buttonOptions("NO", 620, 665, 305, 340, musicNo)
                            effectsYes = buttonOptions("YES", 490, 560, 355, 390, effectsYes)
                            effectsNo = buttonOptions("NO", 620, 665, 355, 390, effectsNo)

                            backSounds = buttonOptions("BACK", 110, 210, 505, 540, backSounds)

                            if masterNo == "nao":
                                pygame.mixer.music.pause()
                                effects = masterNo
                                master = False
                            if masterYes == "sim":
                                pygame.mixer.music.unpause()
                                effects = masterYes
                                master = True
                            if musicNo == "nao":
                                pygame.mixer.music.pause()
                                music = False
                            if musicYes == "sim":
                                pygame.mixer.music.unpause()
                                music = True
                            if effectsNo == "nao":
                                effects = effectsNo
                                effect = False
                            if effectsYes == "sim":
                                effects = effectsYes
                                effect = True

                            pygame.display.update()

            if e.type == pygame.KEYUP:
                if wasd:
                    if e.key == pygame.K_w:
                        jogador.arrasto = False
                    if e.key == pygame.K_a or e.key == pygame.K_d:
                        jogador.rotacao = 0
                else:
                    if e.key == pygame.K_UP:
                        jogador.arrasto = False
                    if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                        jogador.rotacao = 0

        # atualiza jogador
        jogador.atualizaJogador()

        tela.fill(preto)

        font = pygame.font.Font("Square.ttf", 22)
        texto1 = font.render(str(mostraFase-1), True, branco)
        texto2 = font.render("Fase:", True, branco)
        tela.blit(texto2, [700, 5])
        tela.blit(texto1, [760, 5])

        if len(shield) > 0:
            shield[0].atualizaEscudo(jogador.x, jogador.y)
            if shield[0].time <= 0:
                try:
                    shield.pop(0)
                    if len(shield) == 0:
                        escudo = False
                except ValueError:
                    continue

        buffTiro -= 1
        if buffTiro < 0:
            triplo = False
            tiros_max = 5

        if random.randint(0, 500) == 4:
            efeitosSonoros(effects, "power")
            powerUp.append(Buffs())

        if len(powerUp) > 0:
            powerUp[0].atualizaBuff()
            try:
                if len(powerUp) > 1:
                    try:
                        powerUp.pop(0)
                    except ValueError:
                        continue
                if colisao(jogador.x, jogador.y, powerUp[0].x, powerUp[0].y, 20):
                    if random.randint(0, 1) == 1:
                        shield.append(Escudo(jogador.x, jogador.y))
                        escudo = True
                    else:
                        triplo = True
                        buffTiro = 90  # Tempo de duração do buff clock*segundos
                    try:
                        powerUp.pop(0)
                    except ValueError:
                        continue
            except ValueError:
                continue

        #Verifica colisao com asteroide
        for a in asteroids:
            a.atualizaAsteroid()
            if player_state != "Morreu":
                if not escudo:
                     if colisao(jogador.x, jogador.y, a.x, a.y, a.tam):
                         tela.blit(boom, [jogador.x, jogador.y, 50, 50])
                         efeitosSonoros(effects, "colisao")
                         pygame.display.flip()
                         pygame.time.delay(200)
                         jogador.x = largura / 2
                         jogador.y = altura / 2

                         if vidas != 0:
                             vidas -= 1
                         else:
                             jogo = False
                             gameOver()

                         # Divide asteroid
                         if a.t == "Grande":
                             asteroids.append(Asteroid(a.x, a.y, "Normal"))
                             asteroids.append(Asteroid(a.x, a.y, "Normal"))
                             score += 20
                         elif a.t == "Normal":
                             asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                             asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                             score += 50
                         else:
                             score += 100
                         asteroids.remove(a)
                else:
                     if colisaoCirculo(shield[0].x,shield[0].y, a.x, a.y, shield[0].raio, a.tam):
                         vel = a.velocidade
                         ang = a.angulo
                         if a.velocidade > -2.66:
                             a.velocidade = -vel*1.3
                         a.angulo = -ang+math.radians(45)
                         jogador.hspeed = 0
                         jogador.vspeed = 0

        if len(asteroids) == 0 and ovni.state == "Morto":
            if next_level_delay < 30:
                next_level_delay += 1

            else:
                if mostraFase > 1:
                    tela.fill(preto)
                    font = pygame.font.Font("Square.ttf", 30)
                    concs = font.render("Fase concluida!", True, branco)
                    tela.blit(concs, [largura/2-120, altura/2-30])
                    pygame.display.flip()
                    pygame.time.delay(2500)
                mostraFase += 1
                fase += 1
                dificuldade = 0
                # Cria asteroid longe do centro
                for i in range(fase):
                    xTo = largura / 2
                    yTo = altura / 2
                    while xTo - largura / 2 < largura / 4 and yTo - altura / 2 < altura / 4:
                        xTo = random.randrange(0, largura)
                        yTo = random.randrange(0, altura)
                    asteroids.append(Asteroid(xTo, yTo, "Grande"))
                next_level_delay = 0

        # Aumenta dificuldade
        if dificuldade < fase * 450:
            dificuldade += 1

        # Ovni
        if ovni.state == "Morto":
            if random.randint(0, 6000) <= (dificuldade * 2) / (fase * 9) and next_level_delay == 0:
                ovni.criaOvni()
                # So cria naves pequenas >40000
                if score >= 40000:
                    ovni.type = "Pequeno"
        else:
            # Define o angulo de disparo do ovni
            acc = mira_OVNI * 4 / fase
            ovni.bdir = math.degrees(math.atan2(-ovni.y + jogador.y, -ovni.x + jogador.x) + math.radians(random.uniform(acc, -acc)))

            ovni.atualizaOvni()
            ovni.desenhaOvni()

            # Verifica colisao com asteroids
            for a in asteroids:
                if colisao(ovni.x, ovni.y, a.x, a.y, a.tam + ovni.size):
                    # estado do ovni
                    ovni.state = "Morto"

                    # divide asteroids
                    if a.t == "Grande":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                        asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                    asteroids.remove(a)

            # verifica colisao com as balas
            for b in tiros:
                if colisao(b.x, b.y, ovni.x, ovni.y, ovni.size):
                    # soma pontos
                    if ovni.type == "Grande":
                        score += 200
                    else:
                        score += 1000

                    # define estado do ovni
                    ovni.state = "Morto"

                    # Remove bala
                    tiros.remove(b)

            # verifica colisao do ovni com o jogador
            if colisao(ovni.x, ovni.y, jogador.x, jogador.y, ovni.size):
                if not escudo:
                    if player_state != "Morreu":
                        tela.blit(boom, [jogador.x, jogador.y, 50, 50])
                        efeitosSonoros(effects, "colisao")
                        pygame.display.flip()
                        pygame.time.delay(200)
                        jogador.x = largura / 2
                        jogador.y = altura / 2
                        if vidas != 0:
                            vidas -= 1
                        else:
                            jogo = False
                            gameOver()

            # tiros ovni
            for b in ovni.bullets:
                # atualiza tiros
                b.atualizaTiro()

                # verifica colisao com asteroids
                for a in asteroids:
                    if colisao(b.x, b.y, a.x, a.y, a.tam):
                        # divide asteroide
                        if a.t == "Grande":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))

                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                            asteroids.append(Asteroid(a.x, a.y, "Pequeno"))

                        # remove asteroid e bala
                        asteroids.remove(a)
                        ovni.bullets.remove(b)

                        break

                # verifica colisao com jogador
                if colisao(jogador.x, jogador.y, b.x, b.y, 5):
                    if player_state != "Morreu":
                        if not escudo:
                            tela.blit(boom, [jogador.x, jogador.y, 50, 50])
                            efeitosSonoros(effects, "colisao")
                            pygame.display.flip()
                            pygame.time.delay(200)
                            jogador.x = largura / 2
                            jogador.y = altura / 2
                            if vidas != 0:
                                vidas -= 1
                            else:
                                gameOver()

                            # Remove tiro
                            ovni.bullets.remove(b)

                if b.tempo <= 0:
                    try:
                        ovni.bullets.remove(b)
                    except ValueError:
                        continue

        # tiros
        for b in tiros:
            # atualiza tiros
            b.atualizaTiro()

            # verifica se os tiros colidiram com asteroide
            for a in asteroids:
                if b.x > a.x - a.tam and b.x < a.x + a.tam and b.y > a.y - a.tam and b.y < a.y + a.tam:
                    # Divide asteroid
                    if a.t == "Grande":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20

                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                        asteroids.append(Asteroid(a.x, a.y, "Pequeno"))
                        score += 50

                    else:
                        score += 100
                    asteroids.remove(a)
                    tiros.remove(b)

                    break

            # Destroi tiros
            if b.tempo <= 0:
                try:
                    tiros.remove(b)
                except ValueError:
                    continue

        # HUD
        for v in range(vidas + 1):
            Jogador(25 + v * 26, 45).desenhaJogador()
        scores(score)

        #Desenha Nave
        jogador.desenhaJogador()
        pygame.display.update()
        frames.tick(30)

pygame.init()

game_Intro()

pygame.quit()
