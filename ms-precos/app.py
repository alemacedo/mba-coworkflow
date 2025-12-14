from flask import Flask, request, jsonify
from flasgger import Swagger
import datetime

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/pricing/calc', methods=['POST'])
def calculate_price():
    """
    Calcular preço da reserva
    ---
    tags:
      - Preços
    parameters:
      - in: body
        name: pricing
        schema:
          type: object
          required:
            - space_id
            - start_time
            - end_time
          properties:
            space_id:
              type: integer
            start_time:
              type: string
              format: date-time
            end_time:
              type: string
              format: date-time
            user_plan:
              type: string
              enum: ['basic', 'premium', 'enterprise']
              default: basic
    responses:
      200:
        description: Preço calculado
        schema:
          type: object
          properties:
            base_price:
              type: number
            hours:
              type: number
            discount:
              type: number
            total:
              type: number
    """
    data = request.json
    
    # Preço base por hora
    base_price = 25.0
    
    # Calcular horas
    start = datetime.datetime.fromisoformat(data['start_time'])
    end = datetime.datetime.fromisoformat(data['end_time'])
    hours = (end - start).total_seconds() / 3600
    
    # Aplicar descontos por plano
    discounts = {
        'basic': 0.0,
        'premium': 0.1,
        'enterprise': 0.2
    }
    
    discount = discounts.get(data.get('user_plan', 'basic'), 0.0)
    total = base_price * hours * (1 - discount)
    
    return jsonify({
        'base_price': base_price,
        'hours': hours,
        'discount': discount,
        'total': round(total, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)