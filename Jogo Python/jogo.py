import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
import random

# Configurar o driver de áudio para 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Definir as dimensões da janela
Largura = 700
Altura = 700

# Criar a janela do Pygame
Tela = pygame.display.set_mode((Largura, Altura), pygame.RESIZABLE)

# Definir o título da janela
pygame.display.set_caption("Get Rect")

# Definir o volume da música
pygame.mixer.music.set_volume(0.1)

# Definir cores
ciano = (86, 165, 169)
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)

# Inicializar fonte
pygame.font.init()
fonte = pygame.font.SysFont('Arial', 45)
fonte_2 = pygame.font.SysFont('Arial', 30)
fonte_3 = pygame.font.SysFont('Helvetica', 20)

# Texto a ser exibido
texto = "Get rect."
texto_2 = "Pressione qualquer tecla para continuar..."
texto_3 = "Feito por Breno Pontes Couto."
texto_renderizado = fonte.render(texto, True, branco)
texto_renderizado2 = fonte_2.render(texto_2, True, branco)
texto_renderizado3 = fonte_3.render(texto_3, True, branco)

# Função para atualizar a posição dos textos com base no tamanho da janela
def atualizar_posicoes(Largura, Altura):
    texto_rect = texto_renderizado.get_rect(center=(Largura // 2, Altura // 2))
    texto_rect2 = texto_renderizado2.get_rect(center=(Largura // 2, Altura // 2 + 50))
    texto_rect3 = texto_renderizado3.get_rect(center=(Largura // 2, Altura - 30))
    return texto_rect, texto_rect2, texto_rect3

# Inicializa as posições dos textos
texto_rect, texto_rect2, texto_rect3 = atualizar_posicoes(Largura, Altura)

# Diretório dos assets
pasta_assets = os.path.join(os.getcwd(), 'assets')

# Função para carregar sons
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(pasta_assets, filename))

# Carregar som de pontuação e som de desligar
coin_sound = load_sound('coin.mp3')
desligar_sound = load_sound('desligar.mp3')

# Carregar imagem de desligar
desligar_img = pygame.image.load(os.path.join(pasta_assets, 'desligando_img.jpg'))

# Tocar som de fundo inicial
pygame.mixer.music.load(os.path.join(pasta_assets, 'background.mp3'))
pygame.mixer.music.play(-1)

# Função para mostrar a tela inicial
def mostrar_tela_inicial():
    Tela.fill(ciano)
    Tela.blit(texto_renderizado, texto_rect)
    Tela.blit(texto_renderizado2, texto_rect2)
    Tela.blit(texto_renderizado3, texto_rect3)
    pygame.display.update()

# Função principal do jogo
def jogo():
    global Tela, Largura, Altura

    # Parar a música de fundo inicial quando o jogo começar
    pygame.mixer.music.stop()

    rodando = True

    # Posições iniciais
    bola_pos = [Largura // 2, Altura // 2]
    bola_vel = [0, 0]
    bola_raio = 20
    quadrado_pos = [random.randint(0, Largura - 20), random.randint(0, Altura - 20)]
    quadrado_tamanho = 30

    # Inicializar a pontuação
    score = 0
    font_score = pygame.font.SysFont('Arial', 30)

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.VIDEORESIZE:
                Largura, Altura = event.size
                Tela = pygame.display.set_mode((Largura, Altura), pygame.RESIZABLE)
                global texto_rect, texto_rect2, texto_rect3
                texto_rect, texto_rect2, texto_rect3 = atualizar_posicoes(Largura, Altura)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bola_vel[0] = -0.4
        elif keys[pygame.K_RIGHT]:
            bola_vel[0] = 0.4
        else:
            bola_vel[0] = 0
        if keys[pygame.K_UP]:
            bola_vel[1] = -0.4
        elif keys[pygame.K_DOWN]:
            bola_vel[1] = 0.4
        else:
            bola_vel[1] = 0

        bola_pos[0] += bola_vel[0]
        bola_pos[1] += bola_vel[1]

        if bola_pos[0] - bola_raio < 0:
            bola_pos[0] = bola_raio
        if bola_pos[0] + bola_raio > Largura:
            bola_pos[0] = Largura - bola_raio
        if bola_pos[1] - bola_raio < 0:
            bola_pos[1] = bola_raio
        if bola_pos[1] + bola_raio > Altura:
            bola_pos[1] = Altura - bola_raio

        if (bola_pos[0] + bola_raio > quadrado_pos[0] and bola_pos[0] - bola_raio < quadrado_pos[0] + quadrado_tamanho and
                bola_pos[1] + bola_raio > quadrado_pos[1] and bola_pos[1] - bola_raio < quadrado_pos[1] + quadrado_tamanho):
            quadrado_pos = [random.randint(0, Largura - quadrado_tamanho), random.randint(0, Altura - quadrado_tamanho)]
            score += 1
            coin_sound.play()

        if score == 15:
            texto_vitoria = "Parabéns! Você ganhou!"
            texto_renderizado_vitoria = fonte.render(texto_vitoria, True, branco)
            texto_vitoria_2 = "O jogo está fechando..."
            texto_renderizado_vitoria_2 = fonte.render(texto_vitoria_2, True, branco)
            Tela.blit(texto_renderizado_vitoria, (Largura // 2 - texto_renderizado_vitoria.get_width() // 2, Altura // 2 - texto_renderizado_vitoria.get_height() // 2))
            Tela.blit(texto_renderizado_vitoria_2, (Largura // 2 - texto_renderizado_vitoria_2.get_width() // 2, Altura // 2 - texto_renderizado_vitoria_2.get_height() // 2 + 50))
            pygame.display.update()
            pygame.time.wait(1000)
            
            # Redimensionar a imagem para ocupar toda a tela
            desligar_img_resized = pygame.transform.scale(desligar_img, (Largura, Altura))
            Tela.blit(desligar_img_resized, (0, 0))
            pygame.display.update()
            desligar_sound.play()
            pygame.time.wait(3500)
            rodando = False

        Tela.fill(ciano)

        pygame.draw.circle(Tela, preto, bola_pos, bola_raio)
        pygame.draw.rect(Tela, vermelho, (*quadrado_pos, quadrado_tamanho, quadrado_tamanho))

        score_renderizado = font_score.render(f'Pontuação: {score}', True, branco)
        Tela.blit(score_renderizado, (10, 10))

        pygame.display.update()

    pygame.quit()

esperando = True
while esperando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esperando = False
            rodando = False
        if event.type == pygame.KEYDOWN:
            esperando = False

    mostrar_tela_inicial()

# Iniciar a música de fundo inicial
pygame.mixer.music.play(-1)

# Iniciar o jogo após a tecla ser pressionada
jogo()
