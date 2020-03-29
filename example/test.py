from TensorNow import Now
import threading, time
import numpy as np

WAIT_TIME_SECONDS = 1

ticker = threading.Event()

thisNow = Now('cwkeam', 
'UrgiZEfdQ3EfLgZRhrGqkZXCswS2JJ',
'Keras')



def get_loss_val(count):
	while not ticker.wait(WAIT_TIME_SECONDS):
		calc = np.exp(-1 * (count/100))
		return calc


def train():
	thisNow.start_training('ConvNet r=1e5')
	for i in range(0,1000000):
		loss_val = get_loss_val(i)**2
		thisNow.log_loss(loss_val)

train()


