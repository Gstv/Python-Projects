# Importanto e iniciando o Pygame
import pygame

pygame.init()
# Variavel que define as cores, colocar um nome e ela no RGB
preto = (   0,   0,   0)
branco = ( 255, 255, 255)
verde = (   0, 255,   0)
vermelho = ( 255,   0,   0)
# Tamanho da tela, pode ser uma variavel como x y
size = (1280, 720)
#x = 640
#y = 310
# cria uma classe que pode ser usada para tudo, tipo uma variavel, com ela, podemos dar as informacoes, e puxar isso depois.
class personagem (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(vermelho)
        self.rect = self.image.get_rect()
        self.rect.x = 640
        self.rect.y = 320
# Usa a variavel "size"  no caso para abrir a tela, e define o nome da tela.
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ae luanidos")
# um loop para manter a janela aberta, e permitir com que o usuario feche a mesma, pelo visto vai ser usado para tudo, para dar update e td mais
fechar = False
tempo = pygame.time.Clock()
# Gameloop, tudo esta ligado a este while, ele que fica carregando e recarregando tudo na tela.
# pode ter uma funcao que chama este gameloop(o while). O igor que me falou essa ultima parte, pedir ajuda para o luan(para ele explicar e/ou mostrar, ou falar novamente com o Igor
while not fechar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fechar = True
# torna a tela verde, e o mais importante, limpa a tela, de forma que atualiza as infos na mesma. Dessa forma, podemos colocar outras informacoes na tela Nao gerar NADA antes disso( Fora variaveis )
        screen.fill(verde)
        #Barra do topo
        pygame.draw.rect(screen, preto, [40, 50, 1200, 10])
        #Barra de baixo
        pygame.draw.rect(screen, preto, [40, 670, 1200, 10])
        #Esquerda
        pygame.draw.rect(screen, preto, [40, 50, 10, 620])

        pygame.draw.rect(screen, preto, [1240, 50, 10, 620])


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Saindo")
        pygame.display.flip()
# Limita os frames/fps para o numero escolhido, no caso 60, mas esta dando algum bug, verificar e corrigir

# Um laco para printar infos (apenas testando para aprender)(Ainda n esta funcionando)
for event in pygame.event.get():
        if event.type == pygame.QUIT:
           print("Saindo")
# Gera 3 retangulos, MAS precisa estar relacionado com o gameloop para receber o update

pygame.display.flip()

pygame.quit()




