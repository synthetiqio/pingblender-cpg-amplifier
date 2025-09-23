#sh
apt-update && apt upgrade 
apt-get install motion 

systemctl enable motion
systemctl start motion