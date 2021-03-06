#!/usr/bin/python3
# coding: utf-8


import os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException , WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary # for specifying the path to firefox binary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep,ctime
import multiprocessing
import time
import datetime
import argparse
import json

#getting the ENV files for the SSLKEYLOG
SSLKEY   = os.getenv('SSLKEYLOGFILE')
SSLDEBUG = os.getenv('SSLDEBUGFILE')


def getDateFormat(timestamp):
    '''
    This simple function converts traditional UNIX timestamp to YMD_HMS format
    timestamp int - unix timestamp to be converted
    return String - the YMD_HMS format as a string
    '''
    return datetime.datetime.\
        fromtimestamp(float(timestamp)).strftime('%Y%m%d_%H%M%S')


#get current timestamp and convert it
ts = time.time()
timestamp = getDateFormat(str(ts))


# parser for the command line arguements
parser = argparse.ArgumentParser(description="DoH packet capture and .csv conversion script!")

parser.add_argument('-s', action="store", default=1, type=int, dest="start" , help="Specify rank of the starting website")
parser.add_argument('-e', action="store", default=5000, type=int, dest="end" , help="Specify rank of the ending website")
parser.add_argument('-b', action="store", default=200, type=int, dest="batch" , help="Batch Size (range must be a multiple of batch size!)")
parser.add_argument('-r', action="store", default=1, type=int, dest="doh_resolver" , help="DoH resolver :\n1=Cloudflare; \n2=Google;\n3=CleanBrowsing;\n4=Quad9;")
parser.add_argument('-i', '--interface', nargs=1,
                    help="Specify the interface to use for capturing",
                    required=False,
                    default=['eth0'])

results = parser.parse_args()

# setup logging features
log_file = "log_"+str(timestamp)
print("Creating log file "+log_file)
logs = open(log_file, 'a')
logs.write("Logging for doh_capture.py started on "+timestamp+"\n\n")

# remove previous symlink if there was any
if os.system("rm -rf progress.log") == 0:
    print("symlink to previous log file has been deleted")
    logs.write("symlink to previous log file has been deleted\n")
else:
    print("symlink to previous log file could NOT be deleted")
    logs.write("symlink to previous log file could NOT be deleted\n")

# create symlink to the new log file
if os.system("ln -s "+str(log_file)+" progress.log") == 0:
    print("creating symlink progress.log to "+str(log_file)+" is successfull")
    logs.write("creating symlink progress.log to "+str(log_file)+" is successfull\n")
else:
    print("creating symlink progress.log to "+str(log_file)+" was NOT successfull")
    logs.write("creating symlink progress.log to "+str(log_file)+" was NOT successfull\n")


resolver = ""

if(results.doh_resolver==1) :
    resolver = "cloudflare"
elif(results.doh_resolver==2) :
    resolver = "google"
elif(results.doh_resolver==3) :
    resolver = "cleanbrowsing"
elif(results.doh_resolver==4) :
    resolver = "quad9"
else :
    print("Invalid choice for DoH resolver!\nExiting...")
    logs.write("Invalid choice for DoH resolver!\nExiting...")
    logs.flush()
    logs.close()
    exit(0)

def get_resolver_details(resolver) :
    with open('r_config.json') as f:
        resolver_config = json.load(f)
    return resolver_config[resolver]["uri"], resolver_config[resolver]["bootstrap"]


uri , bootstrap = get_resolver_details(resolver)


start = results.start
stop = results.end
batch_size = results.batch
time_out = batch_size * 15
interface = results.interface[0]

# Fine-tune batch size if it is bigger than stop-start
max_possible_batch_size = stop-start+1
if (batch_size > max_possible_batch_size):
    batch_size = max_possible_batch_size


print("Printing script Parameters: ")
logs.write("Printing script Parameters: \n")
print("Start = "+str(start))
logs.write("Start = "+str(start)+"\n")
print("End = "+str(stop))
logs.write("End = "+str(stop)+"\n")
print("(Adjusted) Batch_Size = "+str(batch_size))
logs.write("(Adjusted) Batch_Size = "+str(batch_size)+"\n")
print("DoH_Resolver = "+uri)
logs.write("DoH_Resolver = "+str(uri)+"\n")


data = pd.read_csv('top-1m.csv' , names = ['rank','website'])

print("Process started: " + str(time.ctime()))
logs.write("Process started: " + str(time.ctime())+"\n\n\n")

options = Options()
options.headless = True


## specifying the binary path
binary = FirefoxBinary('./firefox/firefox')



## DesiredCapabilities
#cap = DesiredCapabilities().FIREFOX
#cap['marionette'] = False

#profile = webdriver.FirefoxProfile('/home/user/.mozilla/firefox/0b5055qu.Doh_profile')
## setting the firefox profile to use DoH
profile = webdriver.FirefoxProfile()
profile.set_preference("network.trr.mode", 2)
profile.set_preference("network.trr.uri", uri)
profile.set_preference("network.trr.bootstrapAddress", bootstrap)


logs.flush()



def open_website(url,count):
    #driver = webdriver.Firefox(firefox_profile=profile)
    # logs = open('Progress.txt', 'a')
    tmp_ts = time.time()
    tmp_timestamp = getDateFormat(str(tmp_ts))

    print(str(count)+" "+url+" (visited: "+str(tmp_timestamp)+")\n")
    logs.write(str(count)+" "+url+" (visited: "+str(tmp_timestamp)+")\n")

    ## in the executabel path you need to specify the location of geckodriver location.
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.set_page_load_timeout(16)
    try :
        driver.get(url)
        sleep(2)
    except TimeoutException as ex1 :
        print("TimeoutException Exception has been thrown "+ str(ex1))
        sleep(2)
        logs.write("TimeoutException Exception has been thrown \n"+str(ex1)+"\n")
    except WebDriverException as ex2 :
        print("WebDriverException Exception has been thrown "+ str(ex2))
        sleep(2)
        logs.write("WebDriverException Exception has been thrown \n"+str(ex2)+"\n")
    except Exception as ex3:
        print("Unknown exception has been thrown "+ str(ex3))
        sleep(2)
        logs.write("Unknown exception has been thrown \n"+str(ex3)+"\n")
    logs.flush()
    driver.close()
    sleep(1)

def main_driver(s,e) :
    count = s
    df = data.iloc[s-1:e]
    for domain in df['website'] :
        url = 'https://www.' + domain
        open_website(url,count)
        count = count + 1

    print("batch completed")
    logs.write("batch completed"+"\n")
    logs.flush()


s = start
e = s+batch_size-1



def capture_packets(shell_command) :
    os.system(shell_command)



while(e<=stop) :
    if(e>stop) :
        e=stop

    filename = 'pcap/capture-'+str(s)+'-'+str(e)

    ## here after -i you need to add the ethernet port. which i guess is eth0
    shell_command = "sudo timeout 4400 tcpdump port 443 -i " + interface + " -w " + filename

    t1 = multiprocessing.Process(target=main_driver, args=(s,e,))
    t2 = multiprocessing.Process(target=capture_packets, args=(shell_command,))

    t2.start()
    sleep(3)
    t1.start()

    t1.join()
    sleep(5)
    t2.terminate()

    print("Done")
    logs.write("Done"+"\n")
    logs.flush()
    sleep(2)
    print(time.ctime())
    logs.write(time.ctime())
    logs.flush()
    s = s+batch_size
    e = e+batch_size

    # csv generation
    f=filename
    output_file_name = "csv/csvfile-"+f.split('-')[1] + "-" + f.split('-')[2] +".csv"
    print("Running pcap file analyser to create the csv file {}...".format(output_file_name))
    logs.write("Running pcap file analyser to create the csv file {}...\n".format(output_file_name))
    logs.flush()

    csv_command = 'tshark -r ' + filename +' -Y "http2" -o tls.keylog_file:'+SSLKEY+' -T fields -e frame.number -e _ws.col.Time -e ip.src -e ip.dst -e _ws.col.Protocol -e frame.len -e _ws.col.Info -E header=y -E separator="," -E quote=d -E occurrence=f > '+ output_file_name
    remove_file = "sudo rm -rf "+filename
    os.system(csv_command)
    os.system(remove_file)
    print(output_file_name + " completed!")
    logs.write(output_file_name + " completed!\n\n")
    logs.flush()


logs.close()
