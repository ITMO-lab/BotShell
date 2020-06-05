sudo apt update -y
sudo apt upgrade -y

sudo apt install -y redis-server
sudo systemctl enable redis-server.service
sudo npm install -g redis-commander

sudo apt install -y rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
#sudo ufw allow proto tcp from any to any port 5672,15672
#rabbitmqctl add_user admin {YOUR_PASSWORD}
#rabbitmqctl set_user_tags admin administrator
