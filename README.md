# article-tracking<!-- omit in toc -->

Python app using the Twilio Python API for WhatsApp, the `requests` package for
Telegram and the Heroku Python script hosting solution to send WhatsApp and
Telegram messages on a weekly basis to inform the user about the availability of certain online articles.

## Table of contents<!-- omit in toc -->

- [1. Description](#1-description)
- [2. Getting started](#2-getting-started)
  - [2.1 Dependencies](#21-dependencies)
  - [2.2 Installing](#22-installing)
  - [2.3 Executing program](#23-executing-program)
- [3. Version history](#3-version-history)

<!-- toc -->

## 1. Description

`article-tracking` is a Python app running on the Heroku web server that
makes use of the `selenium` Python package to scrape the web and check on a
weekly basis if a certain online articles are available online and in the store.
An update WhatsApp and Telegram message is sent every week to my phone. For each
article of interest specified by a specific URL, the message contains two pieces
of information:

- Its online availability
- Its availability in stores

## 2. Getting started

### 2.1 Dependencies

Concerning `article-tracking_test.py`:

- Tested on macOS Big Sur version 11.2.3
- Python 3.6

### 2.2 Installing

For testing `article-tracking_test.py`, install the required packages by typing
following Terminal command at the root of the project:

`pip install -r requirements.txt`

To deploy the `article-tracking` Python web app on the Heroku web server,
please refer to the instructions in the `_ApproachToHostOnHeroku.rtfd` file
situated in the `_Resources` folder or feel free to contact me with questions.

### 2.3 Executing program

The `article-tracking_test.py` test script can be run by typing following
command at the root of the project:

`python3.6 article-tracking_test.py`

Concerning the actual web app, once deployed, the app automatically and
continuously runs on the Heroku web server.

## 3. Version history

- 0.1
  - Initial release
