import numpy as np
import requests
import time


requests.packages.urllib3.disable_warnings()


# from notify_error import notify_error


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_ENDPOINT_PROD = 'https://tensornow.com'
API_ENDPOINT = 'http://localhost:8000'


class Now:
	def __init__(self,username, API_KEY, framework):
		# permissions
		self.log_permission = True
		self.userData = init_user_check(username)

		self.premium = self.userData['premium']
		self.exists = self.userData['exists']

		print(self.userData)

		if not self.exists:
			raise Exception('User does not exist.')

		self.IP = API_ENDPOINT
		self.interval = 3 # upload every 40 seconds?
		self.avg_time_per_loss = 0
		self.number_iter = 0 # how many loss iterations have we gone?
		self.iteration_start_time = 0

		self.training = False
		self.framework = framework
		self.username = username
		self.API_KEY = API_KEY
		if framework == 'Keras':
			self.model = KerasModel(username, API_KEY)
		elif framework == 'SKLearn':
			self.model = SKLearnModel()
		else:
			self.model = GenericModel()

		self.logger = {}

	def start_training(self, model_title):
		self.training = True
		self.model_title = model_title
		self.process_ID = register_project(self.username, model_title, self.API_KEY)
		self.project_full_id = self.model_title + "-" + str(self.process_ID);
		self.logger = {
			'pushed_losses': [],
			'queued_losses': []
		}		

		self.starting_time = time.time()
		self.iteration_start_time = time.time()
		
	def log_loss(self, loss_raw):
		self.ending_time = time.time()
		self.number_iter = self.number_iter+1

		time_elapsed = self.ending_time-self.starting_time
		self.avg_time_per_loss = (self.avg_time_per_loss*self.number_iter + time_elapsed)/(self.number_iter+1)

		if not self.training:
			print("Haven't started a process yet.")
			print("Make sure you've flagged the following in the beginning: ")
			print("now.start_training({project_title});")
		else:
			if not len(self.logger['queued_losses']) > 2000:
				
				self.logger['queued_losses'].append(loss_raw)
			

				current_time = time.time()
				if (current_time-self.iteration_start_time)>self.interval:
					# if it's been 40 seconds since the last iteration:
					url = API_ENDPOINT + '/api/user/project/log-loss'
					payload = {
						'username': self.username,
						'project_ID': self.process_ID,
						'api_key': self.API_KEY,
						'loss_val_arr': self.logger['queued_losses']
					}
					response = requests.post(url, data=payload, verify=False)
					if not response.json()['success']:
						print("TENSORNOW: Uploading loss values failed!")
					else:
						if self.log_permission:
							print("TENSORNOW: Loss Values Uploaded.")
						
						self.logger['pushed_losses'] += self.logger['queued_losses']
						self.logger['queued_losses'] = []
						self.iteration_start_time = time.time()
				
			
			
			else:
				print("You are calling loss_log too many times. ")
				print("TensorNow will no longer upload your loss values.")
				notify_error(1, self.username, self.process_ID, self.API_KEY)


			# self.model.format_loss(self.project_full_id, loss_tensor)
		self.starting_time = time.time()
	def return_loss_log(project_full_id):
		return self.logger.pushed_losses


def init_user_check(username):
	url = API_ENDPOINT+'/api/auth/init-user-check'
	payload = {
		'username': username
	}
	data = requests.post(url, data=payload, verify=False)

	returnLoad = {
		'premium': data.json()['premium'],
		'exists': data.json()['exists']
	}
	return returnLoad

def register_project(username, model_title, API_KEY):
	# insert http post request\
	url = API_ENDPOINT+'/api/user/project/create'
	
	payload = {
		'username': username, 
		'projectName': model_title,
		'api_key': API_KEY
	}

	project = requests.post(url, data=payload, verify=False)
	project_ID = project.json()['projectID']
	return project_ID

def temp_address_generator():
	'''
		replace this with a real request to the server asking
		for a unique ID
	'''
	return np.random.randint(low=1, high=100, size=1)[0]


class KerasModel:
	def __init__(self, username, API_KEY):
		self.model = 'keras'
		self.username = username
		self.API_KEY = API_KEY

	def log_loss(self, processID, loss_tensor):
		print("@"+self.username+' of API'+self.API_KEY+' for process '+str(processID)+' log loss: '+str(loss_tensor))

class GenericModel:
	def __init__(self):
			self.model = 'generic'


class SKLearnModel:
	def __init__(self):
		self.model = 'sklearn'




def notify_error(error_code, username, model_ID, API_KEY):

    url = API_ENDPOINT+'/api/user/project/error'
	
    payload = {
	    'username': username, 
		'projectID': model_ID,
		'api_key': API_KEY,
		'error_code': error_code
    }

    request.post(url, data=payload)
	

def notify_custom_error(username, model_ID, API_KEY, message):

    url = API_ENDPOINT+'/api/user/project/custom-error'
	
    payload = {
	    'username': username, 
		'projectID': model_ID,
		'api_key': API_KEY,
		'message': message
    }

    request.post(url, data=payload)
	
