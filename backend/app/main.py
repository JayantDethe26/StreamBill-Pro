from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.organizations import router as organizations_router
from app.api.v1.subscription_plans import (
    router as plans_router
)

from app.api.v1.api_keys import (
    router as api_keys_router
)

from app.api.v1.products import (
    router as products_router
)

from app.api.v1.pricing_tiers import (
    router as pricing_tiers_router
)

from app.api.v1.events import (
    router as events_router
)

from app.api.v1.usage_summary import (
    router as usage_summary_router
)

from app.api.v1.invoices import (
    router as invoices_router
)

from app.api.v1.customers import (
    router as customers_router
)

from app.api.v1.payments import (
    router as payments_router
)

app = FastAPI(
    title="StreamBill Pro",
    version="1.0.0"
)

# Register Routers
app.include_router(auth_router)
app.include_router(organizations_router)
app.include_router(plans_router)
app.include_router(api_keys_router)
app.include_router(products_router)
app.include_router(pricing_tiers_router)
app.include_router(events_router)
app.include_router(usage_summary_router)
app.include_router(invoices_router)
app.include_router(customers_router)
app.include_router(payments_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to StreamBill Pro"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }