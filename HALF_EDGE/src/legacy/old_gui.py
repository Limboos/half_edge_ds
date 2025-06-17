import pygame
from HALF_EDGE.Delauny_Triangulation import *
import cevent


class App(cevent.CEvent):
    def __init__(self,Vertex):
        self._running = True
        self._display_surf = None
        self._font = None
        self.Vertex=Vertex
        self.black = [0, 0, 0]
        self.white = [255, 255, 255]

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((800, 600), pygame.HWSURFACE)
        self._font = pygame.font.SysFont(None, 25)
        self._running = True


    def on_loop(self):
        pass
    def message_on_screen(self,msg,color,cordinates):
        screen_text = self._font.render(msg,True,color)
        self._display_surf.blit(screen_text,cordinates)
    def on_render(self):
        #self._display_surf.blit(self._image_surf, (0, 0))
        for cordinates in self.Vertex:
            pygame.draw.circle(self._display_surf,self.black,cordinates.getxy(),3)
            self.message_on_screen(str(cordinates.Vertex_id),self.black,(cordinates.getxy()[0]+5,cordinates.getxy()[1]-5))
        pygame.display.flip()
        pass
    def on_exit(self):
        self._running = False

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            self._display_surf.fill((255, 255, 255))
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
def main(V):
    theApp = App(V)
    theApp.on_execute()

