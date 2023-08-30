import time

class Animation:
    keys = {
       "1": ["|", "/", "-", "\\"],
       "timer": [1,2,3,4,6,7,9]
    }
    @classmethod
    def Add(cls, name, key):
        if not isinstance(key, list):
            print("only a list must be allowed")
            return
        cls.keys[name] = key
        
    @classmethod
    def start(cls, text="", speed=0.1, key="", align="First", loop=1):
        try:
            key = cls.keys[key]
        except:
            print(" * \033[31mError: invalid key ({key})")
        for l in range(int(loop)):
            for k in key:
                if align == "Last":
                    print(f"\r{k}{text}", end="", flush=True)
                elif align == "First":
                    print(f"\r{text}{k}", end="", flush=True)
                time.sleep(speed)




