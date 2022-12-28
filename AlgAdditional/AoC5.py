import curses
from curses import wrapper
import time

t = 0.1

#починаємо парсинг
with open('AoC5.txt') as file:
    stack_strings, instructions = (i.splitlines() for i in file.read().strip('\n').split('\n\n'))

stacks = {int(digit):[] for digit in stack_strings[-1].replace(" ","")}
indexes = [index for index, char in enumerate(stack_strings[-1]) if char != " "]


def loadStacks():
    for string in stack_strings[:-1]:
        stack_num = 1
        for index in indexes:
            if string[index] == " ":
                pass
            else:
                stacks[stack_num].insert(0, string[index])
            stack_num += 1

#закінчили парсинг
loadStacks()

#функція для знаходження найвищої купки(щоб підлаштовувати розмір крану)
def maxLen(stacks):
	return max([len(stacks[stack]) for stack in stacks])


#ф-ія для початкового малюнку(кран і контейнери)
def draw(stdscr):
	j = 1

	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	YELLOW = curses.color_pair(1)
	RED = curses.color_pair(2)
	MAGENTA = curses.color_pair(3)

	stdscr.clear()

	#додаємо номери купок
	for i in range(2, 36, 4):
		stdscr.addstr(28, i, str((i+2)//4), curses.A_BOLD)

	#додаємо самі контейнера
	for stack in stacks:
		if len(stacks[stack]) == 0:
			stdscr.addstr(29, j, "[/]", MAGENTA)

		for i in range(len(stacks[stack])):
			stdscr.addstr(27-i, j, "[" + stacks[stack][i] + "]")
			if(i+1 == len(stacks[stack])):
				stdscr.addstr(27-i, j, "[" + stacks[stack][i] + "]", RED)
				stdscr.addstr(29, j, "[" + stacks[stack][i] + "]", MAGENTA)
		j += 4

	#малюємо кран
	stdscr.addstr(28, 46, "_/=[||]=\_", YELLOW)
	stdscr.addstr(23 - maxLen(stacks), 34, "/================\==-_", YELLOW)
	stdscr.addstr(24 - maxLen(stacks), 34, "A", YELLOW)
	stdscr.addstr(25 - maxLen(stacks), 34, "[]", YELLOW)

	for i in range(maxLen(stacks) + 4):
		stdscr.addstr(27-i, 50, "||", YELLOW)

	stdscr.refresh()


#ф-ія для руху крана по горизонталі
def moveHor(stdscr, curCrate, destCrate, crateNum):
	letter = stacks[crateNum][-1] if crateNum != 0 else " "

	destCratePos = 1 if destCrate > curCrate else 0 #якщо кран рухається вправо, в кінці вирівнюємося з купкою
	position = curCrate*4-2
	direction = 1 if curCrate > destCrate else -1 #напрям руху
	back = 1 if direction != 1 else 0 #забирається лишній рух крану коли він рухається вправу
	k = 0
	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	YELLOW = curses.color_pair(1)

	#сам рух крану
	for i in range(curCrate*4-2, destCrate*4-2 + destCratePos, -1*direction):
		stdscr.addstr(23 - maxLen(stacks), position-k+back, "=", YELLOW)
		stdscr.addstr(23 - maxLen(stacks), position-2-k+back, " /", YELLOW)
		stdscr.addstr(24 - maxLen(stacks), position-2-k+back, " A ", YELLOW)
		stdscr.addstr(25 - maxLen(stacks), position-3-k+back, " [" + letter + "] ", YELLOW)
		time.sleep(t)
		k += 1*direction
		stdscr.refresh()

	stdscr.refresh()


#ф-ія для підняття(опущення) крану в залежності від максимальної висоти всіх купок
def moveVert(stdscr, crateNum):
	position = crateNum*4-2

	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	YELLOW = curses.color_pair(1)

	stdscr.addstr(23 - maxLen(stacks), 51, "\==-_", YELLOW)

	#малювання крану в новому рядку
	for i in range(51 - position):
		stdscr.addstr(23 - maxLen(stacks), position+i, "=", YELLOW)

	stdscr.addstr(23 - maxLen(stacks), position, "/", YELLOW)

	for i in range(position):
		stdscr.addstr(23 - maxLen(stacks), i, " ")

	#тут відбуватимуться стирання попередніх рядків(коли кран змінив положення)
	for i in range(maxLen(stacks) + 4):
		stdscr.addstr(27-i, 50, "||", YELLOW)

	for i in range(50):
		stdscr.addstr(23 - maxLen(stacks) + 1, i, " ")
		stdscr.addstr(23 - maxLen(stacks) - 1, i, " ")
		stdscr.addstr(23 - maxLen(stacks) + 2, i, " ")
		stdscr.addstr(23 - maxLen(stacks) + 3, i, " ")

	for i in range(10):
		stdscr.addstr(23 - maxLen(stacks) + 1, 52 + i, " ")
		stdscr.addstr(23 - maxLen(stacks) - 1, 49 + i, " ")
	#тут закінчилося стирання

	stdscr.refresh()


#ф-ія для підняття контейнеру
def pickCrate(stdscr, crateNum):
	position = crateNum*4-2
	distance = 3 + maxLen(stacks) - len(stacks[crateNum]) #відстань на яку крюк опискатиметься

	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	YELLOW = curses.color_pair(1)
	RED = curses.color_pair(2)
	MAGENTA = curses.color_pair(3)

	#опускання крюку
	for i in range(distance):
		stdscr.addstr(24 - maxLen(stacks) + i, position-1, " | ", YELLOW)
		stdscr.addstr(25 - maxLen(stacks) + i, position-1, " A ", YELLOW)
		stdscr.addstr(26 - maxLen(stacks) + i, position-1, "[ ] ", YELLOW)
		time.sleep(t)
		stdscr.refresh()

	#крюк бере контейнер, змінюються кольори контейнерів, та назва контейнеру внизу під цифрою(так як один з них забрали)
	stdscr.addstr(26 - maxLen(stacks) + i, position-1, "[" + stacks[crateNum][-1] + "]", YELLOW)
	stdscr.refresh()
	if len(stacks[crateNum]) > 1:
		stdscr.addstr(27 - maxLen(stacks) + i, position-1, "[" + stacks[crateNum][-2] + "]", RED)
		stdscr.refresh()
		stdscr.addstr(29, position-1, "[" + stacks[crateNum][-2] + "]", MAGENTA)
		stdscr.refresh()

	#якщо це був останній контейнер, то назви під цифрою не буде
	else:
		stdscr.addstr(27 - maxLen(stacks) + i, position-1, "   ", RED)
		stdscr.refresh()
		stdscr.addstr(29, position-1, "[/]", MAGENTA)
		stdscr.refresh()

	#підняття контейнеру
	for i in range(distance - 1):
		stdscr.addstr(24 - maxLen(stacks) + distance - 2 - i, position-1, " | ", YELLOW)
		stdscr.addstr(25 - maxLen(stacks) + distance - 2 - i, position-1, " A ", YELLOW)
		stdscr.addstr(26 - maxLen(stacks) + distance - 2 - i, position-1, "[" + stacks[crateNum][-1] + "] ", YELLOW)
		stdscr.addstr(27 - maxLen(stacks) + distance - 2 - i, position-1, "   ")

		#підстраховка, якщо цифра зітреться
		stdscr.addstr(28, position, str(crateNum), curses.A_BOLD)
		time.sleep(t)
		stdscr.refresh()

	#встановлення крюку з контейнером на кінцевій позиції
	stdscr.addstr(24 - maxLen(stacks), position-1, " A ", YELLOW)
	stdscr.addstr(25 - maxLen(stacks), position-1, "[" + stacks[crateNum][-1] + "] ", YELLOW)
	stdscr.addstr(26 - maxLen(stacks), position-1, "   ")
	time.sleep(t)
	stdscr.refresh()


#ф-ія для того щоб поставити контейнер на інші контейнера
def putCrate(stdscr, crateNum, prevCrateNum):
	position = crateNum*4-2
	distance = 3 + maxLen(stacks) - len(stacks[crateNum])

	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
	YELLOW = curses.color_pair(1)
	RED = curses.color_pair(2)
	MAGENTA = curses.color_pair(3)
	WHITE = curses.color_pair(4)

	#опускаємо крюк з контейнером
	for i in range(distance-1):
		stdscr.addstr(24 - maxLen(stacks) + i, position-1, " | ", YELLOW)
		stdscr.addstr(25 - maxLen(stacks) + i, position-1, " A ", YELLOW)
		stdscr.addstr(26 - maxLen(stacks) + i, position-1, "[" + stacks[prevCrateNum][-1] + "]", YELLOW)
		time.sleep(t)
		stdscr.refresh()

	#поставивши контейнер, міняємо кольори і назву контейнера під цифрою(так як з'явився новий контейнер)
	stdscr.addstr(24 - maxLen(stacks) + i, position-1, " A ", YELLOW)
	stdscr.addstr(25 - maxLen(stacks) + i, position-1, "[ ]", YELLOW)
	stdscr.refresh()
	stdscr.addstr(26 - maxLen(stacks) + i, position-1, "[" + stacks[prevCrateNum][-1] + "]", RED)
	if len(stacks[crateNum]) > 0:
		stdscr.addstr(27 - maxLen(stacks) + i, position-1, "[" + stacks[crateNum][-1] + "]", WHITE)
		stdscr.refresh()
	stdscr.addstr(29, position-1, "[" + stacks[prevCrateNum][-1] + "]", MAGENTA)
	stdscr.refresh()

	#підіймаємо крюк вже без контейнера
	for i in range(distance - 3):
		stdscr.addstr(24 - maxLen(stacks) + distance - 4 - i, position-1, " | ", YELLOW)
		stdscr.addstr(25 - maxLen(stacks) + distance - 4 - i, position-1, " A ", YELLOW)
		stdscr.addstr(26 - maxLen(stacks) + distance - 4 - i, position-1, "[ ]", YELLOW)
		stdscr.addstr(27 - maxLen(stacks) + distance - 4 - i, position-1, "   ")

		stdscr.addstr(28, position, str(crateNum), curses.A_BOLD)
		time.sleep(t)
		stdscr.refresh()

	#встановлення крюку без контейнера на кінцевій позиції
	stdscr.addstr(24 - maxLen(stacks), position-1, " A ", YELLOW)
	stdscr.addstr(25 - maxLen(stacks), position-1, "[ ]", YELLOW)
	stdscr.addstr(26 - maxLen(stacks), position-1, "   ")
	time.sleep(t)
	stdscr.refresh()


#основна ф-ія для візуалізації програми
def moveCrane(stdscr):
	prev_crate = 9 #в цій змінній зберігатимемо останю купку яка зазначена в n інструкції, щоб в наступній інструкції можна було від цієї купки рухатись

	#розпаковка інструкцій і їх виконання
	for instruction in instructions:
		instruction = instruction.replace("move", "").replace("from ", "").replace("to ", "").strip().split(" ")
		instruction = [int(i) for i in instruction]

		crates = instruction[0]
		from_stack = instruction[1]
		to_stack = instruction[2]

		moveHor(stdscr, prev_crate, from_stack, 0)

		for i in range(crates):
			pickCrate(stdscr, from_stack)
			moveHor(stdscr, from_stack, to_stack, from_stack)
			putCrate(stdscr, to_stack, from_stack)
			moveHor(stdscr, to_stack, from_stack, 0)

			crate_removed = stacks[from_stack].pop()
			stacks[to_stack].append(crate_removed)
			moveVert(stdscr, from_stack)
			prev_crate = from_stack


def main(stdscr):
	draw(stdscr)
	moveCrane(stdscr)

	stdscr.getch()

wrapper(main)