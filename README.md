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
* Tinche/aiofiles
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

# Downloader
```python
Downloader(self, url, file, threads=4, session=None, progress_bar=True, aiohttp_args={'method': 'GET'}, create_dir=True)
```

An optionally asynchronous multi-threaded downloader class using aiohttp

Attributes:

    - url (str): The URL to download
    - file (str or path-like object): The filename to write the download to.
    - threads (int): The number of threads to use to download
    - session (aiohttp.ClientSession): An existing session to use with aiohttp
    - new_session (bool): True if a session was not passed, and the downloader created a new one
    - progress_bar (bool): Whether to output a progress bar or not
    - aiohttp_args (dict): Arguments to be passed in each aiohttp request. If you supply a Range header using this, it will be overwritten in fetch()

## \_\_init\_\_
```python
Downloader.__init__(self, url, file, threads=4, session=None, progress_bar=True, aiohttp_args={'method': 'GET'}, create_dir=True)
```
Assigns arguments to self for when asyncstart() or start() calls download.

All arguments are assigned directly to self except for:

    - session: if not passed, a ClientSession is created
    - aiohttp_args: if the key "method" does not exist, it is set to "GET"
    - create_dir: see parameter description

Parameters:

    - url (str): The URL to download
    - file (str or path-like object): The filename to write the download to.
    - threads (int): The number of threads to use to download
    - session (aiohttp.ClientSession): An existing session to use with aiohttp
    - progress_bar (bool): Whether to output a progress bar or not
    - aiohttp_args (dict): Arguments to be passed in each aiohttp request. If you supply a Range header using this, it will be overwritten in fetch()
    - create_dir (bool): If true, the directories encompassing the file will be created if they do not exist already.

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
Downloader.fetch(self, progress=False, filerange=(0, ''))
```
Individual thread for fetching files.

Parameters:

    - progress (bool or tqdm.Progress): the progress bar (or lack thereof) to update
    - filerange (tuple): the range of the file to get

## download
```python
Downloader.download(self)
```
Generates ranges and calls fetch() with them.


# Contributing
Any and all pull requests are welcome. As this is a small project, there are no strict standards, but please try to keep your code clean to a reasonable standard. Alternatively, if you would like to clean *my* code, that would be more than welcome!

# License
[MIT](https://choosealicense.com/licenses/mit/)