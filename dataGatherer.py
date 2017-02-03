import sys
from emokit.emotiv import Emotiv

v = 'value'
q = 'quality'
locs=['X','Y','Z','F3','F4','P7','FC6','F7','F8','T7','P8','FC5','AF4','T8','O1','O2','AF3']
highVals=[0]*len(locs)
lowVals=[0]*len(locs)
highQuals=[0]*len(locs)
lowQuals=[0]*len(locs)

with Emotiv() as headset:
	while True:
		packet = headset.dequeue()
		if packet is not None:
			printString = ''
			for x in range(0, len(locs)):
				printString = printString + locs[x] + ': ' + str(packet.sensors[locs[x]][v]) + ',' + str(packet.sensors[locs[x]][q])
			print printString
#		print('\n')
#	while packet is None:
#		packet = headset.dequeue()
#	for x in range(0,len(locs)):
#		highVals[x] = packet.sensors[locs[x]][v]
#		lowVals[x] = highVals[x]
#		highQuals[x] = packet.sensors[locs[x]][q]
#		lowQuals[x] = highQuals[x]


#for x in range(0,len(locs)):
#	print(locs[x] + ': ' + 
