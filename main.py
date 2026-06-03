from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# 1. Your Email Configurations (Stored securely away from the APK)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")       # Your sending email
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD") # Your email app password
RECEIVER_EMAIL = "target-app@example.com"            # Where the JSON is going

@app.route('/send-json', methods=['POST'])
def send_json_email():
    try:
        # Get data sent from the mobile app
        user_data = request.json
        
        # Convert the data into a clean, formatted JSON string
        import json
        json_payload = json.dumps(user_data, indent=4)
        
        # Create the email message
        msg = MIMEText(json_payload, 'plain')
        msg['Subject'] = 'New Data Submission'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        
        # Log into Gmail's servers and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        return jsonify({"status": "success", "message": "JSON sent successfully!"}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)