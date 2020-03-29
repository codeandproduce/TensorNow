.. TensorNow documentation master file, created by
   sphinx-quickstart on Mon Mar 30 00:42:48 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TensorNow
=====================================
A lightweight model progress monitoring solution for independent A.I. developers.

Current version is 1.0.0.


****************
Big Picture Idea
****************
1. Configure TensorNow into your code.
2. Monitor the following aspects to your model progress:
	* Model convergence.
	* Current and past loss values.
	* **Whether your session has terminated (be notified of it).**
	* Anything else you want (custom flagging)
	

********************
Library Installation
********************

Install using pip::

	pip install tensornow




***************
Getting Started
***************

First, create an account at `<http://www.tensornow.com/get-api-register/>`_ and get an API key.

Then hook the library into your code. Minimal example::

	from TensorNow import Now

	now = Now('user_id', 'api_key')


	def get_loss_val(count):
		# your loss value calculating function.
		...

	def train():
		now.start_training('G.A.N. r=1e5')	# Flag start training
		for i in range(epochs):
			loss_val = get_loss_val()
			now.log_loss(loss_val) # Upload loss values

			if loss_val>1000:
				now.flag_error("Model Collapse")

		
		now.end_training() # Flag end training.



	train()




***********
Source Code
***********

This Python interface is hosted on GitHub.

Please feel free to file an issue when you find a bug.



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
