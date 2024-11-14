import asyncio
import aiohttp

async def main():
    
    async with aiohttp.ClientSession() as session:
        
        # response = await session.post(
        #     "http://0.0.0.0:8080/user/",
        #     json={'name': 'user_1', 'password': '1234'},
        #     )
            
#         response = await session.post(
#             "http://0.0.0.0:8080/adv/",
#             json={'owner': 'user_2', 'title': 'guhreouhgoyik[r]frgijp','description': 'pf[sfyiookg][[]'
#                   },
                                                
# )
        response = await session.patch(
            "http://0.0.0.0:8080/adv/1/",
            json={'title': 'guhreouhgofrgijp'},
        )
        

        # response = await session.delete(
        #     "http://0.0.0.0:8080/user/1/",
        # )
        

        # response = await session.get(
        #     "http://0.0.0.0:8080/adv/3/",
        # )
        print(response.status)
        print(await response.text())

asyncio.run(main())