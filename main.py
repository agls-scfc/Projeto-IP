import pygame
from src.entities.enemy import Enemy
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Mario Carne")
    clock = pygame.time.Clock()

    inimigo= Enemy(400,300)

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        inimigo.update()          

        screen.fill((0, 0, 0))
        inimigo.draw(screen) 
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
