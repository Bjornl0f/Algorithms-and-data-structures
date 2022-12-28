import pygame
import random
import math
from heapq import heappush, heappop
import time
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f"{__name__}.log", mode = "w")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")

t = 0.01

pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOUR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 20)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Introsort algorithm visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, ascending=True):
	draw_info.window.fill(draw_info.BACKGROUND_COLOUR)

	title = draw_info.LARGE_FONT.render(f"{'Ascending sorting' if ascending else 'Descending sorting'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2 , 5))
	
	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - ascending | D - descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, colour_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOUR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		colour = draw_info.GRADIENTS[i % 3]

		if i in colour_positions:
			colour = colour_positions[i] 

		pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for i in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def heapsort(draw_info, ascending=True):
	logger.info("Function heapsort started its work")
	lst = draw_info.lst

	h = []
 
	for value in lst:
		heappush(h, value)
	lst = []

	lst = lst + [heappop(h) for i in range(len(h))]
	draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
	time.sleep(t)
	logger.info("Function heapsort ended its work")


def InsertionSort(draw_info, ascending, begin, end):
	lst = draw_info.lst

	left = begin
	right = end

	for i in range(left + 1, right + 1):
		current = lst[i]
		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			time.sleep(t)


def Partition(draw_info, ascending, low, high):
	lst = draw_info.lst

	pivot = lst[high]

	i = low - 1

	for j in range(low, high):
		if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
			i = i + 1
			(lst[i], lst[j]) = (lst[j], lst[i])
			draw_list(draw_info, {j: draw_info.GREEN, i: draw_info.RED}, True)
			time.sleep(t)

	(lst[i + 1], lst[high]) = (lst[high], lst[i + 1])
	draw_list(draw_info, {i+1: draw_info.GREEN, high: draw_info.RED}, True)
	time.sleep(t)

	return i + 1


def MedianOfThree(draw_info, a, b, d):
	lst = draw_info.lst

	A = lst[a]
	B = lst[b]
	C = lst[d]

	if A <= B and B <= C:
		return b
	if C <= B and B <= A:
		return b
	if B <= A and A <= C:
		return a
	if C <= A and A <= B:
		return a
	if B <= C and C <= A:
		return d
	if A <= C and C <= B:
		return d


def IntrosortUtil(draw_info, ascending, begin, end, depthLimit):
	lst = draw_info.lst

	size = end - begin
	if size < 16:
		InsertionSort(draw_info, ascending, begin, end)
		return

	if depthLimit == 0:
		heapsort(draw_info, ascending)
		return

	pivot = MedianOfThree(draw_info, begin, begin + size // 2, end)
	(lst[pivot], lst[end]) = (lst[end], lst[pivot])
	draw_list(draw_info, {pivot: draw_info.GREEN, end: draw_info.RED}, True)
	time.sleep(t)


	partitionPoint = Partition(draw_info, ascending, begin, end)

	IntrosortUtil(draw_info, ascending, begin, partitionPoint - 1, depthLimit - 1)
	IntrosortUtil(draw_info, ascending, partitionPoint + 1, end, depthLimit - 1)

 
def Introsort(draw_info, ascending, begin, end):
	logger.info("Function Introsort started its work")
	lst = draw_info.lst

	depthLimit = 2 * math.floor(math.log2(end - begin))
	IntrosortUtil(draw_info, ascending, begin, end, depthLimit)
	logger.info("Function Introsort ended its work")
	check(draw_info, ascending)


def check(draw_info, ascending):
	lst = draw_info.lst

	for i in range(len(lst)-2):
		if (lst[i] <= lst[i+1] and ascending) or (lst[i] >= lst[i+1] and not ascending):
			pass
		else:
			logger.info("The array was sorted incorectly")
			break


def main():
	run = True
	clock = pygame.time.Clock()

	n = 75
	min_val = 10
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = Introsort

	while run:
		clock.tick(60)

		if sorting:
			pass
		else:
			draw(draw_info, ascending)

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
				sorting_algorithm(draw_info, ascending, 0, len(lst) - 1)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False

	pygame.quit()


if __name__ == "__main__":
	main()