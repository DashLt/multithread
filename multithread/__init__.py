"""An optionally asynchronous multi-threaded downloader module for Python."""
import asyncio
import aiohttp
from aiofile import AIOFile
from pathlib import Path

name = "multithread"

class Downloader:
    """
    An optionally asynchronous multi-threaded downloader class using aiohttp

    Attributes:
        - url (str): The URL to download
        - file (str, path-like object or AIOFile): The file to write the download to. if not an AIOFile, it's used as a path for one
        - threads (int): The number of threads to use to download
        - session (aiohttp.ClientSession): An existing session to use with aiohttp
        - new_session (bool): True if a session was not passed, and the downloader created a new one
        - progress_bar (bool): Whether to output a progress bar or not
        - aiohttp_args (dict): Arguments to be passed in each aiohttp request. If you supply a Range header using this, it will be overwritten in fetch()
    """
    def __init__(self, url, file, threads=4, session=None, progress_bar=True, aiohttp_args={"method": "GET"}, create_dir=True):
        """Assigns arguments to self for when asyncstart() or start() calls download.
        
        All arguments are assigned directly to self except for: 
            - file: if not passed, an AIOFile is reated with the path-like object supplied
            - session: if not passed, a ClientSession is created
            - aiohttp_args: if the key "method" does not exist, it is set to "GET"
            - create_dir: see parameter description
        
        Parameters:
            - url (str): The URL to download
            - file (str, path-like object or AIOFile): The file to write the download to. if not an AIOFile, it's used as a path for one
            - threads (int): The number of threads to use to download
            - session (aiohttp.ClientSession): An existing session to use with aiohttp
            - progress_bar (bool): Whether to output a progress bar or not
            - aiohttp_args (dict): Arguments to be passed in each aiohttp request. If you supply a Range header using this, it will be overwritten in fetch()
            - create_dir (bool): If true, the directories encompassing the file will be created if they do not exist already.
        """
        self.url = url
        if file is not AIOFile:
            if create_dir:
                parent_directory = Path(file).parent
                parent_directory.mkdir(parents=True, exist_ok=True)
            self.file = AIOFile(file, "wb")
        else:
            self.file = file
        self.threads = threads
        if not session:
            self.session = aiohttp.ClientSession()
            self.new_session = True
        else:
            self.session = session
            self.new_session = False
        self.progress_bar = progress_bar
        if "method" not in aiohttp_args:
            aiohttp_args["method"] = "GET"
        self.aiohttp_args = aiohttp_args
    
    def start(self):
        """Calls asyncstart() synchronously"""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.asyncstart())
    
    async def asyncstart(self):
        """Re-initializes file and calls download() with it. Closes session if necessary"""
        async with self.file as fileobj:
            await self.download(fileobj)
        if self.new_session:
            await self.session.close()

    async def fetch(self, fileobj, progress=False, filerange=(0,"")):
        """Individual thread for fetching files.

        Parameters:
            - fileobj (AIOFile): the file to write the download to
            - progress (bool or tqdm.Progress): the progress bar (or lack thereof) to update
            - filerange (tuple): the range of the file to get
        """
        if "headers" not in self.aiohttp_args:
            self.aiohttp_args["headers"] = dict()
        self.aiohttp_args["headers"]["Range"] = f"bytes={filerange[0]}-{filerange[1]}"
        async with self.session.request(url=self.url, **self.aiohttp_args) as filereq:
            offset = filerange[0]
            async for chunk in filereq.content.iter_any():
                if progress:
                    progress.update(len(chunk))
                await fileobj.write(chunk, offset=offset)
                offset += len(chunk)

    async def download(self, fileobj):
        """Generates ranges and calls fetch() with them.

        Parameters:
            fileobj (AIOFile): the file to write the download to"""
        temp_args = self.aiohttp_args.copy()
        temp_args["method"] = "HEAD"
        async with self.session.request(url=self.url, **temp_args) as head:
            length = int(head.headers["Content-Length"])
            start = -1
            base = int(length / self.threads)
            ranges = list()
            for counter in range(self.threads - 1):
                ranges.append((start + 1, start + base))
                start += base    
            ranges.append((start + 1, length))
            if self.progress_bar:
                from tqdm import tqdm
                with tqdm(total=length, unit_scale=True, unit="B") as progress:
                    await asyncio.gather(*[self.fetch(fileobj, progress, filerange) for filerange in ranges])
            else:
                await asyncio.gather(*[self.fetch(fileobj, False, filerange) for filerange in ranges])