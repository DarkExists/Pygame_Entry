import entrybox
import pygame
import sys


screen = pygame.display.set_mode((300,400))
clock = pygame.time.Clock()
MSG = entrybox.draw_text(screen,"Types Of Entries Available",None,20,(255,0,0),(10,10),blit=False)
entrybox.Entry(screen,width=280,height=30,left=10,top=50,staticalpha=150,edge=(3,3,3,3),type="alpha",msg="Alphabetic Entry")
entrybox.Entry(screen,width=280,height=30,left=10,top=entrybox.Entry.entries[-1].bottom+20,staticalpha=150,edge=(3,3,3,3),type="digit",msg="Numbers Entry")
entrybox.Entry(screen,width=280,height=30,left=10,top=entrybox.Entry.entries[-1].bottom+20,staticalpha=150,edge=(3,3,3,3),type="alnum",msg="AlphaNumeric & Symbol Entry")
entrybox.Entry(screen,width=280,height=30,left=10,top=entrybox.Entry.entries[-1].bottom+20,staticalpha=150,edge=(3,3,3,3),type="phone",msg="Phone Number Entry")
entrybox.Entry(screen,width=250,height=30,left=10,top=entrybox.Entry.entries[-1].bottom+20,staticalpha=150,edge=(3,3,3,3),type="alnum",lock=True,msg="Password Entry")

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        entrybox.Entry.inputevents_forall(event)

        if event.type == pygame.QUIT:
            run = False 

    screen.fill((255,255,255))
    screen.blit(*MSG)
    entrybox.Entry.update_all()
    pygame.display.flip()

pygame.quit()
sys.exit()
