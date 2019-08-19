import pygame
from random import randrange

# Cores
Branco = (255, 255, 255)
Vermelho = (255, 0, 0)
Verde = (0, 255, 0)
Preto = (255, 255, 255)
# Medidas
Largura = 320
Altura = 240
Tamanho = 10
snakeXY = []
maça = pygame.image.load("apple.png")

# Construção
tela = pygame.display.set_mode((Largura, Altura))
pygame.display.set_caption("Cobrinha")
relogio = pygame.time.Clock()

pygame.init()

font = pygame.font.SysFont(None, 16)

def texto(msg, cor):
    texto1 = font.render(msg, True, cor)
    tela.blit(texto1, [Largura // 10, Altura//2])

def snake(snakeXY):
    for xy in snakeXY:
        print(xy[0])
        pygame.draw.rect(tela, Verde, [xy[0], xy[1], Tamanho, Tamanho])


def apple(applex, appley):
    tela.blit(maça, [applex, appley, Tamanho, Tamanho])


def jogo():
    jogoativo = True
    gameover = False
    x = randrange(0, Largura - Tamanho, 10)
    y = randrange(0, Altura - Tamanho, 10)
    apple_x = randrange(0, Largura - Tamanho, 10)
    apple_y = randrange(0, Altura - Tamanho, 10)
    velocidade_x = 0
    velocidade_y = 0
    comprimento = 1

    while jogoativo:
        while gameover:
            tela.fill(Preto)
            texto("Fim de jogo, para continuar tecle C ou S para sair", Vermelho)
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    jogoativo = False
                    gameover = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_c:
                        jogo()
                    if e.key == pygame.K_s:
                        jogoativo = False
                        gameover = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                jogoativo = False
            elif e.type == pygame.KEYDOWN:

                if e.key == pygame.K_LEFT and velocidade_x != Tamanho:
                    velocidade_y = 0
                    velocidade_x = -Tamanho

                if e.key == pygame.K_RIGHT and velocidade_x != -Tamanho:
                    velocidade_y = 0
                    velocidade_x = Tamanho

                if e.key == pygame.K_UP and velocidade_y != Tamanho:
                    velocidade_x = 0
                    velocidade_y = -Tamanho

                if e.key == pygame.K_DOWN and velocidade_y != -Tamanho:
                    velocidade_x = 0
                    velocidade_y = Tamanho



        tela.fill(Branco)

        x += velocidade_x
        y += velocidade_y

        if x > Largura:
            x = 0
        if y > Altura:
            y = 0
        if x < 0:
           x = Largura - Tamanho
        if y < 0:
           y = Altura - Tamanho

        snakeI = []
        snakeI.append(x)
        snakeI.append(y)
        print(x, y)
        snakeXY.append(snakeI)
        if len(snakeXY) > comprimento:
            del snakeXY[0]

        if any(bloco == snakeI for bloco in snakeXY[:-1]):
            gameover = True

        snake(snakeXY)
        if x == apple_x and y == apple_y:
            apple_x = randrange(0, Largura - Tamanho, 10)
            apple_y = randrange(0, Altura - Tamanho, 10)
            comprimento += 1

        apple(apple_x, apple_y)
        pygame.display.update()
        relogio.tick(15)



jogo()
pygame.quit()
