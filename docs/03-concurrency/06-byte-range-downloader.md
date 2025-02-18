# Byte-Range downloader code

- This code was written by [BhimRaj Yadav](https://github.com/bhimrazy/fastdownloader/blob/main/byte_range_download.py).
- It's a great example of how to use `semaphore`, `asyncio` and `aiohttp` to download files much faster.

```python
import asyncio
import aiohttp
import time
from aiohttp import ClientSession
from typing import Dict, Optional
from tqdm import tqdm
import random


async def download_chunk(
    session: ClientSession,
    url: str,
    start: int,
    stop: int,
    headers: Dict[str, str],
    buffer: bytearray,
    progress_bar: tqdm,
    retries: int = 3,
):
    """Download a specific chunk of the file and write it to the correct position in the buffer."""
    # Make a local copy of headers so that each call has its own header dict
    local_headers = headers.copy()
    local_headers.update({"Range": f"bytes={start}-{stop}"})

    attempt = 0
    while attempt < retries:
        try:
            # print(f"Downloading chunk {start}-{stop}")
            async with session.get(url, headers=local_headers) as response:
                if response.status != 206:  # 206 Partial Content is expected
                    raise Exception(
                        f"Failed to download chunk {start}-{stop}: HTTP {response.status}"
                    )
                content = await response.read()
                # Write the downloaded content into the buffer at the correct offset
                buffer[start : start + len(content)] = content

            # Update progress bar by the number of bytes expected for this chunk.
            # (Note: the final chunk might be a bit smaller, but that's fine.)
            progress_bar.update(stop - start + 1)
            return  # Successful download; exit the loop
        except Exception as e:
            print(f"Error downloading chunk {start}-{stop}: {e}")
            attempt += 1
            if attempt < retries:
                wait_time = random.uniform(1, 3)
                print(f"Retrying chunk {start}-{stop} in {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(
                    f"Failed to download chunk {start}-{stop} after {retries} retries."
                )
                raise e


async def download_file(
    url: str,
    filename: str,
    chunk_size: int,
    max_connections: int,
    headers: Optional[Dict[str, str]] = None,
):
    """Download a file in parallel chunks using asyncio and aiohttp, storing data in a preallocated bytearray."""
    headers = headers or {}

    # Get total file size (handling redirects if necessary)
    async with aiohttp.ClientSession() as session:
        async with session.head(url, headers=headers) as response:
            if response.status == 302:
                location = response.headers.get("Location")
                if location:
                    # print(f"Redirecting to {location}")
                    url = location
                    async with session.head(url, headers=headers) as new_response:
                        if new_response.status != 200:
                            raise Exception(
                                f"Failed to get file info: HTTP {new_response.status}"
                            )
                        content_length = int(
                            new_response.headers.get("Content-Length", 0)
                        )
                else:
                    raise Exception(
                        f"Failed to get file info: HTTP {response.status} - No Location header found."
                    )
            elif response.status == 200:
                content_length = int(response.headers.get("Content-Length", 0))
            else:
                raise Exception(f"Failed to get file info: HTTP {response.status}")

    print(f"Total file size: {content_length} bytes")

    # Preallocate a bytearray for the file
    buffer = bytearray(content_length)

    with tqdm(
        total=content_length, unit="B", unit_scale=True, desc=filename
    ) as progress_bar:
        tasks = []
        semaphore = asyncio.Semaphore(max_connections)

        async with aiohttp.ClientSession() as session:
            for start in range(0, content_length, chunk_size):
                stop = min(start + chunk_size - 1, content_length - 1)
                # print(f"Chunk {start}-{stop} will be downloaded.")

                # Capture start and stop in the local scope of the task.
                async def limited_download(start=start, stop=stop):
                    async with semaphore:
                        await download_chunk(
                            session, url, start, stop, headers, buffer, progress_bar
                        )

                tasks.append(asyncio.create_task(limited_download()))

            await asyncio.gather(*tasks)

        # After downloading all chunks, write the complete buffer to file.
        with open(filename, "wb") as f:
            f.write(buffer)


# Example usage:
if __name__ == "__main__":
    url = "https://huggingface.co/microsoft/OmniParser-v2.0/resolve/main/icon_caption/model.safetensors"
    filename = "model-byte-range.safetensors"
    chunk_size = 1024 * 1024 * 1  # 1 MB chunks
    max_connections = 16  # Limit parallel connections
    print(
        f"Downloading with {max_connections} connections and chunk size of {chunk_size} bytes"
    )

    start_time = time.time()
    asyncio.run(download_file(url, filename, chunk_size, max_connections))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Download completed in {elapsed_time:.2f} seconds.")
```
