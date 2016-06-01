from scipy.io.wavfile import read
from random import randint
from numpy import fft
import pygame, sys, time


def main():
	
	#graphic interface dimensions
	width, height = 420, 360
	center = [width/2, height/2]
	
	#read amplitude and frequency of music file with defined frame skips
	file_name = sys.argv[1]
	frame_rate, amplitude = read(file_name)
	frame_skip = 96
	amplitude = amplitude[:,0] + amplitude[:,1]
	amplitude = amplitude[::frame_skip]
	frequency = list(abs(fft.fft(amplitude)))
	
	#scale the amplitude to 1/4th of the frame height and translate it to height/2(central line)
	max_amplitude = max(amplitude)
	for i in range(len(amplitude)):
		amplitude[i] = float(amplitude[i])/max_amplitude*height/4 + height/2
	amplitude = [int(height/2)]*width + list(amplitude)

	#initiate graphic interface and play audio piece
	pygame.init()
	screen=pygame.display.set_mode([width, height])
	pygame.mixer.music.load(file_name)
	pygame.mixer.music.play()
	now = time.time()	
	
	#visualizer animation starts here
	for i in range(len(amplitude[width:])):
		
		screen.fill([0, 0, 0])
		
		#circular animation: radius of circle depends on magnitude amplitude and color of circle depends on frequency
		try:
			pygame.draw.circle(screen, [(frequency[i]*2)%255, (frequency[i]*3)%255, (frequency[i]*5)%255], center, amplitude[i], 1)
		except ValueError:
			pass
			
		#the amplitude graph is being translated from both left and right creating a mirror effect
		prev_x, prev_y = 0, amplitude[i]
		for x, y in enumerate(amplitude[i+1:i+1+width][::5]):
			pygame.draw.line(screen, [0, 255, 0], [prev_x*5, prev_y], [x*5, y], 1)
			pygame.draw.line(screen, [0, 255, 0], [(prev_x*5-width/2)*-1+width/2, prev_y], [(x*5-width/2)*-1+width/2, y], 1)
			prev_x,	prev_y = x, y
		
		#time delay to control frame refresh rate
		while time.time()<now+ 1.0000000000/frame_rate*frame_skip:
			time.sleep(.00000000001)
		now = time.time()
		
		pygame.display.flip()


if __name__ == '__main__':
	main()
