def colors(text="", color=None):
    properties = ""
    if color != None:
        try:
            color = color.replace("Red", "41").replace("Black","40").replace("Green", "42").replace("Yellow", "43").replace("Blue", "44").replace("Magenta", "45").replace("Cyan", "46").replace("Gray", "100").replace("Orange", " 208").replace("Purple", "128")
        except:
            pass
        try:
            color = int(color)
        except:
            return f" * Invalid color code: [{color}]"
        if color >= 41 and color <= 47 or color == 100:
            properties += f"\033[{color}m"
        elif int(color) == 208:
            properties += f"\u001B[48;5;208m"
        elif int(color) == 128:
            properties += f"\u001B[48;5;{color}m"
        else:
            return f" * Invalid color code: [{color}]"
    
    equal = properties + text + "\033[0m"
    return equal

