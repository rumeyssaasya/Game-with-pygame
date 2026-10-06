import pygame
import random

# 1. Başlatma ve Pencere Ayarları
pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Pong - Masa Tenisi")
saat = pygame.time.Clock()

# Yazı Tipleri
baslik_font = pygame.font.SysFont("arial", 48, bold=True)
menu_font = pygame.font.SysFont("arial", 28)
skor_font = pygame.font.SysFont("arial", 40, bold=True)

# 2. Oyun Durum Değişkenleri
durum = "menu"       # "menu" veya "oyun"
yapay_zeka = False   # True ise sağdaki oyuncuyu bilgisayar yönetir

# 3. Raketler ve Hızlar
gamer_1 = pygame.Rect(30, 250, 15, 100)
gamer_2 = pygame.Rect(755, 250, 15, 100)
raket_hizi = 7
ai_hizi = 5.5        # Yapay zekanın takip hızı (biraz pay bırakıyoruz ki yenilebilsin)

# 4. Top ve Hız
ball = pygame.Rect(GENISLIK // 2 - 10, YUKSEKLIK // 2 - 10, 20, 20)
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))

# 5. Skorlar
skor_1 = 0
skor_2 = 0

working = True
while working:
    # ==========================
    # 1. BÖLÜM: MENÜ EKRANI
    # ==========================
    if durum == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                # 1'e basılırsa 2 Kişilik Mod
                if event.key == pygame.K_1:
                    yapay_zeka = False
                    durum = "oyun"
                # 2'ye basılırsa Bilgisayara Karşı Mod
                elif event.key == pygame.K_2:
                    yapay_zeka = True
                    durum = "oyun"

        # Menü Çizimi
        ekran.fill((20, 20, 30))
        
        baslik = baslik_font.render("PONG", True, (255, 215, 0))
        secenek1 = menu_font.render("[1] - 2 Kişilik Oyun (W/S vs Ok Tuşları)", True, (255, 255, 255))
        secenek2 = menu_font.render("[2] - Bilgisayara Karşı (W/S)", True, (0, 200, 255))
        bilgi = menu_font.render("Başlamak için 1 veya 2 tuşuna basın", True, (150, 150, 150))

        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 120))
        ekran.blit(secenek1, (GENISLIK // 2 - secenek1.get_width() // 2, 250))
        ekran.blit(secenek2, (GENISLIK // 2 - secenek2.get_width() // 2, 310))
        ekran.blit(bilgi, (GENISLIK // 2 - bilgi.get_width() // 2, 420))

    # ==========================
    # 2. BÖLÜM: OYUN EKRANI
    # ==========================
    elif durum == "oyun":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            # ESC tuşuna basınca menüye dön
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                durum = "menu"
                skor_1, skor_2 = 0, 0
                ball.center = (GENISLIK // 2, YUKSEKLIK // 2)

        keys = pygame.key.get_pressed()

        # 1. Oyuncu Hareketi (Her zaman W - S)
        if keys[pygame.K_w] and gamer_1.top > 0:
            gamer_1.y -= raket_hizi
        if keys[pygame.K_s] and gamer_1.bottom < YUKSEKLIK:
            gamer_1.y += raket_hizi

        # 2. Oyuncu: İnsan mı yoksa Yapay Zeka mı?
        if not yapay_zeka:
            # 2. Kişi klavyeden oynar (Ok tuşları)
            if keys[pygame.K_UP] and gamer_2.top > 0:
                gamer_2.y -= raket_hizi
            if keys[pygame.K_DOWN] and gamer_2.bottom < YUKSEKLIK:
                gamer_2.y += raket_hizi
        else:
            # Yapay Zeka: Topun y konumuna göre raketi otomatik kaydırır
            if gamer_2.centery < ball.centery and gamer_2.bottom < YUKSEKLIK:
                gamer_2.y += ai_hizi
            elif gamer_2.centery > ball.centery and gamer_2.top > 0:
                gamer_2.y -= ai_hizi

        # --- Top Hareketi ---
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # --- Duvarlardan Sekme ---
        if ball.top <= 0 or ball.bottom >= YUKSEKLIK:
            ball_speed_y *= -1

        # --- Raketlerden Sekme ---
        if ball.colliderect(gamer_1):
            ball_speed_x = abs(ball_speed_x)
            ball.left = gamer_1.right

        if ball.colliderect(gamer_2):
            ball_speed_x = -abs(ball_speed_x)
            ball.right = gamer_2.left

        # --- Gol Kontrolü ---
        if ball.left <= 0:
            skor_2 += 1
            ball.center = (GENISLIK // 2, YUKSEKLIK // 2)
            ball_speed_x = 6 * random.choice((1, -1))
            ball_speed_y = 6 * random.choice((1, -1))

        if ball.right >= GENISLIK:
            skor_1 += 1
            ball.center = (GENISLIK // 2, YUKSEKLIK // 2)
            ball_speed_x = 6 * random.choice((1, -1))
            ball_speed_y = 6 * random.choice((1, -1))

        # --- Çizimler ---
        ekran.fill((30, 30, 30))

        # Orta çizgi
        pygame.draw.aaline(ekran, (80, 80, 80), (GENISLIK // 2, 0), (GENISLIK // 2, YUKSEKLIK))

        # Skorlar
        skor_metni_1 = skor_font.render(str(skor_1), True, (255, 255, 255))
        skor_metni_2 = skor_font.render(str(skor_2), True, (255, 255, 255))
        ekran.blit(skor_metni_1, (GENISLIK // 4, 30))
        ekran.blit(skor_metni_2, (GENISLIK * 3 // 4, 30))

        # Raketler ve Top
        pygame.draw.rect(ekran, (255, 255, 255), gamer_1)
        pygame.draw.rect(ekran, (255, 255, 255), gamer_2)
        pygame.draw.ellipse(ekran, (255, 215, 0), ball)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
