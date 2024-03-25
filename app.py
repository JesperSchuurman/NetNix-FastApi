import uvicorn

from argparse import ArgumentParser
from dotenv import load_dotenv

load_dotenv()

from src import App

app = App("NetNix")

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--port", "-p", type=int, default=80)
    args = argparser.parse_args()
    uvicorn.run("app:app", host="0.0.0.0", port=args.port)