from fastapi import APIRouter
from app.core.data_transformer import transform_data
from app.schemas.fusion_request import FusionRequest

router = APIRouter()

@router.post("/process")
def process_data(request: FusionRequest):
    result = transform_data(request.payload)
    return {
        "status": "processed",
        "data": result
    }