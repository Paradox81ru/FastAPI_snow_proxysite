import random
import re

import uvicorn
from fastapi import FastAPI

from proxy_site_middleware import ProxySiteMiddleware

app = FastAPI()

def snow_content_correct(content: str):
    """ Снежное содержимое сайта. """
    symbols = '❄❅❆☃'

    def repl(x):
        result = list(f"{x[0]}")
        result.insert(1, f"<strong>{random.choice(symbols)}</strong>")
        return "".join(result)

    content = re.sub(r"[\w\d>]([.,])(\s|$|\"|\n|<)", repl, content)
    return content

app.add_middleware(ProxySiteMiddleware, site_url='https://fastapi.tiangolo.com', content_correct=snow_content_correct)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)