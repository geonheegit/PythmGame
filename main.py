import pygame
import note

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode([800, 600])

# 화면 택스처
main_bg = pygame.image.load("assets/main_bg.png")  # 80 x 60 px
main_bg = pygame.transform.scale(main_bg, (800, 600))  # 800 x 600 px

# 레인 밝히는 효과
lane_lighting = pygame.image.load("assets/lane_lighting.png").convert_alpha()  # 9 x 60 px
lane_lighting = pygame.transform.scale(lane_lighting, (100, 600))  # 100 x 600 px

# FPS
clock = pygame.time.Clock()
clock.tick(60)

# 폰트
font = pygame.font.SysFont("arial", 30, True, False)
text_color = (0, 0, 0)

# 노트
testnote = note.Note()

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
            key_input = pygame.key.get_pressed()

            if key_input[pygame.K_s]:
                lane_light_s = "S"

            if key_input[pygame.K_d]:
                lane_light_d = "D"

            if key_input[pygame.K_k]:
                lane_light_k = "K"

            if key_input[pygame.K_l]:
                lane_light_l = "L"
            
            # 스크롤 속도
            if event.key == pygame.K_UP:
                testnote.scroll_speed += 1
                
            if event.key == pygame.K_DOWN:
                testnote.scroll_speed -= 1
                
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


    testnote.image_rect.y += testnote.scroll_speed
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


    screen.blit(testnote.image, testnote.image_rect)
    pygame.display.update()

pygame.quit()