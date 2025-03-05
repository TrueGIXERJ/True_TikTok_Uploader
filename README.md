# True_Tiktok_Uploader
A Python-based automation tool for uploading videos to TikTok using Selenium.

This project lets you upload a chosen video with a customisable description by using your browser cookies - meaning no input on the browser whatsoever.

A lot of this work is based on [this tiktok-uploader](https://github.com/wkaisertexas/tiktok-uploader) which is currently non-functional.

## Features
* Automated TikTok video uploads
* Support for multiple video formats (`.mp4`, `.mov`, `.avi`, and more)
* Customisable video description (caption) with support for #hashtags and @mentions
* Fully automated authentication using cookies (meaning no need for manual login!)
* Headless mode support for background execution

## Installation
### Requirements
* Python 3.12+ (probably compatible with older versions too tbh)
* Google Chrome
* Compatible version of the [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) (This should be automatically installed with Chrome)

### Actually Installing
This package is available on PyPI, and can be installed by running:

`pip install True-Tiktok-Uploader`

Alternatively, it can be manually installed by cloning the git repository:

`git clone https://github.com/TrueGIXERJ/True_Tiktok_Uploader.git`

## Usage
The library revolves around the `upload_video` function which takes the file and caption and uploads to TikTok.

### Authentication
To upload a video, first you will need your browser cookies - this enables automatic authentication without a username & password, meaning the process is entirely hands free - as well as bypassing TikTok's regulation on authentication by Selenium controlled browsers.
Really, all you need is your `sessionid`, but for this usage we will use all of your cookies to trick TikTok into believing that the Selenium browser is a real person.

Use [Get cookies.txt](https://github.com/kairi003/Get-cookies.txt-LOCALLY) to export your browsing cookies.

After installing, open the extensions menu on TikTok.com and click `Get cookies.txt` to reveal your cookies. Select `Export As ⇩` and specify a name and location.

Then, pass the cookies to the `upload_video` function like so: `upload_video(..., cookies='cookies.txt')`

### Example Usage
```py
from True_Tiktok_Uploader.upload import upload_video  

upload_video(
    filename="video.mp4",
    description="Check out this cool new video! #fyp @truegixerj",
    cookies="cookies.txt",
    headless=False
)
```
A headless mode is also supported, enabling background operation, simply set `headless=True`. @Mentions and #Hashtags are supported, but you should verify that the user/hashtag exists.

## Licence
This project is licensed under the GNU General Public License v3.0. See the LICENCE file for details.

## Contribution and Questions
Contributions to the project are welcome with fixes and improvements - I will aim to keep on top of any updates to the TikTok platform, as UI updates could potentially break it. If you have any suggestions or improvements, feel free to submit a pull request or open an issue on GitHub. Or just come and shout at me loudly on my personal [Discord](https://discord.gg/zkhuwD5).