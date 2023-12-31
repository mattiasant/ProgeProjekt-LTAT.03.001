import random
import sys
import time

import emojis
import pygame
import pyautogui

import setup
from clicker import aimlab
from dodge import väldi
from fastclick import kiireclick
from mccree import gunslinger

# Constants
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 16
FONT_NAME = 'SpaceMono-Regular.ttf'
TERMINAL_MARGIN = 16
SCROLL_SPEED = 20
scroll_y = 0
min_scroll_y = 0  # Define the minimum scroll value

introjooks = True
kysievent = False
olukord = ''
tmain = None
koodrun = False
hasrun = False

kobra = pygame.mixer.Sound('Chomp.wav')
kaktus = pygame.mixer.Sound('OOF.wav')
bandito = pygame.mixer.Sound('elbandito.wav')

# Define a font
font = pygame.font.Font(FONT_NAME, FONT_SIZE)
fontsuur = pygame.font.Font(FONT_NAME, 72)

# Terminal content
terminal_lines = []
event_lines = []
inventory = {}

# Cursor variables
cursor_visible = True
cursor_last_toggle = time.time()

# Intro messages
final_lines = [
    ("Ärkate keset kõrbe, kuuma päikese all.", True),
    ("Te ei tea kus te täpselt olete, aga hakkate rändama, et leida vastuseid.", True),
    ("Olete gunslinger oma paremates aastates, avastamas metsikut Läänt, aastal 1899.", True),
    ("Valige raskusaste: kerge/mõõdukas", True)
]

# Narrator messages
narrator_lines = [
    'Näed sahisevat põõsast... paistab nagu keegi või miski oleks seal sees.',
    'Näed taevas lendavat lindu, või on see hoopis lendav siga?',
    'Karavan sõitis teist mõõda ja sealt hüppas välja El Bandito',
    'Järsku kukkusite väiksesse orgu, kus on skorpionid! Astuge neile peale, et mitte saada nõelata!',
    'Oh ei! Te astusite vesiliiva sisse, roomake nüüd välja enne kui te upute!',
    'Karavan sõitis teist mõõda ja sealt kukkus maha seljakott'
]
# Main loop
running = False
input_lines = []  # Store individual input lines
input_text = ""
kood = ""
difficulty = "default"


def ol1():
    global olukord
    if time.time() - t1 >= 5:
        olukord = -1
        väärtus = väldi()
        if väärtus == 'Success':
            return 'pos'

        elif väärtus == 'Fail':
            return 'neg'


def ol2():
    global olukord
    if time.time() - t1 >= 5:
        olukord = -1
        väärtus = aimlab()
        if väärtus == 'Success':
            return 'pos'
        elif väärtus == 'Fail':
            return 'neg'


def ol3():
    global olukord
    if time.time() - t1 >= 5:
        olukord = -1
        väärtus = kiireclick()
        if väärtus == 'Success':
            return 'pos'
        elif väärtus == 'Fail':
            return 'neg'


if setup.setupdone:

    if setup.var1.get() == 1:
        WIDTH = pyautogui.size()[0]
        HEIGHT = pyautogui.size()[1]
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    else:
        WIDTH = 800
        HEIGHT = 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(
        emojis.encode('veri e:b:ik geim @alo palun anna meile max punktid :pleading_face::point_right::point_left:'))
    pygame.display.set_icon(pygame.image.load("removingthepolishwithchemicals.png"))

    if setup.var2.get() == 1:
        pygame.mixer.Sound.set_volume(kobra, 0.4)  # 0.4
        pygame.mixer.Sound.set_volume(kaktus, 0.8)  # 0.8
        pygame.mixer.Sound.set_volume(bandito, 0.4)  # 0.4
    else:
        pygame.mixer.Sound.set_volume(kobra, 0)
        pygame.mixer.Sound.set_volume(kaktus, 0)
        pygame.mixer.Sound.set_volume(bandito, 0)

    # Terminal properties
    TERMINAL_ROWS = HEIGHT // FONT_SIZE
    TERMINAL_COLS = WIDTH // (FONT_SIZE // 2)
    CURSOR_BLINK_INTERVAL = 0.5  # Cursor blink interval in seconds
    CURSOR_WIDTH = 2  # Width of the cursor block

    running = True

input_rect = pygame.Rect(0, HEIGHT - 90, WIDTH, 90)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_y += SCROLL_SPEED
            elif event.button == 5:  # Scroll down
                scroll_y -= SCROLL_SPEED

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                quit()

            elif event.key == pygame.K_RETURN:
                final_lines.append((input_text, False))

                if not koodrun:
                    kood = ''

                # Handle difficulty selection
                if difficulty == 'default':
                    if input_text == 'kerge':
                        difficulty = 'kerge'
                        inventory['Inventory'] = ''
                        inventory['elud'] = 6
                        inventory['Lasud'] = random.randint(3, 6)
                    elif input_text == 'mõõdukas':
                        difficulty = 'mõõdukas'
                        inventory['Inventory'] = ''
                        inventory['elud'] = 3
                        inventory['Lasud'] = random.randint(1, 3)
                    if difficulty != 'default':
                        kysievent = True
                        kysieventolukord = True
                        hasrun = True

                if input_text == 'exit' or input_text == 'logout':
                    running = False
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
                if not koodrun:
                    kood = kood[:-1]
            elif not koodrun and event.key == pygame.K_UP:
                kood += 'u'
            elif not koodrun and event.key == pygame.K_DOWN:
                kood += 'd'
            elif not koodrun and event.key == pygame.K_LEFT:
                kood += 'l'
            elif not koodrun and event.key == pygame.K_RIGHT:
                kood += 'r'
            else:
                input_text += event.unicode
                if not koodrun and event.unicode == 'b':
                    kood += event.unicode
                elif not koodrun and event.unicode == 'a':
                    kood += event.unicode

    if hasrun is True and inventory['elud'] <= 0:
        etime = time.time()
        running = False
        if time.time() - etime > 5:
            running = False
    if not koodrun and hasrun is True and input_text == 'ba':
        if kood == 'uuddlrlrba':
            koodrun = True
            kood = None
            inventory['elud'] = inventory['elud'] + 30

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    y = TERMINAL_MARGIN
    if kysievent:
        t1 = time.time()
        t0 = time.time()
        t2 = time.time()
        olukord = random.randint(0, 5)

    if olukord == 0:
        if kysievent:
            kysievent = False
            final_lines.append((narrator_lines[0], True))
        rand0 = random.randint(1, 2)
        if t0 is not None and time.time() - t0 >= 4 and rand0 == 1:
            final_lines.append(('Veider, põõsas ei ole kedagi. Aga ei noh väike skiso käibki asja juurde', True))
            t0 = None
            tmain = time.time()
            olukord = -1
        elif t0 is not None and time.time() - t0 >= 4 and rand0 == 2:
            final_lines.append(('Põõsast hüppas välja kobra, kes hammustas teid ja kaotasite 1 elu', True))
            pygame.mixer.Sound.play(kobra, 0, 0, 0)
            inventory['elud'] = inventory['elud'] - 1
            t0 = None
            olukord = -1
            tmain = time.time() + 4

    if olukord == 5:
        if kysievent:
            kysievent = False
            final_lines.append((narrator_lines[5], True))
            final_lines.append(('Seljakotist leidsite süüa ja moona', True))
            olukord = -1
            inventory['elud'] = inventory['elud'] + (random.randint(1, 2))
            inventory['Lasud'] = inventory['Lasud'] + (random.randint(1, 2))
            tmain = time.time() + 4

    elif olukord == 1:
        if kysievent:
            final_lines.append((narrator_lines[1], True))
            kysievent = False
        vaartus = ol1()
        if vaartus == 'pos':
            final_lines.append((
                               "Uurides lendavat kotkast taevas oleksite peaaegu kaktusele otsa kõndinud, aga õnneks teil olid kiired jalad",
                               True))
        elif vaartus == 'neg':
            final_lines.append(("Uurides lendavat kotkast taevas kõndisite kaktusele otsa ja kaotasite 1 elu.", True))
            pygame.mixer.Sound.play(kaktus)
            inventory['elud'] = inventory['elud'] - 1
        tmain = time.time() + 4

    elif olukord == 3:
        if kysievent:
            final_lines.append((narrator_lines[3], True))
            kysievent = False
        vaartus = ol2()
        if vaartus == 'pos':
            final_lines.append(("Suutsite kõik skorpionid surnuks astuda", True))
        elif vaartus == 'neg':
            final_lines.append(("Mingid skorpionid jäid ikka ellu ja said nõelata nii, et kaotasid 1 elu", True))
            pygame.mixer.Sound.play(kaktus)
            inventory['elud'] = inventory['elud'] - 1
        tmain = time.time() + 4

    elif olukord == 4:
        if kysievent:
            final_lines.append((narrator_lines[4], True))
            kysievent = False
        vaartus = ol3()
        if vaartus == 'pos':
            final_lines.append(
                ("Tõmbasite ennast edukalt vesiliivast välja!", True))
        elif vaartus == 'neg':
            final_lines.append(("Pingutasite liiga vähe ja vesiliiv sai teist jagu ning uppusite ära", True))
            pygame.mixer.Sound.play(kaktus)
            inventory['elud'] = inventory['elud'] - inventory['elud']
        tmain = time.time() + 4

    elif olukord == 2:
        if kysievent:
            kysievent = False
            final_lines.append((narrator_lines[2], True))
        if time.time() - t2 >= 5:
            aeg = gunslinger()
            if aeg <= 500 and inventory['Lasud'] > 0:
                final_lines.append(('Lasite El Bandito surnuks', True))
                pygame.mixer.Sound.play(bandito, 0, 0, 0)
                inventory['Lasud'] = inventory['Lasud'] - 1
                tmain = time.time() + 8
            elif aeg <= 500 and inventory['Lasud'] == 0:
                final_lines.append(('El Bandito peksis teid läbi, sest teil polnud kuule', True))
                inventory['elud'] = inventory['elud'] - 2
                tmain = time.time() + 3
            else:
                final_lines.append(
                    ('El Bandito peksis teid läbi', True))
                inventory['elud'] = inventory['elud'] - 2
                tmain = time.time() + 2
            olukord = -1

    if olukord == -1 and tmain is not None and time.time() - tmain >= 5:
        kysievent = True
        tmain = None

    pygame.display.set_caption(
        emojis.encode('veri e:b:ik geim @alo palun anna meile max punktid :pleading_face::point_right::point_left:'))

    # Blit terminal content
    invy = HEIGHT - 4 * (FONT_SIZE + 5)
    for item in inventory:
        inv_surface = font.render(f'{item}: {inventory[item]}', True, TEXT_COLOR)
        screen.blit(inv_surface, (400, invy))
        invy += 5 + FONT_SIZE

    y = TERMINAL_MARGIN + scroll_y
    for line in final_lines:
        if line[-1]:
            user_surface = font.render('C:\\Users\Alexa>', True, TEXT_COLOR)
            screen.blit(user_surface, (TERMINAL_MARGIN, y))
        else:
            user_surface = font.render('C:\\Users\Glean>', True, TEXT_COLOR)
            screen.blit(user_surface, (TERMINAL_MARGIN, y))

        words = line[0].split()  # Split the text into words
        current_line = ''  # Store the current line being constructed

        for word in words:
            test_line = current_line + word + ' '
            text_surface = font.render(test_line, True, TEXT_COLOR)
            text_width, _ = font.size(test_line)

            if text_width <= WIDTH - TERMINAL_MARGIN * 2 - 160:
                current_line = test_line
            else:

                screen.blit(font.render(current_line, True, TEXT_COLOR), (TERMINAL_MARGIN + 160, y))
                current_line = word + ' '
                y += FONT_SIZE + 5  # Move to the next line

        if current_line != '':
            screen.blit(font.render(current_line, True, TEXT_COLOR), (TERMINAL_MARGIN + 160, y))
            y += FONT_SIZE + 5  # Move to the next line for the remaining text

        y += FONT_SIZE + 5  # Move to the next line for the next entry

    pygame.draw.rect(screen, (0, 0, 0), input_rect)

    invy = HEIGHT - 4 * (FONT_SIZE + 5)
    for item in inventory:
        inv_surface = font.render(f'{item}: {inventory[item]}', True, TEXT_COLOR)
        screen.blit(inv_surface, (400, invy))
        invy += 5 + FONT_SIZE

    # Display terminal content
    luser_surface = font.render("C:\\Users\Glean>", True, TEXT_COLOR)
    screen.blit(luser_surface, (16, HEIGHT - 16 - FONT_SIZE))

    # Display the current input text
    input_surface = font.render(input_text, True, TEXT_COLOR)
    screen.blit(input_surface, (TERMINAL_MARGIN + 160, HEIGHT - 16 - FONT_SIZE))
    # Cursor blink
    if time.time() - cursor_last_toggle >= CURSOR_BLINK_INTERVAL:
        cursor_visible = not cursor_visible
        cursor_last_toggle = time.time()
    if cursor_visible:
        cursor_x = TERMINAL_MARGIN + 160 + font.size(input_text)[0]
        cursor_y = HEIGHT - TERMINAL_MARGIN - FONT_SIZE + FONT_SIZE / 3.5
        cursor_rect = pygame.Rect(cursor_x, cursor_y, CURSOR_WIDTH, FONT_SIZE)
        pygame.draw.rect(screen, TEXT_COLOR, cursor_rect)

    pygame.display.flip()

else:
    texit = time.time()
    screen.fill(BACKGROUND_COLOR)
    lopp = fontsuur.render("Geim over :(", True, TEXT_COLOR)
    lopp_rect = lopp.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    while time.time() - texit < 15:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(lopp, lopp_rect)
        pygame.display.flip()

pygame.quit()
sys.exit()
