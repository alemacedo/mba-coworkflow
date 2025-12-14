from flask import Flask, request, jsonify
from flasgger import Swagger
import requests
import datetime

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/checkin/<int:reservation_id>', methods=['POST'])
def checkin(reservation_id):
    """
    Fazer check-in na reserva
    ---
    tags:
      - Check-in/Check-out
    parameters:
      - in: path
        name: reservation_id
        type: integer
        required: true
        description: ID da reserva
    responses:
      200:
        description: Check-in realizado
        schema:
          type: object
          properties:
            message:
              type: string
            reservation_id:
              type: integer
            checkin_time:
              type: string
      400:
        description: Erro no check-in
      404:
        description: Reserva não encontrada
    """
    # Validar reserva
    try:
        response = requests.get(f'http://ms-reservas:5003/reservations/{reservation_id}')
        reservation = response.json()
        
        now = datetime.datetime.now()
        start_time = datetime.datetime.fromisoformat(reservation['start_time'])
        
        if now < start_time - datetime.timedelta(minutes=15):
            return jsonify({'error': 'Too early for check-in'}), 400
            
        if reservation['status'] != 'active':
            return jsonify({'error': 'Invalid reservation'}), 400
            
        return jsonify({
            'message': 'Check-in successful',
            'reservation_id': reservation_id,
            'checkin_time': now.isoformat()
        })
    except:
        return jsonify({'error': 'Reservation not found'}), 404

@app.route('/checkout/<int:reservation_id>', methods=['POST'])
def checkout(reservation_id):
    """
    Fazer check-out da reserva
    ---
    tags:
      - Check-in/Check-out
    parameters:
      - in: path
        name: reservation_id
        type: integer
        required: true
        description: ID da reserva
    responses:
      200:
        description: Check-out realizado
        schema:
          type: object
          properties:
            message:
              type: string
            reservation_id:
              type: integer
            checkout_time:
              type: string
    """
    return jsonify({
        'message': 'Check-out successful',
        'reservation_id': reservation_id,
        'checkout_time': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)