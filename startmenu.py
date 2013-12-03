from pygame.locals import *
import pygame

class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.background_color = (160,217,92)
        self.menu_background_color = (71,163,255)
        self.start_button_color = (255,0,0)
        self.menu_button_color = (71,163,255)
        self.selected_button_color = (255,215,0)
        self.n_players = False
        
        self.rect_text =    Rect(100,100,400,100)
        self.rect_button1 = Rect(200,200,200,100)
        self.rect_button2 = Rect(200,300,200,100)
        self.rect_button3 = Rect(200,400,200,100)
        self.rect_button4 = Rect(200,600,200,100)
        
        self.start_screen_text = self.screen.subsurface(
            self.rect_text)
        self.start_screen_button1 = self.screen.subsurface(
            self.rect_button1)
        self.start_screen_button2 = self.screen.subsurface(
            self.rect_button2)
        self.start_screen_button3 = self.screen.subsurface(
            self.rect_button3)
        self.start_screen_button4 = self.screen.subsurface(
            self.rect_button4)
            
    def display_menu(self):
        """display the start screen"""
        self.screen.fill(self.background_color)
        border_color = (0,0,0)
        game_area_rect = (0,0,900,900)
        border_width = 4
        
        self.start_screen_text.fill(self.menu_background_color)
        
        if self.n_players == 1:
            self.start_screen_button1.fill(self.selected_button_color)
        else:
            self.start_screen_button1.fill(self.menu_button_color)
            
        if self.n_players == 2:
            self.start_screen_button2.fill(self.selected_button_color)
        else:
            self.start_screen_button2.fill(self.menu_button_color)
            
        if self.n_players == 3:
            self.start_screen_button3.fill(self.selected_button_color)
        else:
            self.start_screen_button3.fill(self.menu_button_color)
            
        self.start_screen_button4.fill(self.start_button_color)
        
        pygame.draw.rect(
            self.start_screen_text,
            border_color,
            Rect(0,0,400,100),
            border_width)
        pygame.draw.rect(
            self.start_screen_button1,
            border_color,
            Rect(0,0,200,100),
            border_width)
        pygame.draw.rect(
            self.start_screen_button2,
            border_color,
            Rect(0,0,200,100),
            border_width)
        pygame.draw.rect(
            self.start_screen_button3,
            border_color,
            Rect(0,0,200,100),
            border_width)
        pygame.draw.rect(
            self.start_screen_button4,
            border_color,
            Rect(0,0,200,100),
            border_width)
            
        myfont = pygame.font.SysFont("monospace", 45, bold=True)
        t = lambda text: myfont.render(text, 1, (0,0,0))
        self.start_screen_text.blit(t('Num. Computers'), (12, 25))
        self.start_screen_button1.blit(t('1'), (90, 25))
        self.start_screen_button2.blit(t('2'), (90, 25))
        self.start_screen_button3.blit(t('3'), (90, 25))
        self.start_screen_button4.blit(t('Start!'), (25, 25))
        
        pygame.display.flip()
        
    def mouse_click_button(self, position):
        """If mouse clicks button update vars
        otherwise Return False
        """
        if self.rect_button1.collidepoint(position):
            self.n_players = 1
            return None
        if self.rect_button2.collidepoint(position):
            self.n_players = 2
            return None
        if self.rect_button3.collidepoint(position):
            self.n_players = 3
            return None
        if self.rect_button4.collidepoint(position):
            if self.n_players:
                return True
        else:
            return False
        
        
