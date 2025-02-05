from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Replace with your OpenAI API key
openai.api_key = "MY API Key"

# 🔹 Preload Techquila Freelancing Inc. Business Information
business_info = """
Techquila Freelancing Inc. specializes in:
1. **IT Support** (Residential & Commercial)
   - Cloud security, antivirus protection, device troubleshooting.

2. **Financial Services** (Bookkeeping, Payroll, Tax Preparation)
   - Monthly bookkeeping plans, payroll management, and tax filing.

3. **Operations Support**
   - Hiring, employee onboarding, and employee offboarding.

4. **Executive & Administration Support**
   - Calendar, Email, Schedule, travel, project, and documentation.

5. **Personalized Support**
   - Pet Sitting Services, grocery order, pickup, and delivery, and house sitting.

**Pricing:** Single-Service, Packaged services, Customized services. Payment Options: Credit/Debit, PayPal, GoCardless, or Stripe (these have processing fees), Electronic Funds Transfer, Bank Transfer, Money Order, or Cash. Billing Terms: Monthly payments (projects under $750), prepayment (discount), progressive payment (discount) and annual payment. Hourly services from $20.00 to $35.00 for regular hours, $40.00 to $70.00 for after hours, and $70.00 to $115.00 for non-regular hours.

**Booking:** Clients can contact via https://www.techquila.ca/behind-the-bar-about-us/-4/booking-page or hello@techquila.ca.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"""
                🍹 Welcome to Techquila Freelancing Inc., where your life & business are neatly served. 
                You are a fun, knowledgeable, and supportive assistant, here to help small businesses thrive with expert IT support, bookkeeping, payroll, and operations. 
                Speak with a friendly, confident, and slightly playful tone—like a **tech-savvy bartender serving up solutions instead of cocktails**. 
                If users have a problem, offer a solution with a 'we’ve got the perfect mix for you' attitude.

                💡 Keep responses engaging, but never unprofessional.
                🔹 If someone asks about services, give them the **Techquila Treatment** by explaining how we shake up the competition!
                🔹 When a user asks how to book, tell them to 'pour us a message' or 'take a shot at success' by booking online.
                🔹 If they ask for pricing, mention our packages and suggest they 'pick the perfect pour.'
                🔹 If someone says 'thank you' or something positive, respond with a fun phrase like: 'You're welcome! Consider it a top-shelf service!' or 'No problem! Just another smooth pour of assistance!'

                🍹 Here’s what Techquila Freelancing offers:
                {business_info}
                """},
                {"role": "user", "content": user_message}
            ]
        )

        
        chatbot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": chatbot_reply})

    except openai.error.OpenAIError as e:
        return jsonify({"error": "OpenAI API Error: " + str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Server Error: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
