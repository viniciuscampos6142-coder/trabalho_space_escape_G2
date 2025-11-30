##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import pygame
import random
import os
import traceback
import math

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES INICIAIS
# ----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

WIDTH, HEIGHT = 800, 600
FPS = 60
BULLET_SPEED = 10
PLAYER_SPEED = 5

# Cores
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Configurações de Gameplay
INVINCIBLE_DURATION = 2000
TELEPORT_INVULNERABILITY_DURATION = 4000
SHIELD_INVULNERABILITY_DURATION = 5000
POWERUP_DURATION = 5000
WIN_SCORE = 1500  # Pontuação para vencer (APENAS NO MODO 2)

try:
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Scape - Always Game Over")
    clock = pygame.time.Clock()

    # ----------------------------------------------------------
    # 🧩 DEFINIÇÃO DOS ASSETS
    # ----------------------------------------------------------
    ASSETS_FILES = {
        "player": "nave-d-gerra.png",
        "laser": "missil.png",
        "sound_shoot": "som-tiro.mp3",
        "sound_phase_change": "next-level.mp3",
        "sound_gameover": "game-over.mp3",

        "meteor_weapon": "meteoro-especial-F3(2.0).png",
        "meteor_teleport": "meteoro-especial-F1(2.0).png",
        "meteor_shield": "meteoro-especial-F2(2.0).png",
        "background": "foto-selva-2.png",
        "meteor": "rocha.png",
        "sound_point": "ponto-selva.mp3",
        "sound_hit": "selva-dano.mp3",
        "music": "retro-retro.mp3",
        "background1": "ceu.jpg",
        "meteor1": "cometa-liquido.png",
        "sound_point1": "ponto.mp3",
        "sound_hit1": "destruicao.mp3",
        "music1": "music-rock.mp3",
        "background2": "fase-final3.0.png",
        "meteor2": "meteoro-final.png",
        "sound_point2": "point-final.mp3",
        "sound_hit2": "som-dano-final.mp3",
        "music2": "som-final.mp3",
    }


    def get_asset_path(filename):
        path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(path): return path
        path = os.path.join(BASE_DIR, filename)
        if os.path.exists(path): return path
        return None


    def load_image(filename, fallback_color, size=None):
        path = get_asset_path(filename)
        if path:
            try:
                img = pygame.image.load(path).convert_alpha()
                if size: img = pygame.transform.scale(img, size)
                return img
            except Exception:
                pass
        surf = pygame.Surface(size or (40, 40))
        surf.fill(fallback_color)
        return surf


    def load_sound(filename):
        path = get_asset_path(filename)
        if path:
            try:
                return pygame.mixer.Sound(path)
            except:
                pass
        return None


    def play_music(filename):
        path = get_asset_path(filename)
        if path:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)


    # --- CARREGANDO ASSETS ---
    p1_img = load_image(ASSETS_FILES["player"], BLUE, (80, 60))
    p2_img = p1_img.copy()
    p2_img.fill((255, 100, 100, 255), special_flags=pygame.BLEND_MULT)

    laser_img = load_image(ASSETS_FILES["laser"], GREEN, (10, 30))

    meteor_weapon_img = load_image(ASSETS_FILES["meteor_weapon"], MAGENTA, (35, 35))
    meteor_teleport_img = load_image(ASSETS_FILES["meteor_teleport"], CYAN, (35, 35))
    meteor_shield_img = load_image(ASSETS_FILES["meteor_shield"], GREEN, (35, 35))

    sound_shoot = load_sound(ASSETS_FILES["sound_shoot"])
    sound_powerup = load_sound("powerup.mp3")

    sound_phase_change = load_sound(ASSETS_FILES["sound_phase_change"])
    sound_gameover = load_sound(ASSETS_FILES["sound_gameover"])

    bg_phase1 = load_image(ASSETS_FILES["background"], BLACK, (WIDTH, HEIGHT))
    meteor_phase1 = load_image(ASSETS_FILES["meteor"], RED, (40, 40))
    snd_point_phase1 = load_sound(ASSETS_FILES["sound_point"])
    snd_hit_phase1 = load_sound(ASSETS_FILES["sound_hit"])

    bg_phase2 = load_image(ASSETS_FILES["background1"], (20, 20, 50), (WIDTH, HEIGHT))
    meteor_phase2 = load_image(ASSETS_FILES["meteor1"], BLUE, (40, 40))
    snd_point_phase2 = load_sound(ASSETS_FILES["sound_point2"])
    snd_hit_phase2 = load_sound(ASSETS_FILES["sound_hit1"])

    bg_phase3 = load_image(ASSETS_FILES["background2"], (50, 0, 0), (WIDTH, HEIGHT))
    meteor_phase3 = load_image(ASSETS_FILES["meteor2"], YELLOW, (50, 50))
    snd_point_phase3 = load_sound(ASSETS_FILES["sound_point2"])
    snd_hit_phase3 = load_sound(ASSETS_FILES["sound_hit2"])

    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 80)
    small_font = pygame.font.Font(None, 24)

    # ----------------------------------------------------------
    # 🧠 VARIÁVEIS GLOBAIS
    # ----------------------------------------------------------
    game_state = "MENU"
    game_mode = 1
    modo_mouse = False

    p1_rect = p1_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    p2_rect = p2_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))

    meteor_list = []
    bullet_list = []

    score = 0
    p1_score = 0
    p2_score = 0

    p1_lives = 3
    p2_lives = 3

    fase = 1
    meteor_speed = 5

    # Estados de Hit e Power-up
    p1_hit = False
    p1_hit_timer = 0
    p1_weapon_active = 0

    p2_hit = False
    p2_hit_timer = 0
    p2_weapon_active = 0

    current_background = bg_phase1
    current_meteor_img = meteor_phase1
    current_sound_point = snd_point_phase1
    current_sound_hit = snd_hit_phase1
    current_music_file = ASSETS_FILES["music"]


    def add_meteor():
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-500, -40)
        rect_size = 40
        rot_speed = random.choice([-3, -2, 2, 3])
        meteor_type = 0

        roll = random.randint(1, 100)

        if roll <= 5:
            meteor_type = 3  # Arma
            rect_size = 35
            rot_speed = 5
        elif roll <= 10:
            meteor_type = 1  # Teleporte
            rect_size = 35
            rot_speed = 4
        elif roll <= 15:
            meteor_type = 2  # Escudo
            rect_size = 35
            rot_speed = 3
        elif random.randint(1, 5) == 1:
            rect_size = 30
            rot_speed = random.choice([-1, 1])

        rect = pygame.Rect(x, y, rect_size, rect_size)
        meteor_list.append({
            'rect': rect,
            'angle': 0,
            'rot_speed': rot_speed,
            'trail': [],
            'type': meteor_type
        })


    def shoot_laser(origin_rect):
        global p1_weapon_active, p2_weapon_active

        shooter_id = 1 if origin_rect == p1_rect else 2
        now = pygame.time.get_ticks()
        has_weapon = False
        if origin_rect == p1_rect and now < p1_weapon_active: has_weapon = True
        if origin_rect == p2_rect and now < p2_weapon_active: has_weapon = True

        if has_weapon:
            angles = [-15, 0, 15]
            for angle in angles:
                start_x = origin_rect.centerx + math.sin(math.radians(angle)) * 20
                start_y = origin_rect.top + math.cos(math.radians(angle)) * 20
                bullet_rect = laser_img.get_rect(center=(start_x, start_y))
                vel_x = math.sin(math.radians(-angle)) * 5
                bullet_list.append(
                    {'rect': bullet_rect, 'trail': [], 'vel_x': vel_x, 'special': True, 'owner': shooter_id})
        else:
            bullet_rect = laser_img.get_rect(center=(origin_rect.centerx, origin_rect.top))
            bullet_list.append({'rect': bullet_rect, 'trail': [], 'vel_x': 0, 'special': False, 'owner': shooter_id})

        if sound_shoot:
            sound_shoot.set_volume(0.4)
            sound_shoot.play()


    def update_phase_assets(new_fase):
        global fase, meteor_speed, current_background, current_meteor_img
        global current_sound_point, current_sound_hit, current_music_file

        if new_fase > 1 and new_fase != fase:
            if sound_phase_change:
                sound_phase_change.play()

        fase = new_fase
        if fase == 1:
            meteor_speed = 5
            current_background = bg_phase1
            current_meteor_img = meteor_phase1
            current_sound_point = snd_point_phase1
            current_sound_hit = snd_hit_phase1
            current_music_file = ASSETS_FILES["music"]
        elif fase == 2:
            meteor_speed = 7
            current_background = bg_phase2
            current_meteor_img = meteor_phase2
            current_sound_point = snd_point_phase2
            current_sound_hit = snd_hit_phase2
            current_music_file = ASSETS_FILES["music1"]
            if len(meteor_list) < 10:
                for _ in range(5): add_meteor()
        elif fase == 3:
            meteor_speed = 8
            current_background = bg_phase3
            current_meteor_img = meteor_phase3
            current_sound_point = snd_point_phase3
            current_sound_hit = snd_hit_phase3
            current_music_file = ASSETS_FILES["music2"]
            if len(meteor_list) < 15:
                for _ in range(5): add_meteor()
        play_music(current_music_file)


    def start_new_game(mode):
        global score, p1_score, p2_score, p1_lives, p2_lives, fase, game_mode
        global p1_hit, p1_hit_timer, p2_hit, p2_hit_timer
        global p1_weapon_active, p2_weapon_active

        game_mode = mode
        score = 0
        p1_score = 0
        p2_score = 0

        p1_hit = False
        p1_hit_timer = 0
        p1_weapon_active = 0
        p2_hit = False
        p2_hit_timer = 0
        p2_weapon_active = 0

        meteor_list.clear()
        bullet_list.clear()

        # [ALTERADO] Configuração de vidas separadas
        if game_mode == 1:
            p1_lives = 3
            p2_lives = 0  # Inativo
            p1_rect.center = (WIDTH // 2, HEIGHT - 60)
            for _ in range(6): add_meteor()
        else:
            p1_lives = 3
            p2_lives = 3
            p1_rect.center = (WIDTH * 0.75, HEIGHT - 60)
            p2_rect.center = (WIDTH * 0.25, HEIGHT - 60)
            for _ in range(8): add_meteor()

        update_phase_assets(1)


    def desenhar_propulsores(target_rect):
        motor_esquerdo = (target_rect.centerx - 10, target_rect.bottom - 5)
        motor_direito = (target_rect.centerx + 10, target_rect.bottom - 5)
        motores = [motor_esquerdo, motor_direito]
        for pos_motor in motores:
            cores = [RED, ORANGE, YELLOW]
            raios = [8, 6, 3]
            for i in range(3):
                offset_x = random.randint(-2, 2)
                offset_y = random.randint(0, 5) + (i * 3)
                raio_atual = raios[i] + random.randint(-1, 1)
                if raio_atual <= 0: raio_atual = 1
                pos_chama = (pos_motor[0] + offset_x, pos_motor[1] + offset_y)
                pygame.draw.circle(screen, cores[i], pos_chama, raio_atual)


    def handle_player_hit(is_p1):
        global p1_lives, p2_lives, p1_hit, p1_hit_timer, p2_hit, p2_hit_timer
        now = pygame.time.get_ticks()

        if is_p1:
            p1_lives -= 1
            p1_hit = True
            p1_hit_timer = now + INVINCIBLE_DURATION
        else:
            p2_lives -= 1
            p2_hit = True
            p2_hit_timer = now + INVINCIBLE_DURATION

        if current_sound_hit: current_sound_hit.play()


    def teleport_player(player_rect):
        new_x = random.randint(50, WIDTH - 50)
        new_y = random.randint(50, HEIGHT - 50)
        player_rect.center = (new_x, new_y)
        if game_mode == 1 and modo_mouse:
            pygame.mouse.set_pos(new_x, new_y)


    # ----------------------------------------------------------
    # 🕹️ LOOP PRINCIPAL
    # ----------------------------------------------------------
    running = True
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False

            if game_state == "MENU":
                pygame.mouse.set_visible(True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: modo_mouse = False; start_new_game(1); game_state = "JOGANDO"
                    if event.key == pygame.K_m: modo_mouse = True; pygame.mouse.set_visible(False); start_new_game(
                        1); game_state = "JOGANDO"
                    if event.key == pygame.K_2: modo_mouse = False; start_new_game(2); game_state = "JOGANDO"

            elif game_state == "JOGANDO":
                if event.type == pygame.KEYDOWN:
                    if game_mode == 1:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL: shoot_laser(p1_rect)
                    elif game_mode == 2:
                        if event.key == pygame.K_RCTRL: shoot_laser(p1_rect)
                        # [ALTERADO] Removido o 'or event.key == pygame.K_z'
                        if event.key == pygame.K_LCTRL: shoot_laser(p2_rect)

            elif game_state == "GAMEOVER" or game_state == "VICTORY":
                if event.type == pygame.KEYDOWN: game_state = "MENU"

        if game_state == "JOGANDO":
            screen.blit(current_background, (0, 0))
            keys = pygame.key.get_pressed()

            # Movimento P1
            if game_mode == 1 and modo_mouse:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                p1_rect.center = (mouse_x, mouse_y)
            else:
                if keys[pygame.K_LEFT]: p1_rect.x -= PLAYER_SPEED
                if keys[pygame.K_RIGHT]: p1_rect.x += PLAYER_SPEED
                if keys[pygame.K_UP]: p1_rect.y -= PLAYER_SPEED
                if keys[pygame.K_DOWN]: p1_rect.y += PLAYER_SPEED
            p1_rect.clamp_ip(screen.get_rect())

            # Movimento P2
            if game_mode == 2:
                if keys[pygame.K_a]: p2_rect.x -= PLAYER_SPEED
                if keys[pygame.K_d]: p2_rect.x += PLAYER_SPEED
                if keys[pygame.K_w]: p2_rect.y -= PLAYER_SPEED
                if keys[pygame.K_s]: p2_rect.y += PLAYER_SPEED
                p2_rect.clamp_ip(screen.get_rect())

            # Timers
            if p1_hit and now > p1_hit_timer: p1_hit = False
            if p2_hit and now > p2_hit_timer: p2_hit = False
            if p1_weapon_active > 0 and now > p1_weapon_active: p1_weapon_active = 0
            if p2_weapon_active > 0 and now > p2_weapon_active: p2_weapon_active = 0

            # Desenho Players
            if not p1_hit or (now // 100) % 2:
                screen.blit(p1_img, p1_rect)
                desenhar_propulsores(p1_rect)

            if game_mode == 2:
                if not p2_hit or (now // 100) % 2:
                    screen.blit(p2_img, p2_rect)
                    desenhar_propulsores(p2_rect)

            # TIROS
            for bullet in bullet_list[:]:
                bullet['trail'].append(bullet['rect'].center)
                if len(bullet['trail']) > 5: bullet['trail'].pop(0)
                bullet['rect'].y -= BULLET_SPEED
                bullet['rect'].x += bullet.get('vel_x', 0)

                if bullet['rect'].bottom < 0 or bullet['rect'].left < -100 or bullet['rect'].right > WIDTH + 100:
                    bullet_list.remove(bullet)
                    continue

                trail_color = MAGENTA if bullet.get('special') else (100, 255, 100)
                for i, pos in enumerate(bullet['trail']):
                    pygame.draw.circle(screen, trail_color, pos, i + 1)
                screen.blit(laser_img, bullet['rect'])

                for meteor in meteor_list[:]:
                    if bullet['rect'].colliderect(meteor['rect']):
                        owner = bullet.get('owner', 0)
                        points = 10
                        if owner == 1:
                            p1_score += points
                        elif owner == 2:
                            p2_score += points
                        score += points

                        if bullet in bullet_list: bullet_list.remove(bullet)
                        meteor_list.remove(meteor)
                        add_meteor()
                        if current_sound_point: current_sound_point.play()
                        break

            # METEOROS
            for meteor in meteor_list[:]:
                meteor['trail'].append(meteor['rect'].center)
                if len(meteor['trail']) > 12: meteor['trail'].pop(0)
                meteor['rect'].y += meteor_speed
                meteor['angle'] = (meteor['angle'] + meteor['rot_speed']) % 360

                # LÓGICA DE ESQUIVA
                if meteor['rect'].y > HEIGHT:
                    meteor_list.remove(meteor)
                    add_meteor()

                    if meteor['type'] == 0:
                        points_evade = 5
                        score += points_evade
                        p1_score += points_evade
                        if game_mode == 2:
                            p2_score += points_evade
                        if current_sound_point: current_sound_point.play()

                    continue

                # COLISÃO PLAYER 1
                if meteor['rect'].colliderect(p1_rect):
                    meteor_list.remove(meteor)
                    add_meteor()

                    if meteor['type'] == 3:  # Arma
                        p1_score += 50
                        score += 50
                        p1_weapon_active = now + POWERUP_DURATION
                        if sound_powerup: sound_powerup.play()

                    elif meteor['type'] == 1:  # Teleporte
                        p1_score += 50
                        score += 50
                        teleport_player(p1_rect)
                        p1_hit = True
                        p1_hit_timer = now + TELEPORT_INVULNERABILITY_DURATION
                        if sound_powerup: sound_powerup.play()

                    elif meteor['type'] == 2:  # Escudo
                        p1_score += 50
                        score += 50
                        p1_hit = True
                        p1_hit_timer = now + SHIELD_INVULNERABILITY_DURATION
                        if sound_powerup: sound_powerup.play()

                    elif not p1_hit:  # Meteoro normal (Type 0)
                        handle_player_hit(True)

                    continue

                # COLISÃO PLAYER 2
                if game_mode == 2 and meteor['rect'].colliderect(p2_rect):
                    meteor_list.remove(meteor)
                    add_meteor()

                    if meteor['type'] == 3:  # Arma
                        p2_score += 50
                        score += 50
                        p2_weapon_active = now + POWERUP_DURATION
                        if sound_powerup: sound_powerup.play()

                    elif meteor['type'] == 1:  # Teleporte
                        p2_score += 50
                        score += 50
                        teleport_player(p2_rect)
                        p2_hit = True
                        p2_hit_timer = now + TELEPORT_INVULNERABILITY_DURATION
                        if sound_powerup: sound_powerup.play()

                    elif meteor['type'] == 2:  # Escudo
                        p2_score += 50
                        score += 50
                        p2_hit = True
                        p2_hit_timer = now + SHIELD_INVULNERABILITY_DURATION
                        if sound_powerup: sound_powerup.play()

                    elif not p2_hit:  # Meteoro normal (Type 0)
                        handle_player_hit(False)

                # ==========================================================
                # 🛑 LÓGICA DE FIM DE JOGO E ELIMINAÇÃO
                # ==========================================================

                # MODO 1 JOGADOR
                if game_mode == 1:
                    if p1_lives <= 0:
                        if game_state != "GAMEOVER":
                            pygame.mixer.music.stop()
                            pygame.mixer.stop()
                            if sound_gameover: sound_gameover.play()
                            game_state = "GAMEOVER"

                # MODO 2 JOGADORES (ELIMINAÇÃO)
                elif game_mode == 2:

                    # Se P1 morre -> P2 Vence
                    if p1_lives <= 0:
                        if game_state != "VICTORY":
                            pygame.mixer.music.stop()
                            pygame.mixer.stop()  # Para sons de explosão
                            # Consideramos Game Over para quem perdeu, mas é tela de vitória
                            if sound_gameover: sound_gameover.play()
                            game_state = "VICTORY"

                    # Se P2 morre -> P1 Vence
                    elif p2_lives <= 0:
                        if game_state != "VICTORY":
                            pygame.mixer.music.stop()
                            pygame.mixer.stop()
                            if sound_gameover: sound_gameover.play()
                            game_state = "VICTORY"

                    # Se ninguém morreu, checa pontos
                    elif score >= WIN_SCORE:
                        if game_state != "VICTORY":
                            pygame.mixer.music.stop()
                            if p1_score == p2_score:
                                if sound_gameover: sound_gameover.play()
                            game_state = "VICTORY"

                # Desenho Meteoros
                img_to_draw = current_meteor_img
                trail_color_outer = ORANGE
                trail_color_core = YELLOW
                if meteor['type'] == 3:
                    img_to_draw = meteor_weapon_img;
                    trail_color_outer = MAGENTA;
                    trail_color_core = RED
                elif meteor['type'] == 1:
                    img_to_draw = meteor_teleport_img;
                    trail_color_outer = CYAN;
                    trail_color_core = WHITE
                elif meteor['type'] == 2:
                    img_to_draw = meteor_shield_img;
                    trail_color_outer = GREEN;
                    trail_color_core = WHITE

                for i, pos in enumerate(meteor['trail']):
                    size = int(i * 1.8)
                    if size > 0:
                        offset_x = random.randint(-3, 3);
                        offset_y = random.randint(-3, 3)
                        pygame.draw.circle(screen, trail_color_outer, (pos[0] + offset_x, pos[1] + offset_y), size)
                        if i > 6: pygame.draw.circle(screen, trail_color_core, pos, size // 2)

                rot_img = pygame.transform.rotate(img_to_draw, meteor['angle'])
                rot_rect = rot_img.get_rect(center=meteor['rect'].center)
                screen.blit(rot_img, rot_rect)

            # Fase
            if fase == 1 and score >= 350:
                update_phase_assets(2)
            elif fase == 2 and score >= 700:
                update_phase_assets(3)

            # HUD
            hud_text = ""
            if game_mode == 1:
                hud_text = f"Pontos: {p1_score}  Vidas: {p1_lives}  Fase: {fase}"
            else:
                hud_text = f"P1: {p1_score} (Vidas: {p1_lives})  |  P2: {p2_score} (Vidas: {p2_lives})  |  Fase: {fase}"

            score_text = font.render(hud_text, True, WHITE)
            screen.blit(score_text, (10, 10))

            if p1_weapon_active > now: screen.blit(
                small_font.render(f"P1 ARMA: {int((p1_weapon_active - now) / 1000)}s", True, MAGENTA), (10, 40))
            if game_mode == 2 and p2_weapon_active > now: screen.blit(
                small_font.render(f"P2 ARMA: {int((p2_weapon_active - now) / 1000)}s", True, MAGENTA),
                (WIDTH - 150, 40))

        elif game_state == "MENU":
            screen.blit(bg_phase1, (0, 0))
            t_surf = title_font.render("SPACE ESCAPE", True, YELLOW)
            t_rect = t_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            screen.blit(t_surf, t_rect)
            if (now // 500) % 2 == 0:
                screen.blit(font.render("1 - 1 JOGADOR (Teclado)", True, WHITE),
                            (WIDTH // 2 - 150, HEIGHT // 2 + 50))
                screen.blit(font.render("M - 1 JOGADOR (Mouse)", True, GREEN), (WIDTH // 2 - 150, HEIGHT // 2 + 90))
                screen.blit(font.render("2 - 2 JOGADORES", True, RED), (WIDTH // 2 - 100, HEIGHT // 2 + 130))

        elif game_state == "GAMEOVER" or game_state == "VICTORY":
            screen.fill((20, 20, 20))

            # ------------------------------------------------------------------
            # [ALTERADO] SEMPRE "GAME OVER" EM VERMELHO
            # ------------------------------------------------------------------
            main_text = "GAME OVER"
            main_color = RED

            screen.blit(title_font.render(main_text, True, main_color), (WIDTH // 2 - 150, HEIGHT // 2 - 150))

            if game_mode == 1:
                screen.blit(font.render(f"Sua Pontuação: {score}", True, WHITE), (WIDTH // 2 - 110, HEIGHT // 2 - 50))
            else:
                screen.blit(font.render(f"Player 1: {p1_score}", True, BLUE), (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                screen.blit(font.render(f"Player 2: {p2_score}", True, RED), (WIDTH // 2 + 50, HEIGHT // 2 - 50))

                # Lógica de texto de vencedor (Pontos ou Eliminação)
                winner_text = ""
                winner_color = WHITE

                # Checa eliminação primeiro
                if p1_lives <= 0:
                    winner_text = "VENCEDOR: PLAYER 2 (Eliminação)"
                    winner_color = RED
                elif p2_lives <= 0:
                    winner_text = "VENCEDOR: PLAYER 1 (Eliminação)"
                    winner_color = BLUE
                else:
                    # Se ninguém morreu, vai por pontos
                    if p1_score > p2_score:
                        winner_text = "VENCEDOR: PLAYER 1 (Pontos)"
                        winner_color = BLUE
                    elif p2_score > p1_score:
                        winner_text = "VENCEDOR: PLAYER 2 (Pontos)"
                        winner_color = RED
                    else:
                        winner_text = "EMPATOU!"

                screen.blit(font.render(winner_text, True, winner_color), (WIDTH // 2 - 200, HEIGHT // 2 + 50))

            screen.blit(font.render("Pressione qualquer tecla para Menu", True, YELLOW),
                        (WIDTH // 2 - 190, HEIGHT // 2 + 120))

        pygame.display.flip()

    pygame.quit()
except Exception as e:
    print("\n❌ ERRO FATAL:")
    print(e)
    traceback.print_exc()
    input("\nEnter para sair...")
