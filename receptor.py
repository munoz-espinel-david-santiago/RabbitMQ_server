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
