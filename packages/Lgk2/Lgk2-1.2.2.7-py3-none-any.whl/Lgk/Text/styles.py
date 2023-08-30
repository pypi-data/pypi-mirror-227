def styles(text="", styles=None):
    properties = ""
    if styles is not None:
        styles = styles.replace("Bold", "1").replace("Italic", "3")
        try:
            styles = int(styles)
        except:
            return f" * \033[31mInvalid style code: ({styles}) not found\033[m"
        if styles >= 1 and styles <= 10:
            properties += f"\033[{styles}m"
        else:
            return f" * \033[31mInvalid style code: ({styles}) not found\033[m"
    
    text = properties + text + "\033[0m"
    return text

