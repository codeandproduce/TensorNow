from tensornow import Now
import threading, time
import numpy as np

WAIT_TIME_SECONDS = 1

ticker = threading.Event()

now = Now('cwkeam', 
'DB8lSe8ZmEMapXXlZpbEPJQcW40vG6')

now.log_permission = True
# now.clear_all_custom_flags()
# now.clear_all_projects()


CONVERGENCE_FLAG = now.create_custom_flag('My personal definition of model convergence.')
GRADIENT_VANISHING_FLAG = now.create_custom_flag("Gradient Vanishing")


def get_loss_val(count):
	while not ticker.wait(WAIT_TIME_SECONDS):
		calc = np.exp(-1 * (count/100))
		return calc


def train():
	now.start_training('RNN depth=20')
	for i in range(0,1000000):
		if(i==100):
			now.flag(CONVERGENCE_FLAG)
		if(i==200):
			now.flag(GRADIENT_VANISHING_FLAG)

		loss_val = get_loss_val(i)**2
		now.log_loss(loss_val)

train()


