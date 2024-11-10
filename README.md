# RabbitMQ_server
Proyecto de servicios telematicos
# manual de instalacion rabbit
cat /etc/system-release ; sestatus ; hostname ; hostname -I ; dnf groupinstall "Development Tools" -y
dnf install epel-release curl -y
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | bash
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | bash
dnf install erlang -y
dnf install rabbitmq-server -y
systemctl start rabbitmq-server ; systemctl enable rabbitmq-server
rabbitmqctl add_user admin
rabbitmqctl set_user_tags admin administrator
rabbitmqctl list_users
rabbitmqctl add_vhost /new_vhost
rabbitmqctl list_vhosts
rabbitmqctl set_permissions -p /new_vhost admin ".*" ".*" ".*"
rabbitmq-plugins enable rabbitmq_management
systemctl restart rabbitmq-server
rabbitmqctl status
ss -antpl | grep 15672
http://192.168.1.20:15672

Enlance de la instalacion
https://quicknotepadtutorial.blogspot.com/2022/04/how-to-install-and-configure-rabbitmq.html
