import uvicorn

from argparse import ArgumentParser
from dotenv import load_dotenv

load_dotenv()

from src import App

app = App("NetNix")

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--port", "-p", type=int, default=80, help="The port to run the server on. Defaults to port 80.")
    argparser.add_argument("--ssl_key", "-k", type=str, default=None, help="The path to an SSL key file.")
    argparser.add_argument("--ssl_cert", "-c", type=str, default=None, help="The path to an SSL cert file")
    args = argparser.parse_args()
    uvicorn.run("app:app", host="0.0.0.0", port=args.port, ssl_keyfile=args.ssl_key, ssl_certfile=args.ssl_cert)