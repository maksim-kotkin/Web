import json
import bcrypt

from aiohttp import web
from models import init_orm , engine, Advertisement, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schema import  CreateAdvertisement, UpdateAdvertisement
from pydantic import ValidationError


app = web.Application()


async def orm_context(app):
    print('START')
    await init_orm()
    yield
    await engine.dispose()
    print("FINISH")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_http_error(error_cls, msg: str | dict | list):
    return error_cls(
        text=json.dumps(
            {"error": msg},
        ),
        content_type="application/json",
    )

def validate_json(json_data: dict, schema_cls: type[CreateAdvertisement] | type[UpdateAdvertisement]):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise get_http_error(web.HTTPNotFound, errors)
   
async def get_adv_by_id(adv_id: int, session: AsyncSession):
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise get_http_error(web.HTTPNotFound, "adv not found")
    return adv


async def add_adv(adv: Advertisement, session: AsyncSession) -> Advertisement:
    session.add(adv)
    try:
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, "adv already exists")
    return adv


class AdvertisementView(web.View):

    @property
    def adv_id(self):
        return int(self.request.match_info["adv_id"])

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get(self):
        adv = await get_adv_by_id(self.adv_id, self.session)
        return web.json_response(adv.json)

    async def post(self):
        adv_data = await self.request.json()
        json_data = validate_json(adv_data, CreateAdvertisement)
        adv = Advertisement(**adv_data)
        adv = await add_adv(adv, self.session)
        return web.json_response({"id": adv.id})

    async def patch(self):
        adv_data = await self.request.json()
        json_data = validate_json(adv_data, UpdateAdvertisement)
        adv = await get_adv_by_id(self.adv_id, self.session)
        for field, value in adv_data.items():
            setattr(adv, field, value)
        adv = await add_adv(adv, self.session)
        return web.json_response({"id": adv.id})

    async def delete(self):
        adv = await get_adv_by_id(self.adv_id, self.session)
        await self.session.delete(adv)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.post("/adv/", AdvertisementView),
        web.get("/adv/{adv_id:\d+}/", AdvertisementView),
        web.patch("/adv/{adv_id:\d+}/", AdvertisementView),
        web.delete("/adv/{adv_id:\d+}/", AdvertisementView),
    ]
)


web.run_app(app)