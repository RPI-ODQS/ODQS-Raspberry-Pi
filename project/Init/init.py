import subprocess
from shutil import copyfile
import time

'''
thePATH = '/home/pi/Documents/water/Init/'
'''
thePATH = './'

filename = 'autolaunch'

copyfile(thePATH+filename, "/etc/init.d/"+filename)
subprocess.call('sudo chmod +x /etc/init.d/'+filename, shell=True)
subprocess.call('sudo update-rc.d '+filename + ' defaults', shell=True)
subprocess.call('sudo insserv '+filename, shell=True)
#time.sleep(10)
subprocess.call('reboot', shell=True)
