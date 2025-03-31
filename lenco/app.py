import requests
import time
import hashlib
import hmac
import json
import frappe
from frappe import _
from frappe.utils.password import get_decrypted_password

def get_settings():
    """
    Retrieve the Lenco Settings document.

    Returns:
        frappe.Document: The "Lenco Settings" document containing all settings fields.
    """
    return frappe.get_cached_doc("Lenco Settings", "Lenco Settings")

def get_keys(settings):
    """
    Retrieve the decrypted API keys from the Lenco Settings.

    Args:
        settings (frappe.Document): The "Lenco Settings" document.

    Returns:
        dict: A dictionary containing 'public_key' and 'secret_key' with their decrypted values.

    Raises:
        frappe.ValidationError: If required keys are not found.
    """

    keys = {}
    public_key = get_decrypted_password("Lenco Settings", "Lenco Settings", "api_public_key", False)
    secret_key = get_decrypted_password("Lenco Settings", "Lenco Settings", "api_secret", False)
    if public_key:
        pass
    else:
        public_key = None

    if secret_key:
        pass
    else:
        secret_key = None

    # Validate that the secret key is present (required for API calls)
    if not secret_key:
        frappe.throw(_("API secret key not configured in Lenco Settings."))

    return {
        'public_key': public_key,
        'secret_key': secret_key
    }

@frappe.whitelist()
def check_transaction_state(reference="ref-adam-dawoodjee-21032025092553", transaction=None):
    # url = f"https://api.lenco.co/access/v2/collections/status/{reference}"

    # headers = {
    #     "accept": "application/json",
    #     "Authorization": "Bearer xo+CAiijrIy9XvZCYyhjrv0fpSAL6CfU8CgA+up1NXqK"
    # }

    # response = requests.get(url, headers=headers)

    # print(response.text)
    # return
    """
    Check the state of a transaction using the Lenco API.

    Args:
        reference (str): The transaction reference to check.
        transaction (str, optional): Additional transaction identifier (e.g., for logging or context).

    Returns:
        dict: A dictionary containing transaction details if successful, or an error message if failed.

    Raises:
        frappe.ValidationError: If the reference is invalid or settings cannot be retrieved.
    """

    reference = "ref-adam-dawoodjee-21032025100401"
    # Validate the reference
    if not reference or not isinstance(reference, str) or reference.strip() == "":
        return {"error": _("Invalid transaction reference provided.")}

    # Retrieve settings and keys
    try:
        settings = get_settings()
        keys = get_keys(settings)
        api_secret_key = keys["secret_key"]
    except Exception as e:
        return {"error": _("Failed to retrieve Lenco settings: {0}").format(str(e))}

    # Determine the API endpoint based on sandbox mode
    if settings.sandbox == 1:
        url = f"https://sandbox.lenco.co/access/v2/collections/status/{reference}"
        url = "https://sandbox.lenco.co/access/v2/collections?page=1"
    else:
        url = f"https://api.lenco.co/access/v2/collections/status/{reference}"

    headers = {"Authorization": f"Bearer {api_secret_key}"}

    print(url, api_secret_key)

    try:
        # Make the API request
        response = requests.get(url, headers=headers, timeout=10)  # Added timeout for reliability
        response.raise_for_status()  # Raises an exception for 4xx/5xx status codes

        # Parse the JSON response
        data = response.json()

        # Check if the API call was successful based on the 'status' field
        if data.get("status", False):
            transaction_data = data["data"]
            print(transaction_data)
            return transaction_data
            result = {
                "status": transaction_data.get("status", "unknown"),
                "amount": transaction_data.get("amount", "0.00"),
                "currency": transaction_data.get("currency", "ZMW"),
                "settlement_status": transaction_data.get("settlementStatus", "unknown"),
                "reference": transaction_data.get("reference", ""),
                "lenco_reference": transaction_data.get("lencoReference", ""),
                "type": transaction_data.get("type", ""),
                "source": transaction_data.get("source", ""),
                "reason_for_failure": transaction_data.get("reasonForFailure", None),
                "mobile_money_details": transaction_data.get("mobileMoneyDetails", {}),
                "bank_account_details": transaction_data.get("bankAccountDetails", {}),
                "card_details": transaction_data.get("cardDetails", {})
            }
            # Optionally log the transaction if provided
            if transaction:
                result["transaction"] = transaction
            return result
        else:
            return {"error": data.get("message", "Unknown error from API")}

    except requests.exceptions.HTTPError as e:
        # Handle specific HTTP errors
        status_code = e.response.status_code
        if status_code == 404:
            return {"error": "Transaction not found"}
        elif status_code == 401:
            return {"error": "Unauthorized: Invalid API key"}
        elif status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"HTTP error {status_code}: {e.response.text}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please check your network connection."}
    except requests.exceptions.RequestException as e:
        # Handle other network-related errors
        return {"error": f"Network error: {str(e)}"}
    except ValueError:
        # Handle JSON parsing errors
        return {"error": "Invalid response format from API"}



def get_payment_status(data):
    # return *args
    # print("data", data)
    return

def request(doc=None, method=None):
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