from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Tip Calculator API")

CENT = Decimal("0.01")
WHOLE = Decimal("1")


class TipBase(str, Enum):
    pre_tax = "pre_tax"
    post_tax = "post_tax"


class RoundingMode(str, Enum):
    none = "none"
    nearest = "nearest"
    up = "up"
    down = "down"


class RoundTarget(str, Enum):
    total = "total"
    per_person = "per_person"


class TipRequest(BaseModel):
    bill: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    tip_percent: Decimal = Field(ge=0, le=100)
    tax_percent: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    people: int = Field(default=1, ge=1, le=100)
    tip_base: TipBase = TipBase.pre_tax
    rounding: RoundingMode = RoundingMode.none
    round_target: RoundTarget = RoundTarget.total


class TipResponse(BaseModel):
    subtotal: Decimal
    tax: Decimal
    tip: Decimal
    rounding_adjustment: Decimal
    total: Decimal
    people: int
    shares: list[Decimal]


def to_cents(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def round_to_whole(value: Decimal, mode: RoundingMode) -> Decimal:
    methods = {
        RoundingMode.nearest: ROUND_HALF_UP,
        RoundingMode.up: ROUND_CEILING,
        RoundingMode.down: ROUND_FLOOR,
    }
    return value.quantize(WHOLE, rounding=methods[mode])


def split_evenly(total: Decimal, people: int) -> list[Decimal]:
    total_cents = int(total * 100)
    base, remainder = divmod(total_cents, people)
    return [
        Decimal(base + (1 if i < remainder else 0)) / 100
        for i in range(people)
    ]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calculate", response_model=TipResponse)
def calculate(req: TipRequest) -> TipResponse:
    tax = to_cents(req.bill * req.tax_percent / 100)
    tip_basis = req.bill if req.tip_base == TipBase.pre_tax else req.bill + tax
    tip = to_cents(tip_basis * req.tip_percent / 100)
    raw_total = req.bill + tax + tip

    if req.rounding == RoundingMode.none:
        total = raw_total
    elif req.round_target == RoundTarget.total:
        total = round_to_whole(raw_total, req.rounding)
    else:
        per_person = round_to_whole(raw_total / req.people, req.rounding)
        total = per_person * req.people

    return TipResponse(
        subtotal=req.bill,
        tax=tax,
        tip=tip,
        rounding_adjustment=total - raw_total,
        total=total,
        people=req.people,
        shares=split_evenly(total, req.people),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)