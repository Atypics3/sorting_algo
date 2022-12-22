import pygame
import random
import math
pygame.init()


class DrawInformation:
    # COLORS
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    # gradients of gray and its shades
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # default font style
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    # 50 pixels (100 total) from left to right on each side
    SIDE_PAD = 100

    # 75 pixels from top to bottom on each side
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    # setting initial values for the list
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # calculates the width of each block
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))

        # calculates the height of each block
        self.block_height = int(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        # gets the starting x-coord.
        self.start_x = self.SIDE_PAD // 2


# fills the window with given information
def draw(draw_info, algo_name, ascending):
    # default color: white
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # rendering title text
    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    # puts text in the upper-middle part of the screen
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    # rendering controls text
    controls = draw_info.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(
        controls, (draw_info.width/2 - controls.get_width()/2, 45))

    # rendering sorting text
    sorting = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(
        sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()

# draws a starting list with given values


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,
                         draw_info.BACKGROUND_COLOR, clear_rect)

    # need to know where to draw the first block
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width

        # gets y based on the height of the screen - min value to get
        # the value that is always larger than the min value
        y = draw_info.height - (val - draw_info.min_val) * \
            draw_info.block_height

        # colors of the blocks
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color,
                         (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

# generates a starting list with default values


def generate_starting_list(n, min_val, max_val):
    lst = []

    # iterates until n is reached
    for _ in range(n):
        # gets number in the range of min value and max value
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

# bubble sort algo.


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN,
                          j + 1: draw_info.RED}, True)
                # generator object -> gets each value and passes it until the function stops running
                yield True

    return lst

# insertion sort algo.


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN,
                      i: draw_info.RED}, True)
            yield True

    return lst

# more algos. go here


def main():
    run = True
    clock = pygame.time.Clock()

    # default values for algo.
    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    # width, height, lst
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        # clock goes for 60 seconds (or 1 minute)
        clock.tick(60)

        # keeps going until sorting ends
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True

                # generator method
                sorting_algorithm_generator = sorting_algorithm(
                    draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
