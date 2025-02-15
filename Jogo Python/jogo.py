import os
import pygame
import random

pygame.init()
pygame.mixer.init()

Largura = 700
Altura = 700

Tela = pygame.display.set_mode((Largura, Altura), pygame.RESIZABLE)
pygame.display.set_caption("Get Rect")

pygame.mixer.music.set_volume(0.1)

ciano = (86, 165, 169)
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)

pygame.font.init()
fonte = pygame.font.SysFont('Arial', 45)
fonte_2 = pygame.font.SysFont('Arial', 30)
fonte_3 = pygame.font.SysFont('Helvetica', 20)
fonte_4 = pygame.font.SysFont('Helvetica', 20)

texto = "Get rect."
texto_2 = "Pressione qualquer tecla para continuar..."
texto_3 = "Feito por Breno Pontes Couto."
texto_4 = "Complete 10 pontos para ganhar e desvie dos obstáculos."
texto_renderizado = fonte.render(texto, True, branco)
texto_renderizado2 = fonte_2.render(texto_2, True, branco)
texto_renderizado3 = fonte_3.render(texto_3, True, branco)
texto_renderizado4 = fonte_4.render(texto_4, True, branco)

def atualizar_posicoes(Largura, Altura):
    texto_rect = texto_renderizado.get_rect(center=(Largura // 2, Altura // 2))
    texto_rect2 = texto_renderizado2.get_rect(center=(Largura // 2, Altura // 2 + 50))
    texto_rect3 = texto_renderizado3.get_rect(center=(Largura // 2, Altura - 30))
    texto_rect4 = texto_renderizado4.get_rect(center=(Largura // 2, Altura - 100))
    return texto_rect, texto_rect2, texto_rect3, texto_rect4

texto_rect, texto_rect2, texto_rect3, texto_rect4 = atualizar_posicoes(Largura, Altura)

pasta_assets = os.path.join(os.getcwd(), 'assets')

def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(pasta_assets, filename))

coin_sound = load_sound('coin.mp3')
desligar_sound = load_sound('desligar.mp3')

desligar_img = pygame.image.load(os.path.join(pasta_assets, 'desligando_img.jpg'))

pygame.mixer.music.load(os.path.join(pasta_assets, 'background.mp3'))
pygame.mixer.music.play(-1)

def mostrar_tela_inicial():
    Tela.fill(ciano)
    Tela.blit(texto_renderizado, texto_rect)
    Tela.blit(texto_renderizado2, texto_rect2)
    Tela.blit(texto_renderizado3, texto_rect3)
    Tela.blit(texto_renderizado4, texto_rect4)
    pygame.display.update()

def atualizar_obstaculos(obstaculos, Largura, Altura):
    for obs in obstaculos:
        obs[0] = random.randint(0, Largura - obs[2])
        obs[1] = random.randint(0, Altura - obs[3])

def mostrar_tela_fim_jogo():
    Tela.fill(ciano)
    texto_fim = fonte.render("Você bateu em um obstáculo!", True, branco)
    texto_opcao = fonte_2.render("Pressione R para reiniciar ou Q para sair", True, branco)
    Tela.blit(texto_fim, (Largura // 2 - texto_fim.get_width() // 2, Altura // 2 - texto_fim.get_height() // 2))
    Tela.blit(texto_opcao, (Largura // 2 - texto_opcao.get_width() // 2, Altura // 2 - texto_opcao.get_height() // 2 + 50))
    pygame.display.update()

def jogo():
    global Tela, Largura, Altura

    pygame.mixer.music.stop()

    rodando = True

    bola_pos = [Largura // 2, Altura // 2]
    bola_vel = [0, 0]
    bola_raio = 20
    quadrado_pos = [random.randint(0, Largura - 20), random.randint(0, Altura - 20)]
    quadrado_tamanho = 30

    score = 0
    font_score = pygame.font.SysFont('Arial', 30)

    obstaculos = []
    for _ in range(3):
        obstaculos.append([random.randint(0, Largura - 30), random.randint(0, Altura - 30), 30, 30])

    fim_jogo = False

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.VIDEORESIZE:
                Largura, Altura = event.size
                Tela = pygame.display.set_mode((Largura, Altura), pygame.RESIZABLE)
                global texto_rect, texto_rect2, texto_rect3, texto_rect4
                texto_rect, texto_rect2, texto_rect3, texto_rect4 = atualizar_posicoes(Largura, Altura)
            elif event.type == pygame.KEYDOWN and fim_jogo:
                if event.key == pygame.K_r:
                    jogo()  # Reinicia o jogo
                elif event.key == pygame.K_q:
                    rodando = False

        if not fim_jogo:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                bola_vel[0] = -0.6
            elif keys[pygame.K_RIGHT]:
                bola_vel[0] = 0.6
            else:
                bola_vel[0] = 0
            if keys[pygame.K_UP]:
                bola_vel[1] = -0.6
            elif keys[pygame.K_DOWN]:
                bola_vel[1] = 0.6
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
                atualizar_obstaculos(obstaculos, Largura, Altura)
                score += 1
                coin_sound.play()

            for obs in obstaculos:
                if (bola_pos[0] + bola_raio > obs[0] and bola_pos[0] - bola_raio < obs[0] + obs[2] and
                        bola_pos[1] + bola_raio > obs[1] and bola_pos[1] - bola_raio < obs[1] + obs[3]):
                        fim_jogo = True

        Tela.fill(ciano)

        pygame.draw.circle(Tela, preto, bola_pos, bola_raio)
        pygame.draw.rect(Tela, vermelho, (*quadrado_pos, quadrado_tamanho, quadrado_tamanho))

        for obs in obstaculos:
            pygame.draw.rect(Tela, branco, obs)

        score_renderizado = font_score.render(f'Pontuação: {score}', True, branco)
        Tela.blit(score_renderizado, (10, 10))

        if fim_jogo:
            mostrar_tela_fim_jogo()

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

pygame.mixer.music.play(-1)

jogo()
