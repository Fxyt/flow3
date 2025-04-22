import asyncio
import aiohttp
import json
from loguru import logger

def printt(res):
    print(json.dumps(res,indent=4))

async def read_refresh_tokens(filename):
    with open(filename, 'r') as file:
        tokens = [line.strip() for line in file]
    return tokens

async def countdown(total_seconds):
    while total_seconds >= 0:
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        print(f"countdown {days:02}:{hours:02}:{minutes:02}:{seconds:02} seconds", end='\r')

        await asyncio.sleep(1)  # Ganti time.sleep dengan asyncio.sleep
        total_seconds -= 1

async def headers(method = 'get', token = None):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*'
    }
    if method == 'post':
        header['content-type'] = 'application/json'
    if token is not None:
        header['Authorization'] = f'Bearer {token}'
    return header

async def request_token(session,refresh_token):
    url = 'https://api2.flow3.tech/api/user/refresh'
    payload = {"refreshToken":refresh_token}
    async with session.post(url,headers=await headers('post'),json=payload) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            if req['result'] == 'success':
                access_token = req['data']['accessToken']
                return access_token
        except Exception as e:
            logger.error(f'Error: {e}')

async def poin(session,access_token):
    url = 'https://api2.flow3.tech/api/user/get-point-stats'
    async with session.get(url,headers=await headers('get',access_token)) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            point = req['data']['totalPointEarned']
            return point
        except Exception as e:
            logger.error(f'Error: {e}')

async def profile(session,access_token):
    url = 'https://api2.flow3.tech/api/user/profile'
    async with session.get(url,headers=await headers('get',access_token)) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            email = req['data']['email']
            return email
        except Exception as e:
            logger.error(f'Error: {e}')

async def ping(session,access_token):
    url = 'https://api2.flow3.tech/api/user/get-connection-quality'
    async with session.get(url,headers=await headers('get',access_token)) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            connection = req['data']
            return connection
        except Exception as e:
            logger.error(f'Error: {e}')

async def get_task(session,access_token):
    url = 'https://api2.flow3.tech/api/task/get-user-task'
    async with session.get(url,headers=await headers('get',access_token)) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            return req
        except Exception as e:
            logger.error(f'Error: {e}')

async def do_task(session,access_token,task_id,i):
    url = 'https://api2.flow3.tech/api/task/do-task'
    payload = {"taskId":task_id}
    async with session.post(url,headers=await headers('post',access_token),json=payload) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            if req['result'] == 'success':
                print(f'do_task {i}')
        except Exception as e:
            logger.error(f'Error: {e}')

async def claim_task(session,access_token,task_id,i):
    url = 'https://api2.flow3.tech/api/task/claim-task'
    payload = {"taskId":task_id}
    async with session.post(url,headers=await headers('post',access_token),json=payload) as res:
        try:
            req = await res.text()
            req = json.loads(req)
            if req['result'] == 'success':
                print(f'claim_task {i}')
        except Exception as e:
            logger.error(f'Error: {e}')

async def run_task(session,access_token,email):
    logger.info('============== check task =============')
    data_task = await get_task(session,access_token)
    data_task = data_task['data']
    for i, id_task in enumerate(data_task):
        i+=1
        task_id = id_task['_id']
        task_status = id_task['status']
        task_name = id_task['name']
        if task_status == 'idle':
            await do_task(session,access_token,task_id,i)
            await claim_task(session,access_token,task_id,i)
        elif task_status == 'claimed':
            print(f'email {email} task {task_name} claimed')
        else:
            print(f'email {email} task {task_name} done')

async def run():
    refresh_tokens = await read_refresh_tokens('token.txt')
    async with aiohttp.ClientSession() as session:
        for refresh_token in refresh_tokens:
            access_token = await request_token(session, refresh_token)
            if access_token:
                email = await profile(session, access_token)
                if email:
                    logger.info(f'email: {email} points: {await poin(session, access_token)}')
                    await run_task(session, access_token, email)

        logger.info('============== mining =============')
        while True:
            for refresh_token in refresh_tokens:
                access_token = await request_token(session, refresh_token)
                if access_token:
                    email = await profile(session, access_token)
                    if email:
                        logger.info(f'email: {email} ping: {await ping(session, access_token)} points: {await poin(session, access_token)}')
            await countdown(10)

asyncio.run(run())