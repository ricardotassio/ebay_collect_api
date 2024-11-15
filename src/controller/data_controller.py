from fastapi import APIRouter, HTTPException

from src.schema import CollectDataResponse

from src.service.data_service import (
    christmas_categories,
    get_all_christmas_data,
    get_christmas_data,
)

router = APIRouter()


@router.get('/categories')
async def get_categories():
    return christmas_categories


@router.get('/collect-data', response_model=CollectDataResponse)
async def fetch_data():
    result = get_all_christmas_data()
    if result['status'] == 'error':
        raise HTTPException(status_code=500, detail='Data collection failed')

    return result


@router.get('/collect-data/{category_name}')
async def collect_data(category_name: str):
    category_id = christmas_categories.get(category_name)
    if not category_id:
        raise HTTPException(status_code=404, detail='Category not found')

    result = get_christmas_data(category_id)
    if result['status'] == 'error':
        raise HTTPException(status_code=500, detail='Data collection failed')

    return result
