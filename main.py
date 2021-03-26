import logging

import stripe
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


class Item(BaseModel):
    cost: int
    success_url: str
    cancel_url: str


@app.get("/stripe/hello/")
async def hello():
    return {"msg": "hello world"}


@app.post("/stripe/create-checkout-session/")
async def create_checkout_session(item: Item, response: Response):
    items = [{
        "price_data": {
            "currency": "rub",
            "unit_amount": item.cost,
            "product_data": {
                "name": "Something here",
            }
        },
        "quantity": 1
    }]
    try:
        checkout_session = stripe.checkout.Session.create(payment_method_types=['card'], line_items=items,
                                                          mode='payment',
                                                          success_url=item.success_url,
                                                          cancel_url=item.cancel_url, )
    except Exception as e:
        logging.error("create_checkout_session error: {}".format(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"err": e}
    return {'id': checkout_session.id}
