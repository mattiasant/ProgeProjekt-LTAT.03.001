import pygame
import setup
import pyautogui


def kiireclick():
    pygame.init()

    if setup.var1.get()==1:
        WIDTH = pyautogui.size()[0]
        HEIGHT = pyautogui.size()[1]
        screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)

    else:
        WIDTH=800
        HEIGHT=600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

    BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
    FPS = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    game_time = 7
    pygame.display.set_caption("rulli rulli liiva sees")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Comic Sans", 28)

    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def main():
        button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, (HEIGHT - BUTTON_HEIGHT) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        clicked = False
        game_running = True
        start_time = pygame.time.get_ticks()
        click_count = 0


        while game_running:
            screen.fill(WHITE)

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            time_left = max(0, game_time*1000 - elapsed_time)

            if time_left <= 0:
                game_running = False

            draw_text(f"Aeg: {time_left:} ms", font, BLACK, screen, 10, 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos) and not clicked:
                        clicked = True
                        click_count += 1
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    clicked = False

            # Draw button
            pygame.draw.rect(screen, RED if clicked else BLACK, button_rect)
            draw_text("Click", font, WHITE, screen, button_rect.x + 20, button_rect.y + 10)


        # Display click count
            draw_text(f"klõpse: {click_count}", font, BLACK, screen, 10, 50)

            pygame.display.flip()
            clock.tick(FPS)
        if click_count < 25:
            return "Fail"
        elif click_count >= 25:
            return "Success"
        pygame.quit()

    return main()
