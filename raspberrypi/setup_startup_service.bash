# Note: Script must be run as root (sudo OK) because it writes file in LIB directory

# Create startup shell that runs python script
echo "/usr/bin/python /home/bruce/pitoys/raspberrypi/buttonpressed.py" > /home/bruce/startup.bash
# for debug, add > log.txt 2>&1 at the end to cause all info to be written to a log file in the home dir
chmod 775 /home/bruce/startup.bash
# Could be worth testing the startup script now - optional
# /bin/bash /home/bruce/startup.bash

# Now create the service file for systemctl
echo "[Unit]" > /lib/systemd/system/startup.service
echo "Description=Service Description" >> /lib/systemd/system/startup.service
echo "After=multi-user.target" >> /lib/systemd/system/startup.service
echo "" >> /lib/systemd/system/startup.service
echo "[Service]" >> /lib/systemd/system/startup.service
echo "WorkingDirectory=/home/bruce/" >> /lib/systemd/system/startup.service
echo "User=bruce" >> /lib/systemd/system/startup.service
echo "ExecStart=/bin/bash /home/bruce/startup.bash" >> /lib/systemd/system/startup.service
echo "" >> /lib/systemd/system/startup.service
echo "[Install]" >> /lib/systemd/system/startup.service
echo "WantedBy=multi-user.target" >> /lib/systemd/system/startup.service

# Service file should be OK.  Now fix the file permissions
sudo chmod 644 /lib/systemd/system/startup.service

# reload systemd and then enable the service
sudo systemctl daemon-reload
sudo systemctl enable startup.service

# Now just reboot and the service should start up automatically
