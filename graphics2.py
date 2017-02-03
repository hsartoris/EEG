from emokit.emotiv import Emotiv
import pygame

v = 'value'
q = 'quality'
locs=['X','Y','Z','F3','F4','P7','FC6','F7','F8','T7','P8','FC5','AF4','T8','O1','O2','AF3']
currX=0

BLACK = 0,0,0

valueMax = 0
valueMin = 0

qualityMax=0
qualityMin=0

valueRange=0
qualityRange=0

pygame.init()
#font = 
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("EEG Values")

values=[]
qualities=[]
#xInc = 2
#dataLen = width/2
dataList=[0]*width

for i in range(0,len(locs)):
	values.append(list(dataList))
	qualities.append(list(dataList))

def valueToHeight(input):
	global valueMin
	global valueRange
	if valueRange == 0:
		return height
	return (1.0 - (input - valueMin)/float(valueRange)) * height

def updateMaxMin(value, quality):
	global valueMax
	global valueMin
	global valueRange
	if value > valueMax:
		valueMax = value
	elif value < valueMin:
		valueMin = value
	#if quality > qualityMax:
	#	qualityMax = quality
	#elif quality > qualityMin:
	#	qualityMin = quality
	# mins should never be above 0 anyway
	valueRange = valueMax - valueMin
	#qualityRange = qualityMax - qualityMin

def updateVals(headset):
	packet = headset.dequeue()
	if packet is not None:
		for i in range(0, len(locs)):
			try:
				values[i][currX] = int(packet.sensors[locs[i]][v])
			except ValueError:
				print("Caught '?'")
			try:
				qualities[i][currX] = int(packet.sensors[locs[i]][q])
			except ValueError:
				print("Caught '?'")
			updateMaxMin(values[i][currX], qualities[i][currX])
	elif currX > 0:
		for i in range(0, len(locs)):
			values[i][currX] = values[i][currX - 1]
			qualities[i][currX]  = qualities[i][currX - 1]
			updateMaxMin(values[i][currX], qualities[i][currX])
	else:
		for i in range(0, len(locs)):
			values[i][currX] = values[i][len(values[i]) - 1]
			qualities[i][currX] = qualities[i][len(qualities[i]) - 1]
			updateMaxMin(values[i][currX], qualities[i][currX])


clk = pygame.time.Clock()
with Emotiv() as headset:
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		screen.fill((255,255,255))
		if currX < width - 1:
			currX = currX + 1
		else:
			currX = 0
		updateVals(headset)
		for x in range(1,currX):
			# gonna assume min value is 0
			for i in range(0, len(locs)):
				### NEEDS REJIGGERING
				pygame.draw.line(screen, BLACK, (x-1, valueToHeight(values[i][x-1])), (x, valueToHeight(values[i][x])))
				#pygame.draw.line(screen, BLACK, (x-1, height / 2), (x, height / 2))
		for x in range(currX + 2, len(values[0])):
			for i in range(0, len(locs)):
				pygame.draw.line(screen, BLACK, (x-1, valueToHeight(values[i][x-1])), (x, valueToHeight(values[i][x])))
		pygame.display.flip()
#		print(values)
#		raw_input()
		clk.tick(60)
pygame.quit()
