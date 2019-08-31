# multithread

Multithread is an optionally asynchronous Python library for downloading files using several threads.

# Features

* Lightweight: one file, a little over 100 lines of code excluding license
* Extensive: the ability to pass your own sessions and your own arguments to each request means you don't need to wait for your desired feature to be implemented; anything you can do in aiohttp, you can do in multithread!
* Fast: benefit from the speed of aiohttp and multithreaded downloading!

# Installation

Requirements:

* Python 3.5.3+
* aiohttp
* mosquito/aiofile
* optional: tqdm

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install multithread.  
For support for progress bars, install multithread[progress].

```bash
pip3 install multithread
```

# Usage

```python
import multithread

download_object = multithread.Download("http://url.com/file", filename)
download_object.start()

# passing headers (you can pass any other arguments that aiohttp.ClientSession.request can take as well)
download_object = multithread.Download("http://url.com/file", filename, aiohttp_args={"headers": {"a": "b", "c": "d"}})
download_object.start()
```

# Documentation

## Downloader
```python
Downloader(self, url, file, threads=4, session=None, progress_bar=True, aiohttp_args={'method': 'GET'}, create_dir=True)
```

A multi-threaded downloader class using aiohttp

Attributes:

    - url (str): The URL to download
    - file (str, path-like object or AIOFile): The file to write the download to. if not an AIOFile, it's used as a path for one
    - threads (int): The number of threads to use to download
    - session (aiohttp.ClientSession): An existing session to use with aiohttp
    - new_session (bool): True if a session was not passed, and the downloader created a new one
    - progress_bar (bool): Whether to output a progress bar or not
    - aiohttp_args (dict): Arguments to be passed in each aiohttp request. If you supply a Range header using this, it will be overwritten in fetch()

## start
```python
Downloader.start(self)
```
Calls asyncstart() synchronously
## asyncstart
```python
Downloader.asyncstart(self)
```
Re-initializes file and calls download() with it. Closes session if necessary
## fetch
```python
Downloader.fetch(self, fileobj, progress=False, filerange=(0, ''))
```
Individual thread for fetching files.

Parameters:

    - fileobj (AIOFile): the file to write the download to
    - progress (bool or tqdm.Progress): the progress bar (or lack thereof) to update
    - filerange (tuple): the range of the file to get

## download
```python
Downloader.download(self, fileobj)
```
Generates ranges and calls fetch() with them.

Parameters:

    - fileobj (AIOFile): the file to write the download to

# Contributing
Any and all pull requests are welcome. As this is a small project, there are no strict standards, but please try to keep your code clean to a reasonable standard. Alternatively, if you would like to clean *my* code, that would be more than welcome!

# License
[MIT](https://choosealicense.com/licenses/mit/)