import asyncio
import time
import httpx
from app.config import settings


URL = "http://localhost:8000/api/v1/predict"

HEADERS = {"X-API-Key": settings.API_KEY}

PAYLOAD = {
    
    "sepal_length": 5.9,
    "sepal_width": 3.0,
    "petal_length": 4.2,
    "petal_width": 1.5,
}

TOTAL_REQUESTS = 100

async def send_request(client, number):

    start_time = time.perf_counter()

    try:

        response = await client.post(URL,json=PAYLOAD,headers=HEADERS)

        duration = time.perf_counter() - start_time

        return {
            
            "request": number,
            "status": response.status_code,
            "duration": duration,
            "success": response.status_code == 200,
        }

    except Exception as error:

        duration = time.perf_counter() - start_time

        return {
            
            "request": number,
            "status": None,
            "duration": duration,
            "success": False,
            "error": str(error),
        }


async def main():

    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:

        tasks = [send_request(client, number) for number in range(1, TOTAL_REQUESTS + 1)]

        overall_start = time.perf_counter()

        results = await asyncio.gather(*tasks)

        overall_duration = time.perf_counter() - overall_start

    successful = sum(1 for result in results if result["success"])

    failed = TOTAL_REQUESTS - successful

    average_duration = sum(result["duration"] for result in results) / TOTAL_REQUESTS

    fastest = min(result["duration"] for result in results)

    slowest = max(result["duration"] for result in results)

    print()
    print("LOAD TEST RESULTS")
    print("-----------------")
    print(f"Total requests       : {TOTAL_REQUESTS}")
    print(f"Successful requests  : {successful}")
    print(f"Failed requests      : {failed}")
    print(f"Total test time      : {overall_duration:.4f} seconds")
    print(f"Average response time: {average_duration:.4f} seconds")
    print(f"Fastest response     : {fastest:.4f} seconds")
    print(f"Slowest response     : {slowest:.4f} seconds")


asyncio.run(main())