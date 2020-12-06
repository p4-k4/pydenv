#!/usr/bin/python3

import subprocess
import click

def listmonitors():
    process = subprocess.Popen([f'xrandr', '--listmonitors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    #print('Device: '+ output.decode('utf-8').split(' ')[3-4])
    return output.decode('utf-8').split(' ')[3-4].rstrip("\n")

def brightness_current():
    COMMAND = "xrandr --verbose | grep 'Brightness: ' | awk  '{print $2}'"
    process = subprocess.Popen([COMMAND], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    #print('Current brightness: ' + out.decode('utf-8').rstrip("\n"))
    return out.decode('utf-8').rstrip("\n")

def brightness_set(OPTION):
    CURRENT = brightness_current()
    MONITOR = listmonitors()
    print(f'{MONITOR} brightness: {CURRENT}')

    if OPTION == 'up':
        print('INCREASE REQUESTED')
        CURRENT = brightness_current()
        if float(CURRENT) >= 1.0:
            print('Brightness is max, no action required.')
            quit()
        else:
            VALUE = float(CURRENT)+float(0.1)
            COMMAND = f"xrandr --output {MONITOR} --brightness {VALUE}"
            process = subprocess.Popen([COMMAND], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

    if OPTION == 'down':
        print('DECREASE REQUESTED')
        if float(CURRENT) <= 0.1:
            print('Brightness is minimum, no action required.')
            quit()
        else:
            VALUE = float(CURRENT)-float(0.1)
            COMMAND = f"sudo xrandr --output {MONITOR} --brightness {VALUE}"
            process = subprocess.Popen([COMMAND], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

@click.command()
@click.option("--set", prompt="+ or -", help="Increase or decrease with +/-")
def input(set):
    brightness_set(OPTION=set)

if __name__ == '__main__':
    input()