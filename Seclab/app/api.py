from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from app.business_logic.ticket_logic import TicketBusinessLogic
from app.data_access.sql_data_access import SQLDataAccess

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change in production
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
# ensure query param names work in both common variants
app.config['JWT_QUERY_STRING_NAME'] = 'jwt'
app.config['JWT_QUERY_STRING_NAME'] = 'access_token'  # fallback for Swagger style if used
jwt = JWTManager(app)

swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/',
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    },
    # Removed global security to avoid issues with unprotected endpoints
}

swagger_template = {
    'info': {
        'title': 'Ticket API',
        'description': 'Simple ticket management API with JWT authentication',
        'version': '1.0',
    },
    'schemes': ['http', 'https'],
}

Swagger(app, template=swagger_template, config=swagger_config)

logic = TicketBusinessLogic(SQLDataAccess())

@app.route('/login', methods=['POST'])
def login():
    """
    Login to get JWT token
    ---
    parameters:
      - in: body
        name: credentials
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: password
    responses:
      200:
        description: JWT token
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    # Simple hardcoded check (replace with real auth)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/tickets', methods=['GET'])
@jwt_required()
def list_tickets():
    """
    Get all tickets
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: List of tickets
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              status:
                type: string
    """
    tickets = logic.get_all()
    return jsonify([
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
        }
        for t in tickets
    ])

@app.route('/tickets/process', methods=['POST'])
@jwt_required()
def process_file():
    """
    Process a CSV file and store tickets
    ---
    security:
      - Bearer: []
    parameters:
      - in: body
        name: payload
        schema:
          type: object
          properties:
            csv_path:
              type: string
              description: path to csv file to process
              example: data.csv
    responses:
      200:
        description: Processing result
    """
    data = request.get_json() or {}
    csv_path = data.get('csv_path')
    if not csv_path:
        return jsonify({'error': 'csv_path is required'}), 400

    try:
        logic.process_file(csv_path)
        return jsonify({'message': 'Processing complete'}), 200
    except FileNotFoundError:
        return jsonify({'error': f'File not found: {csv_path}'}), 404
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


@app.route('/tickets/upload', methods=['POST'])
@jwt_required(locations=['headers', 'query_string'])
def upload_csv():
    """
    Upload a CSV file and import tickets
    ---
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: CSV file with columns title,description,status
    responses:
      200:
        description: Upload and processing success
      400:
        description: Invalid request or bad CSV
    """
    if 'file' not in request.files:
        return jsonify({'error': 'file is required'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'filename is empty'}), 400

    try:
        import csv
        from io import StringIO

        stream = StringIO(file.stream.read().decode('utf-8'))
        rows = list(csv.DictReader(stream))
        if not rows:
            return jsonify({'error': 'CSV contains no rows'}), 400

        logic.process_rows(rows)
        return jsonify({'message': 'Upload and processing complete'}), 200
    except UnicodeDecodeError:
        return jsonify({'error': 'Unable to decode text data from uploaded file'}), 400
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/token', methods=['GET'])
def token_info_public():
    return jsonify({'message': 'public check ok'}), 200

@app.route('/token/auth', methods=['GET'])
@jwt_required()  # default locations from config
def token_info():
    """
    Test JWT token
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Token accepted
    """
    return jsonify({'message': 'token accepted'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
