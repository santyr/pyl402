import httpx
from .wallet import Wallet, PaymentResult

class LNbitsPaymentResponse:
    def __init__(self, amount, description, destination, fee, payment_hash, payment_preimage, payment_request):
        self.amount = amount
        self.description = description
        self.destination = destination
        self.fee = fee
        self.payment_hash = payment_hash
        self.payment_preimage = payment_preimage
        self.payment_request = payment_request

class LNbitsWallet(Wallet):
    def __init__(self, api_key: str, client: httpx.Client = None):
        self.base_url = "https://lnb.bolverker.com/api/v1/payments"  # Adjust this URL to your LNbits instance
        self.credentials = api_key
        self.client = client if client else httpx.Client()

    def pay_invoice(self, invoice: str) -> PaymentResult:
        url = f"{self.base_url}/api/v1/payments"  # Update the endpoint according to LNbits API for invoice payments
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Api-Key': self.credentials,  # LNbits uses an API key for authentication
            'User-Agent': 'lnbits-python'
        }
        body = {
            "invoice": invoice  # Include "amount" if necessary
        }

        try:
            response = self.client.post(url, json=body, headers=headers)
            response.raise_for_status()  # Check for HTTP request errors

            lnbits_response = response.json()
            return PaymentResult(preimage=lnbits_response.get('preimage', ''),
                                 success=True)
        except httpx.HTTPStatusError as e:
            return PaymentResult(preimage='', success=False, error=f'HTTP error: {e.response.status_code} {e.response.reason_phrase}')
        except httpx.RequestError as e:
            return PaymentResult(preimage='', success=False, error=f'Request error: {str(e)}')
        except ValueError:
            return PaymentResult(preimage='', success=False, error='Failed to decode JSON')

# Example usage:
# if __name__ == "__main__":
#     wallet = LNbitsWallet("your_invoice_key_here")
#     invoice = "example_invoice"
#     result = wallet.pay_invoice(invoice)
#     if result.success:
#         print("Payment succeeded:", result.preimage)
#     else:
#         print("Error:", result.error)
