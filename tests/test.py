import random
import re

def content_correct(content):
    symbols = '❄❅❆☃'
    def repl(x):
        result = list(f"{x[0]}")
        result.insert(1, random.choice(symbols))
        return "".join(result)

    content = re.sub("[\w\d]([.,])(\s|$)",  repl, content)
    return content

def test_content_correct():
    txt = "One, two, three. Four fife six... Seven,eight, nine, ten."
    print(content_correct(txt))