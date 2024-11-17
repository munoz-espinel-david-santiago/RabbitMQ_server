# RabbitMQ_server
Proyecto de servicios telematicos
# manual de instalacion rabbit
_NOTA_ : Recuerda ejecutar estos comandos con el super usuario `root`

```
cat /etc/system-release ; sestatus ; hostname ; hostname -I ; dnf groupinstall "Development Tools" -y
```
```
dnf install epel-release curl -y
```
```
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | bash
```
```
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | bash
```
```
dnf install erlang -y
```
```
dnf install rabbitmq-server -y
```
```
systemctl start rabbitmq-server ; systemctl enable rabbitmq-server
```
```
rabbitmqctl add_user admin
```
```
rabbitmqctl set_user_tags admin administrator
```
```
rabbitmqctl list_users
```
```
rabbitmqctl add_vhost /new_vhost
```
```
rabbitmqctl list_vhosts
```
```
rabbitmqctl set_permissions -p /new_vhost admin ".*" ".*" ".*"
```
```
rabbitmq-plugins enable rabbitmq_management
```
```
systemctl restart rabbitmq-server
```
```
rabbitmqctl status
```
```
ss -antpl | grep 15672
```
_NOTA_ : Recuerda que el protocolo rabbotmq esta determinado en el puerto `15672`
```
http://localhost:15672
```
Enlance de la instalacion
https://quicknotepadtutorial.blogspot.com/2022/04/how-to-install-and-configure-rabbitmq.html


# manual de intalacion de grafana para graficar 
## instalacion y configuracion de grafana para rocky linux 
### paso 1: importar llaves de  the GPG key:
```
wget -q -O gpg.key https://rpm.grafana.com/gpg.key
sudo rpm --import gpg.key
```
### paso 2 Crea /etc/yum.repos.d/grafana.repo con el siguiente contenido ::
```
[grafana]
name=grafana
baseurl=https://rpm.grafana.com
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://rpm.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
```
### paso 3: instalar grafana
```
sudo dnf install grafana
```

### paso 4: habilitar el servicio 
```
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```



### paso 5: accerder a grafana 
Acceder a Grafana: Abre un navegador web y accede a Grafana usando la dirección http://<tu-IP>:3000.

Usuario y contraseña predeterminados: admin para ambos.
### paso 6: instalar el plugin de rabbitmq
```
sudo grafana-cli plugins install rabbitmq-monitor
```

### paso 7: reiniciar el servicio rabbitmq
```
sudo systemctl restart grafana-server
```

1. Mandar datos desde un dispositivo o maquina (En este caso mandaremos los datos de una maquina virtual).
- instalar libreria pika
```
pip install pika
```
- ejecutar el siguiente codigo `python emisor.py`
```
import pika
import json
import random
import time

# Configuración de conexión
rabbitmq_host = "IP_DE_TU_MAQUINA_VIRTUAL"
rabbitmq_user = "myuser"
rabbitmq_password = "mypassword"
queue_name = "mi_cola"

# Configurar credenciales
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
)

# Crear canal y declarar la cola
channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True)

try:
    while True:
        # Crear un mensaje JSON con valor aleatorio
        mensaje = {
            "id": 1,
            "nombre": "Sensor",
            "valor": round(random.uniform(10.0, 30.0), 2),  # Valor aleatorio entre 10 y 30
            "unidad": "Celsius"
        }

        # Publicar el mensaje
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(mensaje),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistente
        )

        print(f"Mensaje enviado: {mensaje}")
        time.sleep(5)  # Esperar 5 segundos antes de enviar el siguiente mensaje

except KeyboardInterrupt:
    print("\nDetenido por el usuario")
finally:
    connection.close()
```
2. configuramos grafana para recibir los datos y graficarlos
3. ejecutamos otro codigo en el servidor para probar si llegan los datos
- codigo `python receptor.py`
```
import pika
import json

# Configuración de conexión
rabbitmq_host = "IP_DE_TU_MAQUINA_VIRTUAL"
rabbitmq_user = "myuser"
rabbitmq_password = "mypassword"
queue_name = "mi_cola"

# Configurar credenciales
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
)

# Crear canal
channel = connection.channel()

# Callback para procesar mensajes
def callback(ch, method, properties, body):
    mensaje = json.loads(body)
    print(f"Mensaje recibido: {mensaje}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirmar recepción

# Escuchar mensajes
channel.basic_consume(queue=queue_name, on_message_callback=callback)
print("Esperando mensajes. Presiona CTRL+C para salir.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nDetenido por el usuario")
finally:
    connection.close()
```
4. Instrucciones para ejecución
En la máquina virtual, ejecuta primero el receptor para que esté listo para escuchar mensajes:

```
python receptor.py
```
En la otra máquina, ejecuta el emisor para enviar datos continuamente:
```
python emisor.py
```
Verás los mensajes generados aleatoriamente en la consola del receptor.
