import pygame
from pygame.locals import *
from font_stuff import *


bush_img = pygame.image.load('banana_bush.png')
tree_img = pygame.image.load('banana_tree.png')
farm_img = pygame.image.load('banana_field.png')
factory_img = pygame.image.load('banana_factory.png')
city_img = pygame.image.load('banana_city.png')
state_img = pygame.image.load('banana_state.png')
country_img = pygame.image.load('banana_country.png')
empire_img = pygame.image.load('banana_empire.png')
takeover_img = pygame.image.load('banana_takeover.png')
background_img = pygame.image.load('background.png')
banana_img = pygame.image.load('banana.png')
building_values = [1, 3, 10, 50, 100, 500, 2000, 10000, 40000]
cost_of_building = [10, 100, 1000, 10000, 100000, 1*(10**6), 1*(10**7), 1*(10**8), 1*(10**9)]


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def __repr__(self):
        return f'{self.text}'

    def draw(self, surface, font_size, outline=None):
        if outline:
            pygame.draw.rect(surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), border_radius=30)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=30)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', font_size)
            text1 = textHollow(font, self.text, (0, 0, 0))
            text2 = textOutline(font, self.text, (255, 255, 0), (0, 0, 0))
            surface.blit(text1, (self.x + (self.width / 2 - text1.get_width() / 2), self.y + 5))
            surface.blit(text2, (self.x + (self.width / 2 - text2.get_width() / 2), self.y + 5))

    def print_text(self, surface, font_size, x, y):
        font = pygame.font.SysFont('comicsans', font_size)
        text1 = textHollow(font, self.text, (0, 0, 0))
        text2 = textOutline(font, self.text, (255, 255, 0), (0, 0, 0))
        surface.blit(text1, (x, y + 5))
        surface.blit(text2, (x, y + 5))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


class Time:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.frame_rate = 30
        self.frame_count = 0
        self.font = pygame.font.SysFont('comicsans', 35)

    def what_time(self, buttons, building_amounts, banana_amount):
        total_seconds = self.frame_count // self.frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_string = 'Time: {0:02}:{1:02}'.format(minutes, seconds)
        text = self.font.render(time_string, True, 'black')
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            for button in buttons:
                bananas_produced = building_amounts[button][0] * building_amounts[button][1]
                banana_amount += bananas_produced
        self.clock.tick(self.frame_rate)
        return text, banana_amount


def initialize_game(surface):
    surface.fill((255, 255, 255))
    surface.blit(background_img, (0, 0))
    bush_button = Button((255, 255, 255), 800, 15, 200, 75, 'Banana Bush')
    tree_button = Button((255, 255, 255), 800, 100, 200, 75, 'Banana Tree')
    field_button = Button((255, 255, 255), 800, 185, 200, 75, 'Banana Field')
    factory_button = Button((255, 255, 255), 800, 270, 200, 75, 'Banana Factory')
    city_button = Button((255, 255, 255), 800, 355, 200, 75, 'Banana City')
    state_button = Button((255, 255, 255), 800, 440, 200, 75, 'Banana State')
    country_button = Button((255, 255, 255), 800, 525, 200, 75, 'Banana Country')
    empire_button = Button((255, 255, 255), 800, 610, 200, 75, 'Banana Empire')
    takeover_button = Button((255, 255, 255), 800, 695, 200, 75, 'Banana Takeover')
    buttons = [bush_button, tree_button, field_button, factory_button, city_button, state_button, country_button,
               empire_button, takeover_button]
    for button in buttons:
        button.draw(surface, 30, outline=(0, 0, 0))
    return buttons


def redraw_window(surface, buttons, building_amounts, banana_amount):
    surface.fill((255, 255, 255))
    surface.blit(background_img, (0, 0))
    i = 0
    for button in buttons:
        button.draw(surface, 30, outline=(0, 0, 0))
        font = pygame.font.SysFont('comicsans', 35)
        font1 = pygame.font.SysFont('comicsans', 20)
        if button in building_amounts:
            text = font.render(f'{building_amounts[button][0]}', True, 'black')
            text1 = font1.render(f'{building_amounts[button][2]}', True, 'black')
            surface.blit(text, (button.x + 160, button.y + 45))
            surface.blit(text1, (button.x + 20, button.y + 45))
        else:
            building_amounts[button] = [0, building_values[i], cost_of_building[i]]
            text = font.render(f'{building_amounts[button][0]}', True, 'black')
            text1 = font1.render(f'{building_amounts[button][2]}', True, 'black')
            surface.blit(text, (button.x + 160, button.y + 45))
            surface.blit(text1, (button.x + 20, button.y + 45))
        i += 1
    banana_button = Button((0, 160, 0), 109, 275, 200, 150, '')
    banana_button.draw(surface, 30, outline=None)
    next1 = 20
    images = [bush_img, tree_img, farm_img, factory_img, city_img, state_img, country_img, empire_img, takeover_img]
    surface.blit(banana_img, (banana_button.x + (banana_button.width / 2), banana_button.y + (banana_button.height / 2)))
    for image in images:
        surface.blit(image, (725, next1))
        next1 += 85
    title_box = Button('white', (pygame.Surface.get_width(surface) / 2) - 300, 15, 300, 100, 'Banana Bonanza')
    title_box.draw(surface, 45, outline=(0, 0, 0))
    credits_box = Button('white', 0, 0, 0, 0, 'Created by Connor Escajeda')
    credits_box.print_text(surface, 27, 233, 50)
    banana_box = Button('white', 0, 0, 0, 0, f'You have {banana_amount} bananas')
    banana_box.print_text(surface, 40, 400, 400)
    return banana_button


def main():
    pygame.init()
    surface = pygame.display.set_mode((1024, 785))
    running = True
    building_amounts = {}
    buttons = initialize_game(surface)
    clock = Time()
    banana_amount = 0
    while running:
        banana_button = redraw_window(surface, buttons, building_amounts, banana_amount)
        text, banana_amount = clock.what_time(buttons, building_amounts, banana_amount)
        surface.blit(text, (20, 180))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                i = 0
                for button in buttons:
                    if button.is_over(pos):
                        if button in building_amounts and banana_amount >= building_amounts[button][2]:
                            building_amounts[button][0] += 1
                            banana_amount -= building_amounts[button][2]
                            building_amounts[button][2] += int(((building_amounts[button][2] * .12) // 1))
                        i += 1
                if banana_button.is_over(pos):
                    banana_amount += 1
            if event.type == MOUSEMOTION:
                for button in buttons:
                    if button.is_over(pos):
                        button.color = (0, 0, 0)
                    else:
                        button.color = (255, 255, 255)
        pygame.display.update()
    pygame.quit()

main()
