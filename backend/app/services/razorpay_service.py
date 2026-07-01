import razorpay
from fastapi import HTTPException
from app.core.config import settings


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


async def create_razorpay_order(
    amount: float,
    invoice_id: str
):
    """
    Creates a Razorpay Order.

    Parameters
    ----------
    amount : float
        Invoice amount in Rupees.

    invoice_id : str
        Internal StreamBill invoice id.
    """

    print(f"Invoice Amount (₹): {amount}")
    print(f"Sending to Razorpay (paise): {int(amount * 100)}")

    order = client.order.create(
        {
            "amount": int(amount * 100),   # Convert ₹ → paise
            "currency": "INR",
            "receipt": invoice_id,
            "payment_capture": 1
        }
    )

    return order


async def verify_payment_signature(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str
):
    """
    Verify the payment signature returned by Razorpay.
    """

    try:

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }
        )

        return True

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Payment signature verification failed."
        )