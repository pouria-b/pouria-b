"""Interactive DFA visualizer. Run --check STRING for a dependency-free CLI."""
import argparse
from pathlib import Path
from automaton import Automaton, accepts

# Centers/radii in the original 771 x 482 image. Labels are chronological.
POSITIONS = {
    '000': (133,175,38), '100': (363,175,48),
    '010': (531,175,38), '110': (701,175,48),
    '001': (135,356,38), '101': (363,356,48),
    '011': (531,356,38), '111': (701,356,48),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', metavar='BITS', help='Check a string without opening the GUI')
    args = parser.parse_args()
    if args.check is not None:
        try:
            accepted = accepts(args.check)
        except ValueError as exc:
            parser.error(str(exc))
        print('ACCEPTED' if accepted else 'REJECTED')
        return
    try:
        import pygame
    except ModuleNotFoundError:
        parser.exit(2, 'Install pygame using: python -m pip install -r requirements.txt\n')
    pygame.init()
    try:
        screen = pygame.display.set_mode((900,700))
        pygame.display.set_caption('DFA — Third symbol from the right is 1')
        diagram = pygame.image.load(str(Path(__file__).with_name('at.png'))).convert_alpha()
        font = pygame.font.Font(None,30)
        small = pygame.font.Font(None,25)
        machine = Automaton()
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        machine.backspace()
                    elif event.key in (pygame.K_DELETE,pygame.K_r):
                        machine.reset()
                    elif event.unicode in ('0','1'):
                        machine.feed(event.unicode)
            screen.fill((253,255,230))
            screen.blit(diagram,(65,0))
            x,y,radius = POSITIONS[machine.state]
            # Overlay ring remains visible regardless of source image transparency.
            pygame.draw.circle(screen,(0,125,105),(x+65,y),radius+6,4)
            status = 'ACCEPTED' if machine.accepted else 'REJECTED'
            lines = [f'Input ({len(machine.text)} bits): ...{machine.text[-40:]}' if len(machine.text)>40 else f'Input: {machine.text or "(empty)"}',
                     f'State: q{machine.state} | {status}',
                     'Rule: at least 3 symbols, with 1 in the third position from the right.',
                     '0/1: append | Backspace: undo | R/Delete: reset | Esc: quit']
            for i,line in enumerate(lines):
                screen.blit((font if i<2 else small).render(line,True,(25,40,35)),(35,505+i*38))
            pygame.display.flip()
            clock.tick(30)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
