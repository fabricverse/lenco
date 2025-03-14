import requests
import time
import hashlib
import hmac
import json

def get_payment_status(data):
    # return *args
    frappe.errprint("data", data)

def request(doc, method):
    return {
        "status": True,
        "message": "",
        "data": {
            "id": "d7bd9ccb-0737-4e72-a387-d00454341f21",
            "initiatedAt": "2024-03-12T07:06:11.562Z",
            "completedAt": "2024-03-12T07:14:10.412Z",
            "amount": "10.00",
            "fee": "0.25",
            "bearer": "merchant",
            "currency": "ZMW",
            "reference": "ref-1",
            "lencoReference": "240720004",
            "type": "mobile-money",
            "status": "successful",
            "source": "api",
            "reasonForFailure": None,
            "settlementStatus": "settled",
            "settlement": {
                "id": "c04583d7-d026-4dfa-b8b5-e96f17f93bb8",
                "amountSettled": "9.75",
                "currency": "ZMW",
                "createdAt": "2024-03-12T07:14:10.439Z",
                "settledAt": "2024-03-12T07:14:10.496Z",
                "status": "settled",
                "type": "instant",
                "accountId": "68f11209-451f-4a15-bfcd-d916eb8b09f4"
            },
            "mobileMoneyDetails": {
                "country": "zm",
                "phone": "0977433571",
                "operator": "airtel",
                "accountName": "Beata Jean"
            },
            "bankAccountDetails": None,
            "cardDetails": None
        }
    }
    


def get_paid_with_lenco(public_key, secret_key, email, amount, currency="ZMW", channels=["card", "mobile-money"], first_name="John", last_name="Doe", phone="0971111111"):
    """
    Simulates a Lenco payment process (client-side and server-side verification).

    Note: This is a simplified simulation. In a real application, you would handle
    the client-side interaction using JavaScript and then verify the payment on your
    server. This Python script demonstrates the server-side verification part.

    Args:
        public_key (str): Your Lenco public key.
        secret_key (str): Your Lenco secret key.
        email (str): The customer's email address.
        amount (int): The amount the customer is to pay.
        currency (str): The currency (default: "ZMW").
        channels (list): Payment channels (default: ["card", "mobile-money"]).
        first_name (str): Customer's first name.
        last_name (str): Customer's last name.
        phone (str): Customer's phone number.
    """
    reference = f"ref-{int(time.time() * 1000)}"  # Generate a unique reference

    # Simulate client-side payment initiation (in real app, this is JS)
    print(f"Simulating payment initiation with reference: {reference}")

    # Simulate successful payment (in real app, this would come from Lenco's callback)
    print("Simulating successful payment...")

    # Simulate server-side verification using Lenco API (replace with actual Lenco API endpoint)
    verification_url = "https://api.lenco.co/v1/payments/verify"  # Replace with actual Lenco API endpoint

    payload = {
        "reference": reference,
    }

    # Generate signature (replace with actual Lenco signature generation)
    message = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    signature = hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).hexdigest()

    headers = {
        "Authorization": f"Bearer {public_key}", #Or your secret key, depending on endpoint.
        "Content-Type": "application/json",
        "Lenco-Signature": signature,
    }

    try:
        response = requests.post(verification_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        verification_data = response.json()

        if verification_data.get("status") == "success": #Example of how a success might be returned.
            print("Payment verification successful!")
            print(f"Verification data: {verification_data}")
            # Process successful payment (e.g., update database, send confirmation email)
        else:
            print("Payment verification failed.")
            print(f"Verification data: {verification_data}")

    except requests.exceptions.RequestException as e:
        print(f"Error during payment verification: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response from Lenco API.")

def run():
    # Example usage (replace with your actual keys and customer data)
    public_key = "YOUR_PUBLIC_KEY" #replace with your public key
    secret_key = "YOUR_SECRET_KEY" #replace with your secret key
    customer_email = "customer@email.com"
    payment_amount = 1000

    get_paid_with_lenco(public_key, secret_key, customer_email, payment_amount)