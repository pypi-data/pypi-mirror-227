def colors(text="", color=None):
    properties = ""
    if color != None:
        color = color.replace("Red", "31").replace("Black","30").replace("Green", "32").replace("Yellow", "33").replace("Blue", "34").replace("Magenta", "35").replace("Cyan", "36").replace("White", "37").replace("Orange", " 208").replace("Purple", "128").replace("Gray","90")
        try:
            color = int(color)
        except:
            return f" * Invalid color code: [{color}]"
        if color >= 31 and color <= 37 or color == 90:
            properties += f"\033[{color}m"
        elif int(color) == 208:
            properties += f"\u001B[38;5;208m"
        elif int(color) == 128:
            properties += f"\u001B[38;5;{color}m"
        else:
            return f" * Invalid color code: [{color}]"
    
    equal = properties + text + "\033[0m"
    return equal
