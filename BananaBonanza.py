import pygame
from pygame.locals import *
from font_stuff import *
import math


class Image:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(f'{image}')
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


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


building_values = [1, 3, 10, 50, 100, 500, 2000, 10000, 40000]
cost_of_building = [10, 100, 1000, 10000, 100000, 1*(10**6), 1*(10**7), 1*(10**8), 1*(10**9)]
tree = [False, False, False, False, False]


def initialize_game(surface):
    surface.fill((255, 255, 255))
    background_img = Image(0, 0, 'background.png')
    background_img.draw(surface)
    bush_button = Button((255, 255, 255), 800, 15, 200, 75, 'Banana Bush')
    tree_button = Button((255, 255, 255), 800, 100, 200, 75, 'Banana Tree')
    field_button = Button((255, 255, 255), 800, 185, 200, 75, 'Banana Field')
    factory_button = Button((255, 255, 255), 800, 270, 200, 75, 'Banana Factory')
    city_button = Button((255, 255, 255), 800, 355, 200, 75, 'Banana City')
    state_button = Button((255, 255, 255), 800, 440, 200, 75, 'Banana State')
    country_button = Button((255, 255, 255), 800, 525, 200, 75, 'Banana Country')
    empire_button = Button((255, 255, 255), 800, 610, 200, 75, 'Banana Empire')
    takeover_button = Button((255, 255, 255), 800, 695, 200, 75, 'Banana Takeover')
    bush_img = Image(730, 20, 'banana_bush.png')
    tree_img = Image(720, 105, 'banana_tree.png')
    farm_img = Image(710, 190, 'banana_field.png')
    factory_img = Image(710, 275, 'banana_factory.png')
    city_img = Image(605, 310, 'banana_city.png')
    state_img = Image(710, 445, 'banana_state.png')
    country_img = Image(710, 510, 'banana_country.png')
    empire_img = Image(635, 595, 'banana_empire.png')
    takeover_img = Image(720, 700, 'banana_takeover.jpg')
    takeover_background = Image(0,0, 'banana_takeover.png')
    buttons = [bush_button, tree_button, field_button, factory_button, city_button, state_button, country_button,
               empire_button, takeover_button]
    backgrounds = [background_img,takeover_background]
    images = [bush_img, tree_img, farm_img, factory_img, city_img, state_img, country_img, empire_img, takeover_img]
    for button in buttons:
        button.draw(surface, 30, outline=(0, 0, 0))
    return buttons, images, backgrounds


def button_drawing(surface, buttons, building_amounts, banana_amount, takeover):
    i = 0
    for button in buttons:
        button.draw(surface, 30, outline=(0, 0, 0))
        font = pygame.font.SysFont('comicsans', 35)
        font1 = pygame.font.SysFont('comicsans', 20)
        if button in building_amounts:
            text = font.render(f'{building_amounts[button][0]}', True, 'black')
            if i >= 5:
                text1 = font1.render("{:.2e}".format(building_amounts[button][2]), True, 'black')
                text2 = font1.render(f"{building_values[i]} bps", True, 'black')
            else:
                text1 = font1.render(f'{building_amounts[button][2]}', True, 'black')
                text2 = font1.render(f"{building_values[i]} bps", True, 'black')
            surface.blit(text, (button.x + 160, button.y + 45))
            surface.blit(text1, (button.x + 20, button.y + 45))
            surface.blit(text2, (button.x + 20, button.y + 30))
        else:
            building_amounts[button] = [0, building_values[i], cost_of_building[i]]
            text = font.render(f'{building_amounts[button][0]}', True, 'black')
            text1 = font1.render(f'{building_amounts[button][2]}', True, 'black')
            surface.blit(text, (button.x + 160, button.y + 45))
            surface.blit(text1, (button.x + 20, button.y + 45))
        i += 1
    if not takeover:
        title_box = Button('white', (pygame.Surface.get_width(surface) / 2) - 300, 15, 300, 100, 'Banana Bonanza')
        title_box.draw(surface, 45, outline=(0, 0, 0))
        credits_box = Button('white', 0, 0, 0, 0, 'Created by Connor Escajeda')
        credits_box.print_text(surface, 27, 233, 50)
        banana_box = Button('white', 0, 0, 0, 0,  f"You have {banana_amount} bananas")
        banana_box.print_text(surface, 40, 200, 120)
        reset_button = Button('white', 0, 0, 0, 0, '')
    else:
        takeover_box = Button('white', 0, 0, 0, 0, 'THE BANANAS HAVE WON')
        takeover_box.print_text(surface, 40, 150, 20)
        banana_box = Button('white', 0, 0, 0, 0, f'There are {banana_amount} sentient bananas')
        banana_box.print_text(surface, 35, 60, 60)
        reset_button = Button('black', 420, 310, 280, 30, 'Click to create a new universe')
        reset_button.draw(surface, 30, outline=None)
    return reset_button


def redraw_window(surface, buttons, building_amounts, banana_amount, images, backgrounds):
    surface.fill((255, 255, 255))
    if building_amounts != {}:
        takeover = False
        if building_amounts[buttons[-1]][0] >= 1:
            takeover = True
    else:
        takeover = False
    if takeover:
        backgrounds[1].draw(surface)
        banana_button = Button((0, 160, 0), 400, 500, 100, 75, '')
    else:
        backgrounds[0].draw(surface)
        for image in images:
            image.draw(surface)
        the_tree(banana_amount, surface)
        banana_button = Button((0, 160, 0), 400, 500, 100, 75, '')
        banana_button.draw(surface, 30, outline=None)
        banana_img = Image(415, 520, 'banana.png')
        banana_img.draw(surface)
    reset_button = button_drawing(surface, buttons, building_amounts, banana_amount, takeover)
    return banana_button, reset_button


def the_tree(banana_amount, surface):
    monocle_img = Image(130, 310, 'monocle.png')
    moustache_img = Image(140, 325, 'moustache.png')
    eye_img = Image(195, 290, 'eye.png')
    tophat_img = Image(157, 220, 'tophat.png')
    cigar_img = Image(90, 320, 'cigar.png')
    hatdecoration_img = Image(170, 227, 'hatdecoration.png')
    if banana_amount >= 10000:
        tree[0] = True
    if banana_amount >= 150000:
        tree[1] = True
    if banana_amount >= 1000000:
        tree[2] = True
    if banana_amount >= 1.5*(10**9):
        tree[3] = True
    if banana_amount >= 2.5*(10**9):
        tree[4] = True
    if tree[0]:
        moustache_img.draw(surface)
    if tree[1]:
        monocle_img.draw(surface)
        eye_img.draw(surface)
    if tree[2]:
        tophat_img.draw(surface)
    if tree[3]:
        cigar_img.draw(surface)
    if tree[4]:
        hatdecoration_img.draw(surface)


def main():
    pygame.init()
    surface = pygame.display.set_mode((1024, 785))
    takeover_amount = 0
    running = True
    building_amounts = {}
    buttons, images, backgrounds = initialize_game(surface)
    clock = Time()
    banana_amount = 0
    while running:
        banana_button, reset_button = redraw_window(surface, buttons, building_amounts, banana_amount, images, backgrounds)
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
                    banana_amount += 100000000
                if reset_button.is_over(pos):
                    building_amounts = {}
                    banana_amount = 0
                    clock = Time()
                    for i in range(len(tree)):
                        tree[i] = False
                    for i in range(len(building_values)):
                        building_values[i] *= 1.5
                        building_values[i] = math.ceil(building_values[i])
                    takeover_amount += 1
            if event.type == MOUSEMOTION:
                for button in buttons:
                    if button.is_over(pos):
                        button.color = (128, 128, 128)
                    else:
                        button.color = (255, 255, 255)
        pygame.display.update()
    pygame.quit()


main()


