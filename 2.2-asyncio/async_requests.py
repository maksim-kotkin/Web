import asyncio
import aiohttp
import datetime
import more_itertools
from models import SessionDB, init_orm, SwapiPeople

MAX_REQUESTS = 5

async def get_people(person_id, session):
    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    if response.status == 200:
        json_data = await response.json()
        for field_name in ['films', 'species', 'starships', 'vehicles']:
            if field_name in json_data:
                json_data[field_name]= ','.join(json_data[field_name])
        return json_data
    else:
        print(f'Ошибка:{response.status}')
        return None


async def insert_people(people_list):
    async with SessionDB() as session:
        orm_model_list = [SwapiPeople(
            birth_year=people_dict['birth_year'],
            eye_color=people_dict['eye_color'],
            films=people_dict['films'],
            gender=people_dict['gender'],
            hair_color=people_dict['hair_color'],
            height=people_dict['height'],
            homeworld=people_dict['homeworld'],
            mass=people_dict['mass'],
            name=people_dict['name'],
            skin_color=people_dict['skin_color'],
            species=people_dict['species'],
            starships=people_dict['starships'],
            vehicles=people_dict['vehicles']
            ) for people_dict in people_list if people_dict ]
        session.add_all(orm_model_list)
        await session.commit()
    


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session_http:
        coros = (get_people(i, session_http) for i in range(1, 88))
        for coros_chunk in more_itertools.chunked(coros, 5):
            people_list = await asyncio.gather(*coros_chunk)
            asyncio.create_task (insert_people(people_list))
    
        tasks = asyncio.all_tasks()
        main_task = asyncio.current_task()
        tasks.remove(main_task)
        await asyncio.gather(*tasks)

start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)