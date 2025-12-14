from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/notify/email', methods=['POST'])
def send_email():
    """
    Enviar notificação por e-mail
    ---
    tags:
      - Notificações
    parameters:
      - in: body
        name: email
        schema:
          type: object
          required:
            - to
            - subject
            - body
          properties:
            to:
              type: string
              format: email
            subject:
              type: string
            body:
              type: string
    responses:
      200:
        description: E-mail enviado
    """
    data = request.json
    # Simular envio de e-mail
    print(f"Email sent to {data['to']}: {data['subject']}")
    return jsonify({'message': 'Email sent successfully'})

@app.route('/notify/sms', methods=['POST'])
def send_sms():
    """
    Enviar notificação por SMS
    ---
    tags:
      - Notificações
    parameters:
      - in: body
        name: sms
        schema:
          type: object
          required:
            - phone
            - message
          properties:
            phone:
              type: string
            message:
              type: string
    responses:
      200:
        description: SMS enviado
    """
    data = request.json
    print(f"SMS sent to {data['phone']}: {data['message']}")
    return jsonify({'message': 'SMS sent successfully'})

@app.route('/notify/push', methods=['POST'])
def send_push():
    """
    Enviar push notification
    ---
    tags:
      - Notificações
    parameters:
      - in: body
        name: push
        schema:
          type: object
          required:
            - user_id
            - title
            - message
          properties:
            user_id:
              type: integer
            title:
              type: string
            message:
              type: string
    responses:
      200:
        description: Push notification enviado
    """
    data = request.json
    print(f"Push sent to user {data['user_id']}: {data['title']}")
    return jsonify({'message': 'Push notification sent'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)