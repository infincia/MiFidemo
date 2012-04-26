## Mi-Fi demo API provider

This is a simple but invaluable AppEngine tool for simulating the Mi-Fi CGI interface for querying status from the device.

I created this thing to test 3rd party apps like [Mi-Fi Monitor for Mac](http://infincia.com/apps/mi-fi-monitor-mac) and [Mi-Fi Monitor for iOS](http://infincia.com/apps/mi-fi-monitor-ios) to test functionality without having a working device available (comes in handy when asking Apple to review an app without sending them hardware)

If you need this thing, you already know why. If you just want to see an example of faking an API using AppEngine, here you go, have fun :)

Note: I'm not guaranteeing this API will actually give you every possible response a device would spit out, only that it will spit out responses that will allow you to test apps. Some devices will spit out totally psychotic responses, so USE THE REGEX FORCE, LUKE

###Querying

Most Mi-Fi devices only support GET requests, but they do require a specific query parameter that this code does not check for. On a real device you would hit a URL like this:

	http://192.168.1.1/getStatus.cgi?dataType=TEXT

And in return you get something like this:

    WwNetwkFound=0WwNetwkTech=UMTSWwNetwkName=AT&TWwRssi=4WwRoaming=0WwConnStatus=5BaBattStat=4BaBattChg=0WiConnClients=2WwDNS1=66.174.92.14WwIpAddr=70.213.218.196WwMask=255.255.255.255WwGateway=70.213.218.196WwSessionTxMb=0.01WwSessionRxMb=0.01WwSessionTimeSecs=62CurrRssi=-110
    
Note the esc character separating each key=value pair, make sure you parse this correctly. You may want to resort to using a regex to validate these things, because some devices will spit out things that will make your app cry otherwise


###Note about the debug handler

There is a small section of code here that handles debug data for [Mi-Fi Monitor for Mac](http://infincia.com/apps/mi-fi-monitor-mac), just ignore it. It's a simple email bouncing system that has nothing to do with the API
