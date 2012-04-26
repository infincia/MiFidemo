#!/usr/bin/env python

# Copyright 2012 Stephen Oliver <mrsteveman1@gmail.com>
#
# Mi-Fi demo API built for Mi-Fi Monitor (http://infincia.com/apps/mi-fi-monitor-mac && http://infincia.com/apps/mi-fi-monitor-ios) 
#
# This is only useful if you need to test an application that 
# interacts with the Mi-Fi CGI API, it has no other use but as 
# example code for writing a somewhat hacked together AppEngine service :)

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import mail

import urllib2

import random

# These are global variables for tx/rx indicators so that they will increase and reset 
# randomly as AppEngine instances restart, they are not intended to do anything 
# but change from one request to the next
tx = 0.01
rx = 0.01

class APIHandler(webapp.RequestHandler):
	# this is a GET because virtually all devices support *only* GET requests, despite the spec saying 
	# they should support POST (I'm scowling at you here, AT&T)

	def get(self):

		# we're blatantly modifying global variables even though they will reset 
		# at some random point in the future, yep ... breaking all the rules, living on the wild side :D
		global tx
		global rx

		# this is either true or false
		WwNetwkFound = random.choice(["0", "1"])

		# hardcoded for AT&T but could be virtually anything
		WwNetwkName = "AT&T"

		# type of network connection offered by the Mi-Fi
		WwNetwkTech = random.choice(["GPRS", "UMTS", "HSPA", "HSUPA"])

		# this is typically a 0 or 1 in practice, i've never seen it return 2 but its in the spec somewhere
		WwRoaming = random.choice(["0", "1", "2"])

		# this is equivalent to "bars" on a cellphone
		WwRssi = random.choice(["0", "1", "2", "3", "4", "5"])

		# this is a tricky one, these are defined by the Mi-Fi CGI spec but they have been found to 
		# vary on some devices (thanks, wireless carriers)
		WwConnStatus = random.choice(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]) 
		
		# grab whatever current global state exists for the tx/rx counters so they can be returned in the formatted API string
		WwSessionTxMb = tx
		WwSessionRxMb = rx

		# now increment the global counters for next time
		rx += 0.01
		tx += 0.01

		
		WwSessionTimeSecs = random.choice(["60", "61", "62"])

		# arbitrary IP values so that they at least exist, most api clients dont even use these
		WwIpAddr = "216.54.43.98"
		WwMask = "255.255.255.0"
		WwGateway = "216.54.43.1"
		WwDNS1 = "4.2.2.2"

		# essentially crude battery levels, 0%, 25%, 50%, 75% and 100%
		BaBattStat = random.choice(["0", "1", "2", "3", "4"])

		# boolean to indicate whether the device thinks its charging or not
		# this is random but the real device may as well be random too, unreliable :)
		BaBattChg = random.choice(["0", "1"])

		# indicate how many Wi-Fi clients are currently connected to the device
		WiConnClients = random.choice(["1", "2", "3", "4", "5"])
		
		# this is actually not listed in the original CGI spec but has been seen on WiMax devices, supposed to be a raw rssi level
		CurrRssi = random.choice(["-45","-50","-60","-30","-90","-101","-110"])

		# write out a formatted response as a simple text string, each key=value pair is separated by the esc character
		self.response.out.write('WwNetwkFound=' + WwNetwkFound + "" + 'WwNetwkTech=' + WwNetwkTech + "" + 'WwNetwkName=' + WwNetwkName + "" + 'WwRssi=' + WwRssi + "" + 'WwRoaming=' + WwRoaming + "" + 'WwConnStatus=' + WwConnStatus + "" + 'BaBattStat=' + BaBattStat + "" + 'BaBattChg=' + BaBattChg + "" + 'WiConnClients=' + WiConnClients + "" + 'WwDNS1=' + WwDNS1 + "" + 'WwIpAddr=' + WwIpAddr + "" + 'WwMask=' + WwMask + "" + 'WwGateway=' + WwGateway + "" + 'WwSessionTxMb=' + str(WwSessionTxMb) + "" + 'WwSessionRxMb=' + str(WwSessionRxMb) + "" + 'WwSessionTimeSecs=' + WwSessionTimeSecs + "" + 'CurrRssi=' + CurrRssi)


# this simulates the GPS api found on some Mi-Fi devices, a lot of them have disabled or crippled it so it isn't of much use, but here it is just in case :)
# If you're wondering what the coordinates are, they're somewhere in China, and they jump around psychotically
class GPSHandler(webapp.RequestHandler):
	def get(self):
		altitude = random.choice(["40", "41", "42", "43", "44"])
		angle_uncertainty = "13"
		fix_type = "1"
		heading = random.choice(["250", "315", "90", "12", "140"])
		horizontal_velocity = "0"
		latitude = random.choice(["32.895", "31.895", "34.895", "32.495", "32.795"])
		longitude = "117.201"
		perpendicular_std_dev_uncertainty = "8"
		std_dev_uncertainty = "9"
		timestamp_str = "07/15/2009 04:22:10"
		pmvertical_std_dev_uncertainty = "11"
		vertical_velocity = "0"
		horizontal_accuracy = "14"
		vertical_accuracy = "24"
		loc_uncertainty_conf = "39"
		status = "0"
            
		self.response.out.write('altitude=' + altitude + "" + 'angle_uncertainty=' + angle_uncertainty + "" + 'fix_type=' + fix_type + "" + 'heading=' + heading + "" + 'horizontal_velocity=' + horizontal_velocity + "" + 'latitude=' + latitude + "" + 'longitude=' + longitude + "" + 'perpendicular_std_dev_uncertainty=' + perpendicular_std_dev_uncertainty + "" + 'std_dev_uncertainty=' + std_dev_uncertainty + "" + 'timestamp_str=' + timestamp_str + "" + 'pmvertical_std_dev_uncertainty=' + pmvertical_std_dev_uncertainty + "" + 'vertical_velocity=' + vertical_velocity + "" + 'horizontal_accuracy=' + horizontal_accuracy + "" + 'vertical_accuracy=' + vertical_accuracy + "" + 'loc_uncertainty_conf=' + loc_uncertainty_conf + "" + 'status=' + status)


# this is used by the Mac version of Mi-Fi Monitor to send debug data back for various reasons, its just a string being passed in via POST and emailed 
# has absolutley nothing to do with the API but has been useful 
class DebugHandler(webapp.RequestHandler):
	def get(self):
		pass
	def post(self):
		debugString = self.request.get('debugData')
		self.notifyemail(debugString)
	

	def notifyemail(self,debugdata):
		message = mail.EmailMessage()
		message.sender = "mrsteveman1@gmail.com"
		message.subject = "debug data"
		message.to = "debug@infincia.com"
		message.body = "%s" % debugdata
		message.send()



def main():
    application = webapp.WSGIApplication( [ ('/getStatus.cgi', APIHandler), ('/submitDebugData',DebugHandler), ('/getlastfix.cgi', GPSHandler) ] )
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
