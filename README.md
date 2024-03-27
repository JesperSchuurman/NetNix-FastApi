# NetNixApi
FastAPI REST API for a Netflix clone for a school project

# Prerequisites

First clone this repository and navigate to the project folder:
```bash
git clone https://github.com/JesperSchuurman/NetNix-FastApi && cd NetNix-FastApi
```

Python is required to run this program, you can download it [here](https://www.python.org/downloads/). After going through the installer you can install the requirements using the following command:
```bash
python3 -m pip install -r requirements
```

# Running the application

To start the application simply run the following:

```bash
python3 app.py
```

The API will by default run on port 80 (http://localhost/). You can run this command to see a list of options:
```bash
python3 app.py -h
```

The output would look like this:

```bash
$ python3 app.py -h
sage: app.py [-h] [--port PORT] [--ssl_key SSL_KEY] [--ssl_cert SSL_CERT]

options:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  The port to run the server on. Defaults to port 80.
  --ssl_key SSL_KEY, -k SSL_KEY
                        The path to an SSL key file.
  --ssl_cert SSL_CERT, -c SSL_CERT
                        The path to an SSL cert file
```

For example, if you want to run the application over HTTPS using LetsEncrypt, we can run the following command:

```bash
python3 app.py -p 443 -k "/etc/letsencrypt/live/example.com/privkey.pem" -c "/etc/letsencrypt/example.com/fullchain.pem"
```

# License

MIT License

Copyright (c) 2023 NHL Stenden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.