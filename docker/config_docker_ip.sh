sudo service docker stop
sudo brctl addbr docker1
sudo ifconfig docker1 10.1.16.25/24 netmask 255.255.255.0
sudo service docker start 
