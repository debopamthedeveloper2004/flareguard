from flask import Flask, request, redirect, url_for, render_template, flash
import pickle
import numpy as np

app = Flask(__name__)


model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def hello_world():
    return render_template("forest_fire.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get and validate form inputs
        temperature = int(request.form['Temperature'])
        oxygen = int(request.form['Oxygen'])
        humidity = int(request.form['Humidity'])
        
        # Prepare features for prediction
        final_features = [[temperature, oxygen, humidity]]
        
        # Make prediction
        prediction = model.predict_proba(final_features)
        probability = prediction[0][1] * 100  # Convert to percentage
        output = f'{probability:.2f}%'

        # Prepare alert message
        if probability > 50:
            alert_type = 'danger'
            message = f'⚠️ Your Forest is in Danger!<br>Fire Probability: {output}'
            advice = 'Immediate action required!'
        else:
            alert_type = 'success'
            message = f'✅ Your Forest is Safe<br>Fire Probability: {output}'
            advice = 'Normal conditions maintained'

        # Flash messages for single request
        flash(message, alert_type)
        flash(advice, 'advice')
        
        return redirect(url_for('hello_world'))

    except KeyError:
        flash('⚠️ Error: Missing form fields!', 'error')
        return redirect(url_for('hello_world'))
    except ValueError:
        flash('⚠️ Error: Invalid input values!', 'error')
        return redirect(url_for('hello_world'))
    except Exception as e:
        flash(f'⚠️ Unexpected error: {str(e)}', 'error')
        return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run(debug=True)