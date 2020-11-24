# install the library first
pip install python-kasa --pre

# perform device discovery ( I feel like this should work better than it does - may have to search manually on the local network.
kasa 

# get help
kasa --help

# Here you can set the target as the IP address as long as you know it
kasa --host 192.168.1.19

# turn device on or off
kasa --plug --host 192.168.1.7 on
kasa --plug --host 192.168.1.7 off

# turn the onboard LED off and on.
kasa --plug --host 192.168.1.37 led false
kasa --plug --host 192.168.1.87 led true

# Other commands
kasa --plug --host 192.168.1.11 state
kasa --plug --host 192.168.1.27 sysinfo