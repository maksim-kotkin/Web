
from typing import List


import fastapi


import crud
import models
import schema
from lifespan import lifespan
from dependencies import SessionDependency
from constants import STATUS_SUCCESS_RESPONSE

app = fastapi.FastAPI(
    title='Test Application',
    version='0.0.1',
    description='...',
    lifespan=lifespan
)


@app.get("/v1/advertisement/{advertisement_id}", response_model=schema.GetAdvResponse)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement = await crud.get_item(session, models.Advertisement, advertisement_id)
    return advertisement.dict


@app.get("/v1/advertisement")
async def get_advertisement_qs(session: SessionDependency, title: str = None,
                        description: str = None, price: str = None, author: str = None):
    advertisement = await crud.get_item_qs(session, title, description, price, author)
    return advertisement


@app.post("/v1/advertisement", response_model=schema.CreateAdvResponse)
async def create_advertisement(advertisement_json: schema.CreateAdvRequest, session: SessionDependency):
    advertisement = models.Advertisement(**advertisement_json.dict())
    advertisement = await crud.add_item(session, advertisement)
    return advertisement.id_dict



@app.patch("/v1/advertisement/{advertisement_id}", response_model=schema.UpdateAdvResponse)
async def update_advertisement(
    advertisement_id: int, advertisement_json: schema.UpdateAdvRequest, session: SessionDependency
):

    advertisement = await crud.get_item(session, models.Advertisement, advertisement_id)
    advertisement_patch = advertisement_json.dict(exclude_unset=True)
    for field, value in advertisement_patch.items():
        setattr(advertisement, field, value)
    await crud.add_item(session, advertisement)
    return advertisement.id_dict

@app.delete("/v1/advertisement/{advertisement_id}", response_model=schema.DeleteAdvResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    await crud.delete_item(session, models.Advertisement, advertisement_id)
    return STATUS_SUCCESS_RESPONSE
