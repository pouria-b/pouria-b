# سومین عدد از سمت راست یک باشد
import pygame

# روش اول

# pygame.init()
# screen = pygame.display.set_mode((900, 700))
# pygame.display.set_caption("Automata")
# blue = (46, 196, 182)
# white = (253, 255, 230)
#
# img = pygame.image.load('at.png')
# screen.fill(white)
#
# pygame.draw.circle(screen, blue, (198, 175), 38)
# screen.blit(img, (65, 0))
# pygame.display.update()
#
# stats = {'000': [198, 175, 38], '001': [428, 175, 48], '010': [596, 175, 38], '011': [766, 175, 48],
#          '100': [200, 356, 38], '101': [428, 356, 48], '110': [596, 356, 38], '111': [766, 356, 48]}
# texts = ''
# text = '000'
# pygame.event.pump()
# while True:
#
#     event = pygame.event.wait()
#     if event.type == pygame.QUIT:
#         print('Quit')
#         break
#
#     l = ['0', '1']
#     if event.type == pygame.KEYDOWN:
#         print('Key Down')
#         print(event.unicode in l)
#
#         if event.unicode in l:
#             text = text + event.unicode
#             texts = texts + event.unicode
#             l3_text = text[-1:-4:-1]
#             print(l3_text)
#             font = pygame.font.Font(None, 36)
#             strings = font.render(texts, True, (0, 0, 0))
#
#             if l3_text == '000':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['000'][0], stats['000'][1]), radius=stats['000'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '001':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['001'][0], stats['001'][1]), radius=stats['001'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '010':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['010'][0], stats['010'][1]), radius=stats['010'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '011':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['011'][0], stats['011'][1]), radius=stats['011'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '100':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['100'][0], stats['100'][1]), radius=stats['100'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '101':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['101'][0], stats['101'][1]), radius=stats['101'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '110':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['110'][0], stats['110'][1]), radius=stats['110'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()
#
#             elif l3_text == '111':
#                 screen.fill(white)
#                 pygame.draw.circle(screen, blue, center=(stats['111'][0], stats['111'][1]), radius=stats['111'][2])
#                 screen.blit(img, (65, 0))
#                 screen.blit(strings, (50, 500))
#                 pygame.display.update()
#                 pygame.event.pump()

# روش دوم

pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Automata")
blue = (46, 196, 182)
white = (253, 255, 230)

img = pygame.image.load('at.png')
screen.fill(white)

pygame.draw.circle(screen, blue, (198, 175), 38)
screen.blit(img, (65, 0))
pygame.display.update()

stats = {'000': ['000', '100', 198, 175, 38], '001': ['000', '100', 428, 175, 48], '010': ['001', '101', 596, 175, 38], '011': ['001', '101', 766, 175, 48],
         '100': ['010', '110', 200, 356, 38], '101': ['010', '110', 428, 356, 48], '110': ['011', '111', 596, 356, 38], '111': ['011', '111', 766, 356, 48]}
texts = ''
text = '000'
pygame.event.pump()
while True:

    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        print('Quit')
        break

    l = ['0', '1']
    if event.type == pygame.KEYDOWN:
        print('Key Down')

        if event.unicode in l:
            texts = texts + event.unicode
            l3_text = text[-1:-4:-1]
            font = pygame.font.Font(None, 36)
            strings = font.render(texts, True, (0, 0, 0))

            if event.unicode == '0':
                print('state 0:', l3_text, '=', (stats[l3_text][0])[::-1])
                stt = stats[stats[l3_text][0]]
                screen.fill(white)
                pygame.draw.circle(screen, blue, center=(stt[2], stt[3]), radius=stt[4])
                screen.blit(img, (65, 0))
                screen.blit(strings, (50, 500))
                pygame.display.update()
                pygame.event.pump()

            elif event.unicode == '1':
                print('state 1:', l3_text, '=', (stats[l3_text][1])[::-1])
                stt = stats[stats[l3_text][1]]
                screen.fill(white)
                pygame.draw.circle(screen, blue, center=(stt[2], stt[3]), radius=stt[4])
                screen.blit(img, (65, 0))
                screen.blit(strings, (50, 500))
                pygame.display.update()
                pygame.event.pump()

            text = text + event.unicode