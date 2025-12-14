from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

reservations_db = {}

@app.route('/reservations', methods=['POST'])
def create_reservation():
    """
    Criar nova reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: body
        name: reservation
        schema:
          type: object
          required:
            - user_id
            - space_id
            - start_time
            - end_time
            - total_price
          properties:
            user_id:
              type: integer
            space_id:
              type: integer
            start_time:
              type: string
              format: date-time
            end_time:
              type: string
              format: date-time
            total_price:
              type: number
    responses:
      201:
        description: Reserva criada
      400:
        description: Dados inválidos
    """
    data = request.json
    reservation_id = len(reservations_db) + 1
    reservation = {
        'id': reservation_id,
        'user_id': data['user_id'],
        'space_id': data['space_id'],
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'status': 'active',
        'total_price': data['total_price']
    }
    reservations_db[reservation_id] = reservation
    return jsonify({'id': reservation_id}), 201

@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    """
    Obter detalhes da reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: path
        name: reservation_id
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da reserva
      404:
        description: Reserva não encontrada
    """
    reservation = reservations_db.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    return jsonify(reservation)

@app.route('/reservations/user/<int:user_id>', methods=['GET'])
def get_user_reservations(user_id):
    """
    Listar reservas do usuário
    ---
    tags:
      - Reservas
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Lista de reservas do usuário
    """
    user_reservations = [r for r in reservations_db.values() if r['user_id'] == user_id]
    return jsonify(user_reservations)

@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    """
    Cancelar reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: path
        name: reservation_id
        type: integer
        required: true
    responses:
      200:
        description: Reserva cancelada
      404:
        description: Reserva não encontrada
    """
    reservation = reservations_db.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    reservation['status'] = 'cancelled'
    return jsonify({'message': 'Reservation cancelled'})

@app.route('/admin/reservations', methods=['GET'])
def get_all_reservations():
    """
    Listar todas as reservas (Admin)
    ---
    tags:
      - Admin
    responses:
      200:
        description: Lista de todas as reservas
    """
    return jsonify(list(reservations_db.values()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)