import time
import pygame
from pygame import HWSURFACE

import note

# 초기화
pygame.init()

# 화면 설정
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT], HWSURFACE)

# 모든 스프라이트 그룹
all_sprite = pygame.sprite.Group()

# 화면 택스처
main_bg = pygame.image.load("assets/main_bg.png")  # 80 x 60 px
main_bg = pygame.transform.scale(main_bg, (800, 600))  # 800 x 600 px

# 레인 밝히는 효과
lane_lighting = pygame.image.load("assets/lane_lighting.png").convert_alpha()  # 9 x 60 px
lane_lighting = pygame.transform.scale(lane_lighting, (100, 600))  # 100 x 600 px

# 노래
song = pygame.mixer.Sound("song/Duo Blade Against.wav")
song.set_volume(0.2)
song.play()

beatdiv_const = 4  # 4beat * 4 = 16beat

# FPS
clock = pygame.time.Clock()
clock.tick(60)
start_time = time.time()

# BPM에 따라 증가하는 인덱스
BPM = 202
count = 0

# 폰트
font = pygame.font.SysFont("arial", 30, True, False)
dark_yellow = (255, 172, 5)
green = (100, 158, 0)

perfect_text = pygame.image.load("assets/perfect_text.png").convert_alpha()
good_text = pygame.image.load("assets/good_text.png").convert_alpha()
bad_text = pygame.image.load("assets/bad_text.png").convert_alpha()

# 노트 맞춘 시간
note_hit_time = 0

# SFX
hihat = pygame.mixer.Sound("sfx/hihat.wav")
hihat.set_volume(0.2)

# 노트
note_group = pygame.sprite.Group()

# 노트 판정 범위 (빨강)
per_start = 490
per_last = 520

# 판정 변수
perfect_input = False
good_input = False
bad_input = False

# note_data_file에서 노트 데이터를 불러온 뒤, note_data 리스트에 한 줄 씩 집어넣기 //// 시간(count 변수), key 순서대로 data.  한 박자 당 시간 = '3'
note_data = []
note_data_file = "data/note_data.txt"
with open(note_data_file, 'r') as file:
    for line in file:
        note_data.append(line.strip('\n').split(' '))

# note_data.txt에서 빈 줄 제거 알고리즘
for i in range(len(note_data)):
    note_data[i] = [n for n in note_data[i] if n]

icount = 0
for i in note_data:
    if not i:
        del note_data[icount]
    icount += 1

# note_data 맨 앞의 변수 값 (시간)
note_data_index_list = []
for single_tuple in note_data:
    note_data_index_list.append(single_tuple[0])

# 만들어진 노트 수
note_created = 0

# 키 입력 여부
lane_light_s = "None"
lane_light_d = "None"
lane_light_k = "None"
lane_light_l = "None"

# 루프문
running = True
while running:
    # 종료
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
        if event.type == pygame.KEYDOWN:
            input_time = time.time()
            key_input = pygame.key.get_pressed()

            for each_note in note_group:
                if key_input[pygame.K_s]:
                    lane_light_s = "S"
                    if per_start <= each_note.rect.y <= per_last:
                        each_note.kill()
                        note_hit_time = time.time()
                        perfect_input = True

                    elif per_start - 15 <= each_note.rect.y <= per_last + 15:
                        each_note.kill()
                        note_hit_time = time.time()
                        good_input = True

                    elif per_start - 40 <= each_note.rect.y <= per_last + 40:
                        each_note.kill()
                        note_hit_time = time.time()
                        bad_input = True

                if key_input[pygame.K_d]:
                    lane_light_d = "D"
                    if per_start <= each_note.rect.y <= per_last:
                        each_note.kill()
                        note_hit_time = time.time()
                        perfect_input = True

                    elif per_start - 15 <= each_note.rect.y <= per_last + 15:
                        each_note.kill()
                        note_hit_time = time.time()
                        good_input = True

                    elif per_start - 40 <= each_note.rect.y <= per_last + 40:
                        each_note.kill()
                        note_hit_time = time.time()
                        bad_input = True

                if key_input[pygame.K_k]:
                    lane_light_k = "K"
                    if per_start <= each_note.rect.y <= per_last:
                        each_note.kill()
                        note_hit_time = time.time()
                        perfect_input = True

                    elif per_start - 15 <= each_note.rect.y <= per_last + 15:
                        each_note.kill()
                        note_hit_time = time.time()
                        good_input = True

                    elif per_start - 40 <= each_note.rect.y <= per_last + 40:
                        each_note.kill()
                        note_hit_time = time.time()
                        bad_input = True

                if key_input[pygame.K_l]:
                    lane_light_l = "L"
                    if per_start <= each_note.rect.y <= per_last:
                        each_note.kill()
                        note_hit_time = time.time()
                        perfect_input = True

                    elif per_start - 15 <= each_note.rect.y <= per_last + 15:
                        each_note.kill()
                        note_hit_time = time.time()
                        good_input = True

                    elif per_start - 40 <= each_note.rect.y <= per_last + 40:
                        each_note.kill()
                        note_hit_time = time.time()
                        bad_input = True
                
    # 키 입력 땠을 때
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                lane_light_s = "None"

            if event.key == pygame.K_d:
                lane_light_d = "None"

            if event.key == pygame.K_k:
                lane_light_k = "None"

            if event.key == pygame.K_l:
                lane_light_l = "None"

    # 배경 그리기
    screen.blit(main_bg, (0, 0))

    # 레인 입력 이펙트 감지 및 출력
    if lane_light_s == "S":
        screen.blit(lane_lighting, (70, 0))
    if lane_light_d == "D":
        screen.blit(lane_lighting, (170, 0))
    if lane_light_k == "K":
        screen.blit(lane_lighting, (270, 0))
    if lane_light_l == "L":
        screen.blit(lane_lighting, (370, 0))

    # 박자 계산해서 count 세기
    if time.time() - start_time >= 60 / (BPM * beatdiv_const):
        start_time = time.time()
        count += 1
    
    # 노트 생성
    if note_created < len(note_data_index_list):
        if count == int(note_data_index_list[note_created]):
            if note_data[note_created][1] == "S":
                notes = note.Note("S")
                note_created += 1
                all_sprite.add(notes)
                note_group.add(notes)

            elif note_data[note_created][1] == "D":
                notes = note.Note("D")
                note_created += 1
                all_sprite.add(notes)
                note_group.add(notes)

            elif note_data[note_created][1] == "K":
                notes = note.Note("K")
                note_created += 1
                all_sprite.add(notes)
                note_group.add(notes)

            elif note_data[note_created][1] == "L":
                notes = note.Note("L")
                note_created += 1
                all_sprite.add(notes)
                note_group.add(notes)

    # 판정 이미지 화면에 0.2초간 띄우기
    if perfect_input:
        now = time.time()
        if now - note_hit_time <= 0.2:
            # 다른 판정 변수 다 False 해준 뒤, screen blit.
            good_input = False
            bad_input = False
            screen.blit(perfect_text, (200, 50))
        else:
            perfect_input = False

    elif good_input:
        now = time.time()
        if now - note_hit_time <= 0.2:
            perfect_input = False
            bad_input = False
            screen.blit(good_text, (200, 50))
        else:
            good_input = False

    elif bad_input:
        now = time.time()
        if now - note_hit_time <= 0.2:
            perfect_input = False
            good_input = False
            screen.blit(bad_text, (200, 50))
        else:
            bad_input = False

    note_group.draw(screen)
    note_group.update(HEIGHT)
    pygame.display.update()

pygame.quit()