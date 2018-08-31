#This script uses the pysnmp library to poll SNMP data given a community string and an OID
from pysnmp.entity.rfc3413.oneliner import cmdgen 
import datetime

cg = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('public', mpModel=0)
transport1 = cmdgen.UdpTransportTarget(('10.10.10.10', 161))
transport2 = cmdgen.UdpTransportTarget(('10.10.10.11', 161))



#variables = (1,3,6,1,2,1,1,3,0) #uptime
#variables = (1,3,6,1,2,1,1,1,0) #SysDescription
#variables = (1,3,6,1,2,1,5,1,0) #icmpIn

def getData(transport):
	variableslist = [( 1,3,6,1,2,1,1,5,0),(1,3,6,1,2,1,1,1,0),(1,3,6,1,2,1,1,3,0),(1,3,6,1,2,1,5,1,0)] #sysname

	for i in range(len(variableslist)):
		errIndication, errStatus, errIndex, result = cg.getCmd(comm_data, transport, variableslist[i])
	
		if errIndication:
			print(errIndication)
		elif ':mib-2.5.1.0' in str(result[0]):
			rawdata = str(result[0])
			refinedData = rawdata.split('=')
			print('ICMP traffic in bytes = '+ refinedData[1])
	
		elif 'sysUpTime' in str(result[0]):
			rawdata = str(result[0])
			refinedData = rawdata.split('=')
			timeinseconds = int(refinedData[1])
			date_time = str(datetime.timedelta(seconds=timeinseconds))
			print('System uptime: ' + date_time)
		else:
			print(result[0])
if __name__ == '__main__':
	getData(transport1)
	getData(transport2)
