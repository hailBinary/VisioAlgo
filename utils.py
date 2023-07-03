import pygame, sys
from button import Button

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def get_button( position, text, font_size = 50, h_color = "Green", img_loc = "assets/Options Rect.png",  b_color = "White"): #return a button object

    return Button(pygame.image.load(img_loc), position, text, get_font(font_size),b_color, h_color)