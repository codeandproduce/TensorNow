from TensorNow import Now
import threading, time
import numpy as np

WAIT_TIME_SECONDS = 1

ticker = threading.Event()

now = Now('test', 
'0LCgAknBzrC3MQ2lFUN3M3xshjsgFe',
'Keras')

now.log_permission = True


now.clear_all_custom_flags();


CONVERGENCE_FLAG = now.create_custom_flag('My personal definition of model convergence.')
GRADIENT_VANISHING_FLAG = now.create_custom_flag("Gradient Vanishing")


def get_loss_val(count):
	while not ticker.wait(WAIT_TIME_SECONDS):
		calc = np.exp(-1 * (count/100))
		return calc


def train():
	now.start_training('Big boy test')
	for i in range(0,1000000):
		if(i==10):
			now.flag(CONVERGENCE_FLAG)
		if(i==20):
			now.flag(GRADIENT_VANISHING_FLAG)

		loss_val = get_loss_val(i)**2
		now.log_loss(loss_val)

train()


