import pygame
import random

pygame.init()
ekran = pygame.display.set_mode((600, 400))
saat = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
bitti_font = pygame.font.SysFont("arial", 32, bold=True)

BLOK_BOYUTU = 20

# Başlangıçta SADECE TEK BİR KARE var
yilan = [[100, 100]]

# Başlangıç hızı: Sağa doğru aksın
hiz_x = BLOK_BOYUTU
hiz_y = 0

# Yem konumu (ekrana tam oturacak şekilde)
yem_x = random.randint(0, (600 - BLOK_BOYUTU) // BLOK_BOYUTU) * BLOK_BOYUTU
yem_y = random.randint(0, (400 - BLOK_BOYUTU) // BLOK_BOYUTU) * BLOK_BOYUTU
yem = pygame.Rect(yem_x, yem_y, BLOK_BOYUTU, BLOK_BOYUTU)

oyun_bitti = False
calisiyor = True

while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False
        
        # Oyun bittiğinde 'R' tuşuna basılırsa sıfırla
        if olay.type == pygame.KEYDOWN and oyun_bitti:
            if olay.key == pygame.K_r:
                yilan = [[100, 100]]
                hiz_x = BLOK_BOYUTU
                hiz_y = 0
                oyun_bitti = False

    # Tuş kontrolleri (Sadece oyun devam ederken çalışsın)
    if not oyun_bitti:
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_RIGHT] and hiz_x == 0:
            hiz_x = BLOK_BOYUTU
            hiz_y = 0
        elif tuslar[pygame.K_LEFT] and hiz_x == 0:
            hiz_x = -BLOK_BOYUTU
            hiz_y = 0
        elif tuslar[pygame.K_UP] and hiz_y == 0:
            hiz_x = 0
            hiz_y = -BLOK_BOYUTU
        elif tuslar[pygame.K_DOWN] and hiz_y == 0:
            hiz_x = 0
            hiz_y = BLOK_BOYUTU

        # 1. Yeni kafa ekle
        yeni_kafa = [yilan[0][0] + hiz_x, yilan[0][1] + hiz_y]

        # Ekrandan taşınca karşıdan çıkma
        if yeni_kafa[0] >= 600: yeni_kafa[0] = 0
        elif yeni_kafa[0] < 0:  yeni_kafa[0] = 600 - BLOK_BOYUTU
        if yeni_kafa[1] >= 400: yeni_kafa[1] = 0
        elif yeni_kafa[1] < 0:  yeni_kafa[1] = 400 - BLOK_BOYUTU

        # Kendine çarpma kontrolü
        if yeni_kafa in yilan:
            oyun_bitti = True
        else:
            yilan.insert(0, yeni_kafa)

            # 2. Yem yendi mi?
            kafa_rect = pygame.Rect(yilan[0][0], yilan[0][1], BLOK_BOYUTU, BLOK_BOYUTU)
            if kafa_rect.colliderect(yem):
                yem.x = random.randint(0, (600 - BLOK_BOYUTU) // BLOK_BOYUTU) * BLOK_BOYUTU
                yem.y = random.randint(0, (400 - BLOK_BOYUTU) // BLOK_BOYUTU) * BLOK_BOYUTU
            else:
                yilan.pop()

    # --- 3. ÇİZİM ADIMI (Sıralama: Zemin -> Nesneler -> Yazılar) ---
    ekran.fill((30, 30, 30))  # Önce ekranı temizle

    # Yılan parçalarını çiz
    for parca in yilan:
        pygame.draw.rect(ekran, (0, 200, 100), (parca[0], parca[1], BLOK_BOYUTU, BLOK_BOYUTU))

    # Yemi çiz
    pygame.draw.rect(ekran, (238, 173, 14), yem)
    pygame.draw.rect(ekran, (139, 101, 8), yem, 2)

    # Skor yazısı
    skor_resmi = font.render(f"Skor: {len(yilan)}", True, (255, 255, 255))
    ekran.blit(skor_resmi, (10, 10))

    # Oyun bittiyse mesajı zemin temizlendikten SONRA basıyoruz
    if oyun_bitti:
        bitti_resmi = bitti_font.render(f"GAME OVER - Skor: {len(yilan)}", True, (255, 80, 80))
        tekrar_resmi = font.render("Yeniden baslamak icin [R] tusuna basin", True, (200, 200, 200))
        ekran.blit(bitti_resmi, (140, 160))
        ekran.blit(tekrar_resmi, (130, 210))

    pygame.display.set_caption(f"Yılan Oyunu - Uzunluk: {len(yilan)}")
    pygame.display.flip()
    saat.tick(10)

pygame.quit()