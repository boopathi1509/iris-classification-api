import asyncio
import time
import httpx

URL = "http://127.0.0.1:8000/api/v1/predict"
API_KEY = "my-secret-api-key-123"

payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

async def send_request(client):
    start = time.perf_counter()

    response = await client.post(
        URL,
        json=payload,
        headers={"x-api-key": API_KEY}
    )

    elapsed = time.perf_counter() - start
    return response.status_code, elapsed

async def main():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()

        results = await asyncio.gather(
            *[send_request(client) for _ in range(50)]
        )

        total_time = time.perf_counter() - start

    success = sum(1 for status, _ in results if status == 200)
    failed = len(results) - success
    avg_time = sum(t for _, t in results) / len(results)

    print(f"Total requests: {len(results)}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print(f"Average response time: {avg_time:.4f} seconds")
    print(f"Total test time: {total_time:.4f} seconds")

asyncio.run(main())