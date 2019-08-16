#!/usr/bin/env python
import os
directory = os.path.dirname(os.path.realpath(__file__))

from precise_runner import PreciseEngine
from precise import PreciseRunner

import rospy
from std_msgs.msg import Empty

def play_audio(filename: str):
    """
    Args:
        filename: Audio filename
    """
    import platform
    from subprocess import Popen

    player = 'play' if platform.system() == 'Darwin' else 'aplay'
    Popen([player, '-q', filename])


def activate_notify():
    audio = directory+'/resources/activate.wav'
    #audio = abspath(dirname(abspath(__file__)) + '/../' + audio)

    play_audio(audio)

class WakeWord():
	def __init__(self):
		print('Starting... ')
		engine = PreciseEngine(directory+'/resources/precise-engine', directory+'/resources/zordon.pb')
		self.runner = PreciseRunner(engine, on_activation=self.hotword_detected)
		self.pub = rospy.Publisher('roboga/wake_word/result', Empty, queue_size=10)
		rospy.Subscriber('roboga/wake_word/activate', Empty, callback=self.activate)
		rospy.init_node('wake_word', anonymous=True)
		self.active = False

	def activate(self, data):
		self.active = True

	def run(self):
		print("starting wakeword listener...")
		self.runner.start()		

	def hotword_detected(self):
		if(self.active):
			activate_notify()
			msg = Empty()
			self.pub.publish(msg)
			self.active = False
			print("hotword detected")

if __name__ == "__main__":
	wakeword = WakeWord()
	wakeword.run()
	import time
	#while(True):
	#	time.sleep(5) 
	#	chatbot.run()