def compare(value, In="", equal="", rtype="true"):
    rv = None
    for v in value:
        if v in In and In != "":
            rv = v
        elif v == equal and equal != "":
            rv = v
    
    if rtype == "true" and rv != None:
        return True
    elif rv == None:
        return rv
    elif rtype == "value":
        return rv


def WithFirstWord(args, w):
    args = args.split(" ")
    for i in args:
        if i == w: return True
    return False

