from TensorNow import Now
import threading, time
import numpy as np

WAIT_TIME_SECONDS = 1

ticker = threading.Event()

thisNow = Now('ff', 
'0vskTyyeadkkRhwNErxgkgaG09CtnA',
'Keras')

thisNow.log_permission = False



def get_loss_val(count):
	while not ticker.wait(WAIT_TIME_SECONDS):
		calc = np.exp(-1 * (count/100))
		return calc


def train():
	thisNow.start_training('RNN a=1e4')
	for i in range(0,1000000):
		loss_val = get_loss_val(i)**2
		thisNow.log_loss(loss_val)

train()


