from emokit.emotiv import Emotiv

if __name__ == "__main__":
	with Emotiv() as headset:
		while True:
			packet = headset.dequeue()
			if packet is not None:
print("Gyro - X:{x_position} Y:{y_position}".format(x_position=packet.sensors['X']['value'],y_position=packet.sensors['Y']['value']))



