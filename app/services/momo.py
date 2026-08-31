import base64
import httpx
import pybreaker
from app.core.config import settings

momo_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)

class MomoService:
    def __init__(self)->None:
        self.subscription_key = settings.MOMO_SUBSCRIPTION_KEY
        self.api_user = settings.MOMO_API_USER
        self.api_key = settings.MOMO_API_KEY
        self.env = settings.MOMO_ENVIRONMENT
        self.base_url = settings.MOMO_BASE_URL
        self.public_url = settings.PUBLIC_URL

    
    async def _get_access_token(self)->str:
        credentials = f"{self.api_user}:{self.api_key}"
        encoded_creds = base64.b64encode(credentials.encode()).decode()


        url = f"{self.base_url}/collection/token/"
        headers = {
            "Authorization":f"Basic {encoded_creds}",
            "Ocp-Apim-Subscription-Key":self.subscription_key,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(url, headers=headers)
            if res.status_code != 200:
                raise Exception(f"MoMo Auth Error ({res.status_code}):{res.text}")
            return res.json().get("access_token")


    @momo_breaker
    async def request_to_pay(
        self,
        phone_number:str,
        amount:float,
        reference_id:str
    )-> dict:
        token = await self._get_access_token()
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id":reference_id,
            "X-Target-Environment":self.env,
            "X-Callback-Url":f"{settings.PUBLIC_URL}/api/v1/payments/momo/callback",
            "Content-Type":"application/json",
            "Ocp-Apim-Subscription-Key":self.subscription_key
        }

        payload = {
            "amount":str(int(amount)),
            "currency": "EUR",
            "externalId": reference_id,
            "payer":{"partyIdType":"MSISDN", "partyId":phone_number},
            "payerMessage": "Ticket Payment",
            "payeeNote": "Event Ticketing"
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.post(url, json=payload, headers=headers)
            if res.status_code not in (200, 202):
                raise Exception(f"MoMo RequestToPay failed ({res.status_code}):{res.text}")
            return {"status":"PENDING", "reference_id":reference_id}