from .Text.colors import colors
import time


def TexHL(text, Hlc="White", color="Gray", second=0.5):
    v = ""
    for i in range(len(text)+1):
        print(f'\r{colors(text=v,color=Hlc)}{colors(text=text, color=color)}',end="", flush=True)
        try:
            v += text[0]
            text = text[1:]
            time.sleep(second)
        except:
            print()



