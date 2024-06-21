import pygame

class FoodEngine:
    class Ingredient:

        def __init__(self, name, icon):
            self.name: str = name
            self.icon = icon

        def get_system_name(self):
            return self.icon.split("/")[-1].split(".")[0]

        def __repr__(self):
            return f"{self.name}"


    class Dish:

        def __init__(self, name, image, recipe: list):
            self.name = name
            self.recipe: list = recipe
            self.image: str = image

        def is_that_ingredients(self, ingredients: list):
            recipe_names = []
            ingredients_names = []
            if len(ingredients) >= 1:

                if type(ingredients[0]) is str:
                    ingredients_names = ingredients
                else:
                    i: FoodEngine.Ingredient
                    for i in ingredients:
                        ingredients_names.append(i.get_system_name())
                i: FoodEngine.Ingredient
                for i in self.recipe:
                    recipe_names.append(i.get_system_name())

                print()
                print(recipe_names)
                print(ingredients_names)

                return set(recipe_names) == set(ingredients_names)

        def __repr__(self):
            return f"{self.name}"


    rice = Ingredient("Рис", "image/rice.png")
    nori = Ingredient("Лист Нори", "image/nori.png")
    cottage_cheese = Ingredient("Творожный сыр", "image/cottage_cheese.png")
    chicken_fillet = Ingredient("Куринное филе", "image/chicken_fillet.png")
    cucumber = Ingredient("Огурец", "image/cucumber.png")
    spicy_sauce = Ingredient("Спайси соус", "image/spicy_sauce.png")
    parmesan_cheese = Ingredient("Сыр пармезан", "image/parmesan_cheese.png")
    seven = Ingredient("Сёмга", "image/seven.png")
    mayonese = Ingredient("Майонез", "image/mayonese.png")
    unagi_sauce = Ingredient("Унаги соус", "image/unagi_sauce.png")
    sesame_seeds = Ingredient("Семена кунжута", "image/sesame_seeds.png")
    panko = Ingredient("Панко (Сухари)", "image/panko.png")
    tobiko_caviar = Ingredient("Икра Тобико", "image/tobiko_caviar.png")
    acne = Ingredient("Угорь", "image/acne.png")

    ingredients = [rice, nori, cottage_cheese, chicken_fillet, cucumber, spicy_sauce,
                   parmesan_cheese, seven, mayonese, unagi_sauce, sesame_seeds,
                   panko, tobiko_caviar, acne]

    chicken_spicy = Dish("Чиккен Спайси",
                         "image/chicken_spicy.png",
                         [rice, nori, cottage_cheese, chicken_fillet, cucumber, spicy_sauce])

    karolina_maki = Dish("Каролина Маки",
                         "image/karolina_maki.png",
                         [rice, nori, cottage_cheese, seven, parmesan_cheese, tobiko_caviar])

    alaska = Dish("Аляска",
                  "image/alaska.png",
                  [rice, nori, cottage_cheese, seven, cucumber, acne, mayonese, parmesan_cheese, unagi_sauce, sesame_seeds])

    chicken_tempura = Dish("Чиккен темпура",
                           "image/chicken_tempura.png",
                           [rice, nori, cottage_cheese, chicken_fillet, cucumber, panko])

    tobiko_maki = Dish("Тобико Маки",
                       "image/tobiko_maki.png",
                       [rice, nori, cottage_cheese, seven, cucumber, tobiko_caviar])

    philadelfia = Dish("Филадельфия",
                       "image/philadelfia.png",
                       [rice, nori, cottage_cheese, seven, cucumber])

    dishes = [chicken_spicy, karolina_maki, alaska, chicken_tempura, tobiko_maki, philadelfia]


class LevelsData:

    class Level:

        def __init__(self, dialogs, name):
            self.levelName = name
            self.cur_dialog = 0
            self.dialogs: list = dialogs

        def get_dish(self):
            if self.cur_dialog <= len(self.dialogs) - 1:
                data: LevelsData.Dialog = self.dialogs[self.cur_dialog]
                return data.dish.image.split("/")[-1].split(".")[0]
            else:
                return None

        def get_success_dialog(self):
            if self.cur_dialog <= len(self.dialogs) - 1:
                data: LevelsData.Dialog = self.dialogs[self.cur_dialog]
                return data.successDialog
            else:
                return None

        def get_miss_dialog(self):
            if self.cur_dialog <= len(self.dialogs) - 1:
                data: LevelsData.Dialog = self.dialogs[self.cur_dialog]
                return data.missDialog
            else:
                return None

        def next_dialog(self):
            self.cur_dialog += 1

        def get_character(self):
            if self.cur_dialog <= len(self.dialogs) - 1:
                data: LevelsData.Dialog
                data = self.dialogs[self.cur_dialog].character
                print(data)
                return data
            else:
                return None

        def get_dialog(self):
            if self.cur_dialog <= len(self.dialogs) - 1:
                data: LevelsData.Dialog
                data = self.dialogs[self.cur_dialog].dialog
                return data
            else:
                return None


    class Dialog:

        def __init__(self, dialog, missDialog, successDialog, character, dish):
            self.dialog = dialog
            self.missDialog = missDialog
            self.successDialog = successDialog
            self.character = character
            self.dish = dish


    dialog = [
        "Hello, can I get Tobico Maki?"
    ]
    miss_dialog = [
        "It's not that I wanted!"
    ]
    success_dialog = [
        "Oh... Excellent! Thank you!\nClick to continue."
    ]
    dish = FoodEngine.tobiko_maki
    character = [
        "image/characters/bob/bob1.png",
        "image/characters/bob/bob2.png",
        "image/characters/bob/bob3.png",
        "image/characters/bob/bob4.png"
    ]

    bob = Dialog(dialog, miss_dialog, success_dialog, character, dish)

    dialog = [
        "Hi, gimme Chicken Tempura."
    ]
    success_dialog = [
        "Oh, man! It's a super dish!\nClick to continue."
    ]
    miss_dialog = [
        "It's a trash! Gimme Chicken Tempura"
    ]
    dish = FoodEngine.chicken_tempura
    character = [
        "image/characters/street_boy/street_boy1.png",
        "image/characters/street_boy/street_boy2.png",
        "image/characters/street_boy/street_boy3.png",
        "image/characters/street_boy/street_boy4.png"
    ]
    street_boy = Dialog(dialog, miss_dialog, success_dialog, character, dish)

    dialog = [
        "Hello, Tovarich! Can I have Philadelfia?"
    ]
    success_dialog = [
        "Spacibo you, Tovarich! See you later\nClick to continue."
    ]
    miss_dialog = [
        "Are joking me?! I want PHILADELFIA!"
    ]
    dish = FoodEngine.philadelfia
    character = [
        "image/characters/ivan/ivan1.png",
        "image/characters/ivan/ivan2.png",
        "image/characters/ivan/ivan3.png",
        "image/characters/ivan/ivan4.png"
    ]
    ivan = Dialog(dialog, miss_dialog, success_dialog, character, dish)

    dialog = [
        "Hey, what's up man? I ned spicy.. Chicken Spicy MC!"
    ]
    success_dialog = [
        "What a SUPER dish, bratish!\nClick to continue."
    ]
    miss_dialog = [
        "No no no MAN, I ned Chicken Spicy"
    ]
    dish = FoodEngine.chicken_spicy
    character = [
        "image/characters/shtern/shtern1.png",
        "image/characters/shtern/shtern2.png",
        "image/characters/shtern/shtern3.png",
        "image/characters/shtern/shtern4.png"
    ]

    shtern = Dialog(dialog, miss_dialog, success_dialog, character, dish)

    dialog = [
        "- Can we have Tobiko Maki (Uber)?\n- Arghh... Again? (Yumi)"
    ]
    success_dialog = [
        "- Mmm... Great Taste!!! (Yumi)\n- As always (Uber)\nClick to continue."
    ]
    miss_dialog = [
        "No! (Uber)"
    ]
    dish = FoodEngine.tobiko_maki
    character = [
        "image/characters/vasabi/vasabi1.png",
        "image/characters/vasabi/vasabi2.png",
        "image/characters/vasabi/vasabi3.png",
        "image/characters/vasabi/vasabi4.png"
    ]

    vasabi = Dialog(dialog, miss_dialog, success_dialog, character, dish)

    dialog = [
        "- (Some japanese text) Karolina Maki！"
    ]
    success_dialog = [
        "- (Some japanese text)\nClick to continue."
    ]
    miss_dialog = [
        "(Some japanese text)!!!"
    ]
    dish = FoodEngine.karolina_maki
    character = [
        "image/characters/oren_ishi/oren_ishi1.png",
        "image/characters/oren_ishi/oren_ishi2.png",
        "image/characters/oren_ishi/oren_ishi3.png",
        "image/characters/oren_ishi/oren_ishi4.png"
    ]

    oren_ishi = Dialog(dialog, miss_dialog, success_dialog, character, dish)

    level1 = Level([bob, ivan], "lev1")
    level2 = Level([street_boy, shtern], "lev2")
    level3 = Level([vasabi, oren_ishi], "lev3")


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, group, x, y, width, height, weight, image_path):
        super().__init__(group)
        if image_path is not None:
            self.x = x + width
            self.y = y + width
            self.current_image = 0
            self.size = (weight - width, height - width)
            self.image = pygame.transform.scale(pygame.image.load(image_path), self.size)
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        else:
            self.image = pygame.image.load("image/empty.png")
            self.rect = pygame.Rect(-100, -100, 1, 1)


class AnimatedCharacter(pygame.sprite.Sprite):

    def __init__(self, group, x, y, width, height, weight, animation_list):
        super().__init__(group)
        self.x = x + width
        self.y = y + width
        self.animation_list: list = animation_list
        self.current_image = 0
        self.size = (weight - width, height - width)
        self.image = pygame.transform.scale(pygame.image.load(animation_list[self.current_image]), self.size)
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def update(self, *args, **kwargs):
        if self.current_image <= len(self.animation_list) - 1:
            self.image = pygame.transform.scale(pygame.image.load(self.animation_list[self.current_image]), self.size)
            self.current_image += 1
        else:
            self.current_image = 0
            self.image = pygame.transform.scale(pygame.image.load(self.animation_list[self.current_image]), self.size)


class CustomerWindow:

    def __init__(self, x, y, height, weight, width, screen, group, level):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.width = width
        self.screen = screen
        self.level = level
        self.customer = AnimatedCharacter(group, self.x, self.y, self.width, self.height, self.weight,
                                          self.level.get_character())

    def draw(self):
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)


class MenuWindow:

    def __init__(self, x, y, height, weight, width, screen):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.width = width
        self.screen = screen

    def draw(self):
        pygame.threads.init()
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)


def get_score():
    lvl_1_score = 0
    lvl_2_score = 0
    lvl_3_score = 0
    try:
        file = open("save.txt", "r")
        lines = file.readlines()
        file.close()
        lvl_1_score = int(lines[1].split("=")[-1].split("\n")[0])
        lvl_2_score = int(lines[2].split("=")[-1].split("\n")[0])
        lvl_3_score = int(lines[3].split("=")[-1].split("\n")[0])
        score = lvl_1_score + lvl_2_score + lvl_3_score
        return score

    except Exception as e:
        return 0


class TextBox:
    def __init__(self, x, y, height, weight, width, screen: pygame.surface.Surface, text=None):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.rect = pygame.draw.rect(screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        self.width = width
        self.score = get_score()
        if text is None:
            self.text = f"Поздравляем с завершением этой короткой, но душевной игры!\nЗа игру вы заработали: {get_score()} очков !\nСпасибо за внимание!"
        else:
            self.text = text
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 25)

    def draw(self):
        words = [word.split(" ") for word in self.text.splitlines()]
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)

        x, y = self.x + 10, self.y + 10
        space = self.font.size(' ')[0]
        for line in words:
            for word in line:
                word_surface = self.font.render(word, True, (0, 0, 255))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.weight:
                    x = self.x + 10  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = self.x + 10  # Reset the x.
            y += word_height  # Start on new row


class CustomerTextWindow:

    def __init__(self, x, y, height, weight, width, screen: pygame.surface.Surface, group, level, customer):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.rect = pygame.draw.rect(screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        self.level = level
        self.width = width
        self.text = level.get_dialog()
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 25)
        self.customer = customer

    def click(self):
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.level.get_dialog() is not None:
                if self.text == self.level.get_success_dialog():
                    self.level.next_dialog()
                    if self.level.get_dialog() is None:
                        level_completed(self.level)
                    self.next_dialog()
                    self.customer: AnimatedCharacter
                    self.customer.animation_list = self.level.get_character()
                    return
                else:
                    self.text = self.level.get_dialog()

            else:
                level_completed(self.level)

    def next_dialog(self):
        self.text = self.level.get_dialog()
        if self.level.get_dialog() is None:
            self.text = ["Level completed! Click me to finish level"]

    def draw(self):
        words = [word.split(" ") for word in self.text[0].splitlines()]
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)

        x, y = self.x + 10, self.y + 10
        space = self.font.size(' ')[0]
        for line in words:
            for word in line:
                word_surface = self.font.render(word, True, (0, 0, 255))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.weight:
                    x = self.x + 10  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = self.x + 10  # Reset the x.
            y += word_height  # Start on new row


class DishIcon(pygame.sprite.Sprite):

    def __init__(self, group, x, y, weight, height, width, icon: str, slot):
        super().__init__(group)
        self.x = x
        self.y = y
        self.vel_x = self.x
        self.vel_y = self.y
        self.size = (weight - width, height - width)
        self.slot = slot
        if icon is not None and icon != "image/empty.png":
            print("NOT NONE")
            image = pygame.image.load(icon)
            self.ingredient_name = icon.split("/")[-1].split(".")[0]
            self.ingredient_path = icon
            self.image = pygame.transform.scale(image, self.size)
            self.empty = False
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        else:
            print("INACGE")
            self.ingredient_name = "None"
            self.ingredient_path = "None"
            self.empty = True
            image = pygame.image.load("image/empty.png")
            self.image = pygame.transform.scale(image, self.size)
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def update(self, *args, **kwargs):
        self.rect = pygame.Rect(self.vel_x, self.vel_y, self.image.get_width(), self.image.get_height())


class IngredientSlot:

    def __init__(self, x, y, height, weight, width, screen, icon, group):
        self.x = x
        self.y = y
        self.height = height
        self.group = group
        self.weight = weight
        self.width = width
        self.screen = screen
        self.icon: DishIcon = DishIcon(group, x + width, y + width, weight, height, width, icon, self)
        self.slot_is_empty = self.icon.empty

    def draw(self):
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)


class IngredientsWindow:

    def __init__(self, x, y, height, weight, width, screen, group):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.width = width
        self.screen = screen
        self.slots = []
        self.group = group
        self.generate_slots(FoodEngine.ingredients)

    def generate_slots(self, ingredients):
        height = self.height
        weight = self.weight
        pos_x = self.x + 10
        pos_y = self.y + 10

        for ingredient in ingredients:
            ingredient_slot = IngredientSlot(pos_x, pos_y, 100, 100, 5, virtual_screen, ingredient.icon, self.group)
            self.slots.append(ingredient_slot)
            pos_x += 110
            if (pos_x - self.x) >= weight - 100:
                pos_x = self.x + 10
                pos_y += 110

    def draw_slots(self):
        for slot in self.slots:
            slot.draw()

    def draw(self):
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)
        self.draw_slots()


class DishSlot:
    def __init__(self, x, y, height, weight, width, screen, icon, group):
        self.x = x
        self.y = y
        self.height = height
        self.group = group
        self.weight = weight
        self.width = width
        self.screen = screen
        self.icon: DishIcon = DishIcon(group, self.x + width, self.y + width, self.weight, self.height, self.width,
                                       icon, self)
        self.slot_is_empty = self.icon.empty

    def draw(self):
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)


class RectButton:
    def __init__(self, x, y, height, weight, width, screen, group, text, command, image=None):
        self.x = x
        self.y = y
        self.height = height
        self.group = group
        self.weight = weight
        self.width = width
        self.screen: pygame.Surface = screen
        self.image = ImageSprite(group, self.x, self.y, self.width, self.height, self.weight, image)
        self.font = pygame.font.SysFont("Arial", 24)
        self.text = text
        self.text_surface = self.font.render(text, True, (0, 0, 255))
        self.command = command
        self.rect = pygame.draw.rect(screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)

    def draw(self):
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)
        self.screen.blit(self.text_surface, (
            self.x + self.text_surface.get_rect().width // 2, self.y + self.text_surface.get_rect().height // 2))


class DishWindow:

    def __init__(self, x, y, height, weight, width, screen, group, level, customer_text, customer_window):
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.customer_text: CustomerTextWindow = customer_text
        self.width = width
        self.screen = screen
        self.customer_window = customer_window
        self.group = group
        self.level = level
        self.slot_1 = IngredientSlot(self.x + 10, self.y + 10, 100, 100, 5, screen, "image/empty.png", group)
        self.slot_2 = IngredientSlot(self.slot_1.x + 110, self.y + 10, 100, 100, 5, screen, "image/empty.png", group)
        self.slot_3 = IngredientSlot(self.slot_2.x + 110, self.y + 10, 100, 100, 5, screen, "image/empty.png", group)
        self.slot_4 = IngredientSlot(self.x + 10, self.y + 120, 100, 100, 5, screen, "image/empty.png", group)
        self.slot_5 = IngredientSlot(self.slot_4.x + 110, self.y + 120, 100, 100, 5, screen, "image/empty.png", group)
        self.slot_6 = IngredientSlot(self.slot_5.x + 110, self.y + 120, 100, 100, 5, screen, "image/empty.png", group)
        self.dish_slot = DishSlot(self.x + 450, self.y + 10, 150, 150, 5, screen, "image/empty.png", group)
        self.slots = [self.slot_1, self.slot_2, self.slot_3, self.slot_4, self.slot_5, self.slot_6]
        self.dishMakeBtn = RectButton(self.x + 450, self.y + 175, 40, 150, 3, screen, group, "Make", None,
                                      "image/make.png")
        self.dishClearBtn = RectButton(self.x + 450, self.dishMakeBtn.y + 45, 40, 150, 3, screen, group, "Dismiss",
                                       None, "image/dismiss.png")

    def get_slots(self):
        return self.slots

    def clear_all_slots(self):
        for dish_slot in self.get_slots():
            group = dish_slot.group
            x = dish_slot.x
            y = dish_slot.y
            weight = dish_slot.weight
            height = dish_slot.height
            width = dish_slot.width
            icon = "image/empty.png"
            dish_slot.icon = DishIcon(group, x + width, y + width, weight, height, width, icon, dish_slot)
            dish_slot.slot_is_empty = True
            print("DELETED")

    def get_ingredients(self):
        slot: IngredientSlot
        ingredients = []
        for slot in self.get_slots():
            if not slot.slot_is_empty:
                ingredients.append(slot.icon.ingredient_name)
        return ingredients

    def clear_dish_slot(self):
        group = self.dish_slot.group
        x = self.dish_slot.x
        y = self.dish_slot.y
        weight = self.dish_slot.weight
        width = self.dish_slot.width
        height = self.dish_slot.height
        icon = "image/empty.png"

        self.dish_slot.icon = DishIcon(group, x + width, y + width, weight, height, width, icon, self.dish_slot)
        return

    def click(self):
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        if self.dishMakeBtn.rect.collidepoint(mouse_x, mouse_y):
            self.make_dish()
        elif self.dishMakeBtn.text_surface.get_rect().collidepoint(mouse_x, mouse_y):
            self.make_dish()

        if self.dishClearBtn.rect.collidepoint(mouse_x, mouse_y):
            if self.level.get_dialog() is not None:
                self.customer_text.text = self.level.get_dialog()
            self.clear_dish_slot()
        elif self.dishMakeBtn.text_surface.get_rect().collidepoint(mouse_x, mouse_y):
            if self.level.get_dialog() is not None:
                self.customer_text.text = self.level.get_dialog()
            self.clear_dish_slot()

        if self.dish_slot.icon.rect.collidepoint(mouse_x, mouse_y):
            name = self.dish_slot.icon.ingredient_name
            dish_name = self.level.get_dish()
            print(name)
            print(dish_name)
            if name == dish_name:
                self.clear_dish_slot()
                self.customer_text.text = self.level.get_success_dialog()
                self.customer_window: CustomerWindow
                if self.level.get_character() is not None:
                    self.customer_window.customer.animation_list = self.level.get_character()

            else:
                if self.level.get_miss_dialog() is not None:
                    self.customer_text.text = self.level.get_miss_dialog()

    def make_dish(self):
        data = self.get_ingredients()
        for dish in FoodEngine.dishes:
            if dish.is_that_ingredients(data):
                print("FINED!")
                self.clear_all_slots()
                print(dish)

                group = self.dish_slot.group
                x = self.dish_slot.x
                y = self.dish_slot.y
                weight = self.dish_slot.weight
                height = self.dish_slot.height
                width = self.dish_slot.width
                icon = dish.image

                self.dish_slot.icon = DishIcon(group, x + width, y + width, weight, height, width, icon, self.dish_slot)
                break

    def draw(self):
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_COLOR, (self.x, self.y, self.weight, self.height), 0, 5)
        pygame.draw.rect(virtual_screen, WINDOW_STANDARD_BORDER_COLOR,
                         (self.x, self.y, self.weight + self.width, self.height + self.width), self.width, 5)
        slot: IngredientSlot
        for slot in self.slots:
            slot.draw()
        self.dish_slot.draw()
        self.dishMakeBtn.draw()
        self.dishClearBtn.draw()


def new_game():
    lvl_reached = 1
    lvl_1_score = 0
    lvl_2_score = 0
    lvl_3_score = 0
    text = f"lvl_reached={lvl_reached}\nlvl_1_score={lvl_1_score}\nlvl_2_score={lvl_2_score}\nlvl_3_score={lvl_3_score}"
    file = open("save.txt", "w")
    file.write(text)
    file.close()
    level_selection()
    return


def save_data():
    lvl_reached = 0
    lvl_1_score = 0
    lvl_2_score = 0
    lvl_3_score = 0
    try:
        file = open("save.txt", "r")
        lines = file.readlines()
        file.close()
        lvl_reached = lines[0].split("=")[-1].split("\n")[0]
        lvl_1_score = lines[1].split("=")[-1].split("\n")[0]
        lvl_2_score = lines[2].split("=")[-1].split("\n")[0]
        lvl_3_score = lines[3].split("=")[-1].split("\n")[0]
        print(lvl_reached)
        print(lvl_1_score)
        print(lvl_2_score)
        print(lvl_3_score)
        return lvl_reached, lvl_1_score, lvl_2_score, lvl_3_score

    except Exception as e:
        return 0, 0, 0, 0


def get_data():
    lvl_reached = 0
    lvl_1_score = 0
    lvl_2_score = 0
    lvl_3_score = 0
    try:
        file = open("save.txt", "r")
        lines = file.readlines()
        file.close()
        lvl_reached = lines[0].split("=")[-1].split("\n")[0]
        lvl_1_score = lines[1].split("=")[-1].split("\n")[0]
        lvl_2_score = lines[2].split("=")[-1].split("\n")[0]
        lvl_3_score = lines[3].split("=")[-1].split("\n")[0]
        print(lvl_reached)
        print(lvl_1_score)
        print(lvl_2_score)
        print(lvl_3_score)
        return True

    except Exception as e:
        return False


def load_game():
    if get_data():
        level_selection()
        return


def show_final_results():
    global run, current_size, virtual_screen, screen

    final_text = TextBox(0, 0, current_size[1], current_size[0], 5, virtual_screen)
    button_group = pygame.sprite.Group()
    back = RectButton(450, 600, 100, 300, 5, virtual_screen, button_group, "Back", None, "image/back.png")

    def click():
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        if back.rect.collidepoint(mouse_x, mouse_y):
            level_selection()
            return

    while run:
        virtual_screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                current_size = pygame.display.get_surface().get_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click()

        final_text.draw()
        back.draw()
        button_group.draw(virtual_screen)

        scaled_vurtual_screen = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scaled_vurtual_screen, (0, 0))

        clock.tick(FPS)
        pygame.display.flip()


def level_selection():
    global run, virtual_screen, current_size
    levels = []
    menu_group = pygame.sprite.Group()
    return_button = RectButton(500, 600, 100, 300, 5, virtual_screen, menu_group, "Back", None, "image/back.png")
    data = save_data()
    if data is not None:
        lvl_reached = int(data[0])
        print(f"level: {lvl_reached}")
        if lvl_reached == 1:
            lev_1_btn = RectButton(450, 50, 100, 400, 5, virtual_screen, menu_group, "Lvl1", None, "image/level1.png")
            levels = [lev_1_btn]
        elif lvl_reached == 2:
            lev_1_btn = RectButton(450, 50, 100, 400, 5, virtual_screen, menu_group, "Lvl1", None, "image/level1.png")
            lev_2_btn = RectButton(450, 160, 100, 400, 5, virtual_screen, menu_group, "Lvl2", None, "image/level2.png")
            levels = [lev_1_btn, lev_2_btn]
        elif lvl_reached == 3:
            lev_1_btn = RectButton(450, 50, 100, 400, 5, virtual_screen, menu_group, "Lvl1", None, "image/level1.png")
            lev_2_btn = RectButton(450, 160, 100, 400, 5, virtual_screen, menu_group, "Lvl2", None, "image/level2.png")
            lev_3_btn = RectButton(450, 270, 100, 400, 5, virtual_screen, menu_group, "Lvl3", None, "image/level3.png")
            levels = [lev_1_btn, lev_2_btn, lev_3_btn]
        elif lvl_reached == 4:
            lev_1_btn = RectButton(450, 50, 100, 400, 5, virtual_screen, menu_group, "Lvl1", None, "image/level1.png")
            lev_2_btn = RectButton(450, 160, 100, 400, 5, virtual_screen, menu_group, "Lvl2", None, "image/level2.png")
            lev_3_btn = RectButton(450, 270, 100, 400, 5, virtual_screen, menu_group, "Lvl3", None, "image/level3.png")
            lev_4_btn = RectButton(450, 380, 100, 400, 5, virtual_screen, menu_group, "Lvl3", None, "image/level4.png")
            levels = [lev_1_btn, lev_2_btn, lev_3_btn, lev_4_btn]

    def click():
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if return_button.rect.collidepoint(mouse_x, mouse_y):
            start_menu()
            return

        ld = LevelsData
        if lev_1_btn is not None and lev_1_btn.rect.collidepoint(mouse_x, mouse_y):
            print(f"test: {ld.level1.cur_dialog}")
            level_start(ld.level1)
            ld = None
            return
        elif lev_2_btn is not None and lev_2_btn.rect.collidepoint(mouse_x, mouse_y):
            level_start(ld.level2)
            ld = None
            return
        elif lev_3_btn is not None and lev_3_btn.rect.collidepoint(mouse_x, mouse_y):
            level_start(ld.level3)
            ld = None
            return
        elif lev_4_btn is not None and lev_4_btn.rect.collidepoint(mouse_x, mouse_y):
            show_final_results()
            ld = None
            return

    while run:
        virtual_screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                current_size = pygame.display.get_surface().get_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click()
        return_button.draw()
        button: RectButton
        for button in levels:
            button.draw()
        menu_group.draw(virtual_screen)

        scaled_vurtual_screen = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scaled_vurtual_screen, (0, 0))

        clock.tick(FPS)
        pygame.display.flip()


def start_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("music/background.mp3")
    pygame.mixer.music.play(-1, 0, 500)
    global run, virtual_screen, clock, current_size
    menu_group = pygame.sprite.Group()

    new_game_button = RectButton(500, 150, 100, 300, 5, virtual_screen, menu_group, "New Game", None,
                                 "image/new_game.png")
    load_button = RectButton(500, 260, 100, 300, 5, virtual_screen, menu_group, "Load", None, "image/load_game.png")
    settings_button = RectButton(500, 370, 100, 300, 5, virtual_screen, menu_group, "Settings", None,
                                 "image/settings.png")
    exit_button = RectButton(500, 550, 100, 300, 5, virtual_screen, menu_group, "Exit", None, "image/exit.png")

    def click():
        global run
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if new_game_button.rect.collidepoint(mouse_x, mouse_y):
            new_game()
            return
        if load_button.rect.collidepoint(mouse_x, mouse_y):
            load_game()
            return
        if exit_button.rect.collidepoint(mouse_x, mouse_y):
            run = False
            return

    while run:
        virtual_screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                current_size = pygame.display.get_surface().get_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click()
        new_game_button.draw()
        load_button.draw()
        settings_button.draw()
        exit_button.draw()
        menu_group.draw(virtual_screen)

        scaled_vurtual_screen = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scaled_vurtual_screen, (0, 0))

        clock.tick(FPS)
        pygame.display.flip()


def pressed(dish_window_slots, ingredients_window_slots):
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]
    ingredient_slot: IngredientSlot
    for ingredient_slot in ingredients_window_slots:
        is_empty = ingredient_slot.icon.empty
        if ingredient_slot.icon.rect.collidepoint(mouse_x, mouse_y) and not is_empty:
            new_ingredient_path = ingredient_slot.icon.ingredient_path

            dish_slot: IngredientSlot
            for dish_slot in dish_window_slots:
                if dish_slot.slot_is_empty:
                    group = dish_slot.group
                    x = dish_slot.x
                    y = dish_slot.y
                    weight = dish_slot.weight
                    width = dish_slot.width
                    height = dish_slot.height
                    icon = new_ingredient_path

                    dish_slot.icon = DishIcon(group, x + width, y + width, weight, height, width, icon, dish_slot)
                    dish_slot.slot_is_empty = False
                    break
                else:
                    print("ALL SLOTS RESERVED!")

    dish_slot: IngredientSlot
    for dish_slot in dish_window_slots:
        is_empty = dish_slot.slot_is_empty
        if not is_empty:
            if dish_slot.icon.rect.collidepoint(mouse_x, mouse_y):
                group = dish_slot.group
                x = dish_slot.x
                y = dish_slot.y
                weight = dish_slot.weight
                width = dish_slot.width
                height = dish_slot.height
                icon = "image/empty.png"
                dish_slot.icon = DishIcon(group, x + width, y + width, weight, height, width, icon, dish_slot)
                dish_slot.slot_is_empty = True
                print("DELETED")
                break


def level_completed(level: LevelsData.Level):
    lvl_reached, lvl_1_score, lvl_2_score, lvl_3_score = save_data()

    lvl_reached = int(lvl_reached) + 1
    if lvl_reached >= 5:
        lvl_reached = 4
    lvl_1_score = int(lvl_1_score)
    lvl_2_score = int(lvl_2_score)
    lvl_3_score = int(lvl_3_score)

    if level.levelName == "lev1":
        lvl_1_score = 5000
    if level.levelName == "lev2":
        lvl_2_score = 7500
    if level.levelName == "lev3":
        lvl_3_score = 10000

    text = f"lvl_reached={lvl_reached}\nlvl_1_score={lvl_1_score}\nlvl_2_score={lvl_2_score}\nlvl_3_score={lvl_3_score}"
    file = open("save.txt", "w")
    file.write(text)
    file.close()
    pygame.mixer.music.stop()
    level_selection()
    return


def show_recipes(group: pygame.sprite.Group, recipes):
    recipes.add(group)
    return


def hide_recipes(group: pygame.sprite.Group, recipes: ImageSprite):
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]

    if not recipes.rect.collidepoint(mouse_x, mouse_y):
        if len(group.spritedict) >= 1:
            group.remove(recipes)


def level_start(level):
    global run, current_size
    pygame.mixer.music.stop()

    if level.levelName == "lev1":
        pygame.mixer.music.load("music/level_1.mp3")
        pygame.mixer.music.play(-1, 0, 500)
    elif level.levelName == "lev2":
        pygame.mixer.music.load("music/level_2.mp3")
        pygame.mixer.music.play(-1, 0, 500)
    elif level.levelName == "lev3":
        pygame.mixer.music.load("music/level_3.mp3")
        pygame.mixer.music.play(-1, 0, 500)

    level: LevelsData.Level
    customer_group = pygame.sprite.Group()
    test_group = pygame.sprite.Group()
    dish_group = pygame.sprite.Group()
    upper_group = pygame.sprite.Group()

    cus_win = CustomerWindow(10, 10, 350, 350, 5, virtual_screen, customer_group, level)
    cus_tex = CustomerTextWindow(10, 380, 250, 350, 5, virtual_screen, customer_group, level, cus_win.customer)
    menu = RectButton(370, 10, 130, 150, 5, virtual_screen, test_group, "Menu", None, "image/menu.png")
    recipe_book = RectButton(370, 150, 130, 150, 5, virtual_screen, upper_group, "Recipes", None, "image/recipes.png")
    ingredients_window = IngredientsWindow(450, 400, 270, 800, 5, virtual_screen, test_group)
    dish_making_window = DishWindow(530, 10, 270, 725, 5, virtual_screen, dish_group, level, cus_tex, cus_win)

    recipes = ImageSprite(upper_group, 0, 0, 5, current_size[1] - 100, current_size[0] - 100, "image/recipe_list.png")

    def menu_buttons_click():
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if menu.rect.collidepoint(mouse_x, mouse_y):
            start_menu()
            return
        if recipe_book.rect.collidepoint(mouse_x, mouse_y):
            show_recipes(upper_group, recipes)
            return

    upper_group.remove(recipes)

    while run:
        virtual_screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                current_size = pygame.display.get_surface().get_size()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed(dish_making_window.slots, ingredients_window.slots)
                dish_making_window.click()
                cus_tex.click()
                menu_buttons_click()
                test_group.update()
                hide_recipes(upper_group, recipes)
        cus_win.draw()
        cus_tex.draw()
        menu.draw()
        recipe_book.draw()
        ingredients_window.draw()
        dish_making_window.draw()
        test_group.draw(virtual_screen)
        test_group.update()
        dish_group.draw(virtual_screen)
        dish_group.update()
        customer_group.draw(virtual_screen)
        customer_group.update()

        upper_group.draw(virtual_screen)

        scaled_vurtual_screen = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scaled_vurtual_screen, (0, 0))

        clock.tick(FPS)
        pygame.display.flip()


def title_screen():
    global run, current_size, virtual_screen, screen

    image_group = pygame.sprite.Group()
    final_text = ImageSprite(image_group, 0, 0, 5, current_size[1], current_size[0], "image/title_screen.png")

    while run:
        virtual_screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                current_size = pygame.display.get_surface().get_size()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_menu()
                    return

        image_group.draw(virtual_screen)

        scaled_vurtual_screen = pygame.transform.scale(virtual_screen, current_size)
        screen.blit(scaled_vurtual_screen, (0, 0))

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_icon(pygame.image.load("image/icon.png"))
    pygame.display.set_caption("SushiMaker")
    pygame.mixer.music.set_volume(0.2)
    size = w, h = 1280, 720
    user_display = pygame.display.Info()
    user_size = (user_display.current_w, user_display.current_h)
    screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    current_size = screen.get_size()
    virtual_screen = pygame.Surface((1280, 720))

    clock = pygame.time.Clock()
    run = True
    FPS = 30
    BACKGROUND_COLOR = (233, 185, 139)
    WINDOW_STANDARD_COLOR = (186, 164, 142)
    WINDOW_STANDARD_BORDER_COLOR = (0, 0, 0)

    title_screen()
