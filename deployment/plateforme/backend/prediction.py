from flask import Blueprint, render_template, request
from flask_login import LoginManager, login_required
from flask_cors import cross_origin
import joblib

# List of US state codes
States = [
    'CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'MI', 'GA', 'NC', 'NJ', 'VA',
    'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI', 'CO', 'MN', 'SC', 'AL',
    'LA', 'KY', 'OR', 'OK', 'CT', 'UT', 'IA', 'NV', 'AR', 'MS', 'KS', 'NM',
    'NE', 'WV', 'ID', 'HI', 'ME', 'NH', 'RI', 'MT', 'DE', 'SD', 'ND', 'AK',
    'VT', 'WY',
]

# State-to-code mapping
StatesCodes = {state: idx for idx, state in enumerate(States)}

# Load pre-trained model
model = joblib.load(r"C:\Users\user\Desktop\plateforme\backend\rf_model.joblib")


# Create Blueprint
prediction = Blueprint('prediction', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(prediction)


@prediction.route('/prediction', methods=['GET'])
@login_required
def show():
    return render_template('prediction.html', States=States)


@prediction.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    try:
        # Extract and validate form inputs
        Account_length = int(request.form.get("account_length", 0))
        Number_vmail_messages = int(request.form.get("number_vmail_messages", 0))
        Total_day_calls = int(request.form.get("total_day_calls", 0))
        Total_day_charge = float(request.form.get("total_day_charge", 0.0))
        Total_eve_calls = int(request.form.get("total_eve_calls", 0))
        Total_eve_charge = float(request.form.get("total_eve_charge", 0.0))
        Total_night_calls = int(request.form.get("total_night_calls", 0))
        Total_night_charge = float(request.form.get("total_night_charge", 0.0))
        Total_intl_calls = int(request.form.get("total_intl_calls", 0))
        Total_intl_charge = float(request.form.get("total_intl_charge", 0.0))
        Customer_service_calls = int(request.form.get("customer_service_calls", 0))
        State_encoded = int(request.form.get("State_encoded", 0))


        

        # Convert Yes/No to binary
        International_plan = request.form.get("international_plan_encoded", "No")
        International_plan_encoded = 1 if International_plan.lower() == "yes" else 0

        Voice_mail_plan = request.form.get("voice_mail_plan_encoded", "No")
        Voice_mail_plan_encoded = 1 if Voice_mail_plan.lower() == "yes" else 0
        if  State_encoded in  States:
             State_encoded = StatesCodes[State_encoded]
        else:
            StatesCodes = -1 

        

        # Perform prediction
        prediction = model.predict([[
            Account_length,
            Number_vmail_messages,
            Total_day_calls,
            Total_day_charge,
            Total_eve_calls,
            Total_eve_charge,
            Total_night_calls,
            Total_night_charge,
            Total_intl_calls,
            Total_intl_charge,
            Customer_service_calls,
            State_encoded,
            International_plan_encoded,
            Voice_mail_plan_encoded,
        ]])

        output = prediction[0]

        # Map prediction to message
        result_text = "The customer is likely to churn." if output == 1 else "The customer is not likely to churn."

        # Return result
        return render_template('prediction.html', prediction_text=result_text, States=States)

    except Exception as e:
        # Handle unexpected errors
        return render_template('prediction.html', prediction_text=f"Error occurred: {str(e)}", States=States)
