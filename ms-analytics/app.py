from flask import Flask, jsonify
from flasgger import Swagger
import random

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/analytics/dashboard', methods=['GET'])
def get_dashboard():
    """
    Obter dados do dashboard de analytics
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Dados do dashboard
        schema:
          type: object
          properties:
            total_users:
              type: integer
            active_reservations:
              type: integer
            occupancy_rate:
              type: number
            popular_spaces:
              type: array
              items:
                type: string
            peak_hours:
              type: array
              items:
                type: string
    """
    return jsonify({
        'total_users': random.randint(100, 1000),
        'active_reservations': random.randint(10, 50),
        'occupancy_rate': round(random.uniform(60, 95), 1),
        'popular_spaces': ['Sala A', 'Sala B', 'Auditório'],
        'peak_hours': ['09:00-11:00', '14:00-16:00']
    })

@app.route('/analytics/usage', methods=['GET'])
def get_usage():
    """
    Obter relatório de uso dos espaços
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Dados de uso
        schema:
          type: object
          properties:
            daily_bookings:
              type: integer
            average_session_duration:
              type: number
            most_used_space:
              type: string
            busiest_day:
              type: string
    """
    return jsonify({
        'daily_bookings': random.randint(20, 80),
        'average_session_duration': round(random.uniform(2, 6), 1),
        'most_used_space': 'Sala de Reunião A',
        'busiest_day': 'Terça-feira'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)