from flask              import Flask, request, jsonify
from flask_sqlalchemy   import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Message model
class Signal(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    message_time    = db.Column(db.String, nullable=False)
    signal_time     = db.Column(db.String, nullable=False)
    open            = db.Column(db.Float, nullable=False)
    signal          = db.Column(db.String, nullable=False)
    take_profit     = db.Column(db.Float, nullable=False)
    stop_loss       = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'message time': self.message_time,
            'signal time': self.signal_time,
            'open': self.open,
            'signal': self.signal,
            'take profit': self.take_profit,
            'stop loss': self.stop_loss
        }

# Create the database and tables
with app.app_context():
    db.create_all()

def add_signal(data):
    new_signal = Signal(message_time=data["message time"],
                        signal_time=data["signal time"],
                        open=data["open"],
                        signal=data["signal"],
                        take_profit=data["take profit"],
                        stop_loss=data["stop loss"])
    
    db.session.add(new_signal)
    db.session.commit()

# Endpoint to receive and save Telegram messages
@app.route('/post_signal', methods=['POST'])
def save_signal():
    data = request.get_json()  # Expecting a JSON payload
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    # Save message to the list
    add_signal(data)
    return jsonify({'status': 'Message saved'}), 201

# Endpoint to retrieve the last signal
@app.route('/get_signal', methods=['GET'])
def get_signal():
    # Retrieve the last 'limit' messages from the database
    signal  = Signal.query.order_by(Signal.id.desc()).limit(1).all()[0]
    print(signal)
    # Convert messages to list of dictionaries
    signal  = [signal.to_dict()]
    
    return jsonify(signal)

# Endpoint to retrieve all signals
@app.route('/get_all_signal', methods=['GET'])
def get_all_signal():
    # Retrieve the last 'limit' messages from the database
    signals = Signal.query.order_by(Signal.id.desc()).all()
    # Convert messages to list of dictionaries
    signals = [signal.to_dict() for signal in signals]
    
    return jsonify(signals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=5000, debug=True)
