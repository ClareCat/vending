"""
	Machine-Controlled, Generic, Expandable Interface for Vending and Amusement Appliances
	(McGeivaa)

	An API for creating unified systems for managing and using vending machines and arcade games
	and attaching them to the Internet.
"""

import sys

"""
	Logging Routines and Types
"""

def log(log_type, module_name, log_message):
	"""
		Log a message from an internal module
	"""
	if log_type > Log.Verbose:
		log(Log.Notice, "log", "Invalid log message type. Assuming `Info`.")
		log_type = Log.Info
	log_level = getConfig("log_print_level")
	if log_level is None:
		log_level = Log.Warn
	if log_type <= log_level:
		sys.stdout.write("[%s] %s: %s\n" % (_logNames[log_type], module_name, log_message))
	pass # TODO: Write to log file regardless

_logNames = ["Error", "Warn", "Notice", "Info"]

class Log:
	Error	= 0
	Warn	= 1
	Notice	= 2
	Info	= 3
	Verbose	= 4
	# TODO: Add any other log levels and ensure INFO is the most trivial. Adjust values to match.

def fatalError(message):
	"""
		Raise a fatal, internal error.
		Kill everything, log sufficiently, and inform the main class to restart.
	"""
	log(Log.Error, "api-main", "FATAL ERROR: %s -- Shutting down and restarting!" % message)
	sys.exit(0)
	# TODO: Shutdown, restart

"""
	State
"""

class State:
	Initalizing		= 0
	Ready			= 1
	Authenticated	= 2
	Confirm			= 3
	Acknowledge		= 4
	Vending			= 5
	Idaho			= 6
	New_York		= 7
	OfMind			= 8


state = 0

"""
	Configuration
"""

config_options = {}

def getConfig(config_option):
	if config_options.has_key(config_option):
		return config_options[config_option]
	else:
		return None

def _readConfig():
	"""
		Read the configuration
	"""
	try:
		conf_file = open("vend.conf")
		conf = conf_file.readlines()
		for i in conf:
			if (i.startswith("#")):
				continue
			i = i.replace("\n","")
			arr = i.split(": ")
			if len(arr) < 2:
				log(Log.Warn, "api-main", "Invalid configuration line: %s." % i)
				continue
			config_options[arr[0]] = eval(arr[1],globals(),locals())
			log(Log.Info, "api-main", "Setting config value `%s` to `%s`." % (arr[0], arr[1]))
		log(Log.Notice, "api-main", "Finished reading config file.")
	except:
		log(Log.Warn, "api-main", "Could not read config file (vend.conf), this may be bad.")

"""
	Main Object
"""

Tool = None

class Vending:
	"""
		Vending API super class
	"""
	def __init__(self):
		Tool = self
		_readConfig()
	def start(self):
		self.db.start()

"""
	Transaction Classes
"""

class User:
	def __init__(self, uid):
		self.uid = uid
	def chargeMoney(self, amount):
		pass
