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

# 게임 속 계산 변수들
score_val = 0
perfect_num = 0
good_num = 0
bad_num = 0
total_hit_num = 0

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
font = pygame.font.Font("assets/font/Facon.ttf", 30)
dark_yellow = (255, 172, 5)
green = (100, 158, 0)

score_text = font.render("Score: ", True, (0, 0, 0))

perfect_num_text = font.render("Perfect: ", True, (0, 0, 0))
good_num_text = font.render("Good: ", True, (0, 0, 0))
bad_num_text = font.render("Bad: ", True, (0, 0, 0))
total_hit_num_text = font.render("Total: ", True, (0, 0, 0))

# 점수 계산 텍스트
score_calc_text = font.render(str(score_val), True, (0, 0, 0))
def score_add(val):
    global score_calc_text
    global score_val
    score_val += val
    score_calc_text = font.render(str(score_val), True, (0, 0, 0))

# Perfect 개수 계산 텍스트
perfect_num_calc_text = font.render(str(perfect_num), True, (0, 0, 0))
def perfect_add():
    global perfect_num_calc_text
    global perfect_num
    perfect_num += 1
    perfect_num_calc_text = font.render(str(perfect_num), True, (0, 0, 0))

# Good 개수 계산 텍스트
good_num_calc_text = font.render(str(good_num), True, (0, 0, 0))
def good_add():
    global good_num_calc_text
    global good_num
    good_num += 1
    good_num_calc_text = font.render(str(good_num), True, (0, 0, 0))

# Bad 개수 계산 텍스트
bad_num_calc_text = font.render(str(bad_num), True, (0, 0, 0))
def bad_add():
    global bad_num_calc_text
    global bad_num
    bad_num += 1
    bad_num_calc_text = font.render(str(bad_num), True, (0, 0, 0))

# Bad 개수 계산 텍스트
total_num_calc_text = font.render(str(total_hit_num), True, (0, 0, 0))
def total_update():
    global total_num_calc_text
    global total_hit_num
    total_hit_num = perfect_num + good_num + bad_num
    total_num_calc_text = font.render(str(total_hit_num), True, (0, 0, 0))

# 판정 이미지
perfect_text = pygame.image.load("assets/perfect_text.png").convert_alpha()
good_text = pygame.image.load("assets/good_text.png").convert_alpha()
bad_text = pygame.image.load("assets/bad_text.png").convert_alpha()

# 이미지 위치 조정 변수
add_val = 0
text_p_posx = 200
text_g_posx = 200
text_b_posx = 200

print(perfect_text.get_size(), good_text.get_size(), bad_text.get_size())

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

            # 판정  // Perfect - 300, Good - 150, Bad - 50, Miss - 0
            for each_note in note_group:
                if key_input[pygame.K_s]:
                    lane_light_s = "S"
                    if each_note.key == "S":
                        if per_start <= each_note.rect.centery <= per_last:
                            # 애니메이션 겹침 방지용 변수 초기화
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()  # 친 노트 객체 삭제
                            note_hit_time = time.time()  # 노트를 친 순간 기록
                            score_add(300)  # 점수 추가
                            perfect_add()  # 퍼펙 개수 1 추가
                            total_update()  # 전체 개수
                            perfect_input = True

                        elif per_start - 15 <= each_note.rect.centery <= per_last + 15:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(150)
                            good_add()  # Good 개수 1 추가
                            total_update()  # 전체 개수
                            good_input = True

                        elif per_start - 40 <= each_note.rect.centery <= per_last + 40:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(50)
                            bad_add()  # Bad 개수 1 추가
                            total_update()  # 전체 개수
                            bad_input = True

                if key_input[pygame.K_d]:
                    lane_light_d = "D"
                    if each_note.key == "D":
                        if per_start <= each_note.rect.centery <= per_last:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(300)
                            perfect_add()  # 퍼펙 개수 1 추가
                            total_update()  # 전체 개수
                            perfect_input = True

                        elif per_start - 15 <= each_note.rect.centery <= per_last + 15:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(150)
                            good_add()  # Good 개수 1 추가
                            total_update()  # 전체 개수
                            good_input = True

                        elif per_start - 40 <= each_note.rect.centery <= per_last + 40:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(50)
                            bad_add()  # Bad 개수 1 추가
                            total_update()  # 전체 개수
                            bad_input = True

                if key_input[pygame.K_k]:
                    lane_light_k = "K"
                    if each_note.key == "K":
                        if per_start <= each_note.rect.centery <= per_last:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(300)
                            perfect_add()  # 퍼펙 개수 1 추가
                            total_update()  # 전체 개수
                            perfect_input = True

                        elif per_start - 15 <= each_note.rect.centery <= per_last + 15:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(150)
                            good_add()  # Good 개수 1 추가
                            total_update()  # 전체 개수
                            good_input = True

                        elif per_start - 40 <= each_note.rect.centery <= per_last + 40:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(50)
                            bad_add()  # Bad 개수 1 추가
                            total_update()  # 전체 개수
                            bad_input = True

                if key_input[pygame.K_l]:
                    lane_light_l = "L"
                    if each_note.key == "L":
                        if per_start <= each_note.rect.centery <= per_last:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(300)
                            perfect_add()  # 퍼펙 개수 1 추가
                            total_update()  # 전체 개수
                            perfect_input = True

                        elif per_start - 15 <= each_note.rect.centery <= per_last + 15:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(150)
                            good_add()  # Good 개수 1 추가
                            total_update()  # 전체 개수
                            good_input = True

                        elif per_start - 40 <= each_note.rect.centery <= per_last + 40:
                            perfect_input = False
                            good_input = False
                            bad_input = False
                            add_val = 0

                            each_note.kill()
                            note_hit_time = time.time()
                            score_add(50)
                            bad_add()  # Bad 개수 1 추가
                            total_update()  # 전체 개수
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
        elapsed = now - note_hit_time
        if elapsed <= 0.2:
            # 다른 판정 변수 다 False 해준 뒤, screen blit.
            good_input = False
            bad_input = False

            # Perfect 애니메이션
            add_val += 6
            if add_val > 255:
                add_val = 255
            perfect_text.set_alpha(255 - add_val)  # 흐릿하게
            screen.blit(perfect_text, (200 * (1 / add_val) + text_p_posx, 50))  # 오른쪽에서 왼쪽으로 슬라이딩 이펙트
        else:
            perfect_input = False
            add_val = 0

    elif good_input:
        now = time.time()
        elapsed = now - note_hit_time
        if elapsed <= 0.2:
            perfect_input = False
            bad_input = False

            # Good 애니메이션
            add_val += 6
            if add_val > 255:
                add_val = 255
            good_text.set_alpha(255 - add_val)  # 흐릿하게
            screen.blit(good_text, (200 * (1 / add_val) + text_g_posx, 50))  # 오른쪽에서 왼쪽으로 슬라이딩 이펙트
        else:
            good_input = False
            add_val = 0

    elif bad_input:
        now = time.time()
        elapsed = now - note_hit_time
        if elapsed <= 0.2:
            perfect_input = False
            good_input = False

            # Bad 애니메이션
            add_val += 6
            if add_val > 255:
                add_val = 255
            bad_text.set_alpha(255 - add_val)  # 흐릿하게
            screen.blit(bad_text, (200 * (1 / add_val) + text_b_posx, 50))  # 오른쪽에서 왼쪽으로 슬라이딩 이펙트
        else:
            bad_input = False
            add_val = 0

    # 오른쪽 네모박스 속 요소들
    # score
    screen.blit(score_text, (520, 30))
    screen.blit(score_calc_text, (650, 33))

    # Perfect 개수
    screen.blit(perfect_num_text, (520, 90))
    screen.blit(perfect_num_calc_text, (685, 93))

    # Good 개수
    screen.blit(good_num_text, (520, 120))
    screen.blit(good_num_calc_text, (630, 123))

    # Bad 개수
    screen.blit(bad_num_text, (520, 150))
    screen.blit(bad_num_calc_text, (600, 153))

    # Total 개수
    screen.blit(total_hit_num_text, (520, 180))
    screen.blit(total_num_calc_text, (640, 183))


    # 화면에 그리기 업데이트
    for each_note in note_group:
        pygame.draw.rect(screen, (0,0,0), [each_note.rect.centerx, each_note.rect.centery, 20, 20])

    pygame.draw.rect(screen, (0, 0, 255), [70, per_start - 40, 390, per_last + 80 - per_start])
    pygame.draw.rect(screen, (0, 255, 0), [70, per_start - 15, 390, per_last + 30 - per_start])
    pygame.draw.rect(screen, (255,0,0), [70, per_start, 390, per_last - per_start])

    note_group.draw(screen)
    note_group.update(HEIGHT)
    pygame.display.update()

pygame.quit()