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
