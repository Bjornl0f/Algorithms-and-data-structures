from random import randint
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f"{__name__}.log", mode = "w")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")


class HashTable:
	def __init__(self, size):
		self.SIZE = size
		self.arr = [None for i in range(self.SIZE)]
		self.collisionCount = 0

	def hashFunc(self, key):
		return (2003 - len(key)) % self.SIZE

	def insertElement(self, key):
		logger.info("Inserting an element into table...")
		index = self.hashFunc(key)
		while self.arr[index] != None:
			index += 1
			index %= self.SIZE
			logger.info("Collision happened!")
			self.collisionCount += 1
		self.arr[index] = key

	def findElement(self, key):
		index = hashFunc(key)
		while self.arr[index] != key:
			index += 1
			index %= self.SIZE
		return index

	def deleteItem(self, key):
		index = hashFunc(key)
		while self.arr[index] != key:
			index += 1
			index %= self.SIZE
		self.arr[index] = None

	def printItems(self):
		print("Hash Table: ")
		for item in self.arr:
			print("\t", item)


def main():
	some_list = ('monkey', 'elephant', 'tiger', 'leopard', 'horse', 'dog', 'cat', 'donkey', 'turtle', 'parrot', 'bear', 'mouse', 'rat', 'wolf', 'lion',
               'capybara', 'beaver', 'racoon', 'snake', 'hepard', 'pig', 'cow', 'straus', 'penquin', 'chicken', 'calf', 'spider', 'hornet', 'bee', 'ant', 
               'snail', 'chimpanze', 'orangutan', 'zebra', 'pelican', 'sparrow', 'herring', 'moose', 'gorilla', 'hippo', 'rhino', 'giraffe', 'camel', 
               'goose', 'goat', 'duck', 'turkey', 'lizard', 'koala', 'sloth', 'kangaroo', 'platypus', 'bull', 'fox', 'sheep', 'lama', 'panda', 'seagul', 'moth')

	newTable = HashTable(12)
	for i in range(newTable.SIZE - 1):
		item = some_list[randint(0, len(some_list) - 1)]
		newTable.insertElement(item)

	newTable.printItems()
	print("\nAmount of collisions = ", newTable.collisionCount)
	logger.info("The end of the testing")


if __name__ == "__main__":
	main()