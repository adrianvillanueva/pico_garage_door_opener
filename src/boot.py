import network
import machine
import time

wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.ifconfig([{{ IP }}, {{ SUBNET_MASK }}, {{ ROUTER }}, {{ DNS }}])
    wlan.active(True)
    wlan.connect({{ SID }}, {{ PASSWORD }})

    # Wait for connect or fail
    wait = 10
    while wlan.isconnected():
        if wait == 0:
            break
        wait -= 1
        print('waiting for connection...')
        time.sleep(1)
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
    machine.reset()
else:
    print('connected to wifi')
