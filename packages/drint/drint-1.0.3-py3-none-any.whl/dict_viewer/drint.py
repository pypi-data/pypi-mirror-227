
def dict_msg(i: int = 0, indent: int = 4, d: dict = None, msg: str = "") -> str:
    
    for dict_key, dict_value in zip(d.keys(), d.values()):
        if type(dict_value) is not dict:
            msg = msg + " "*(indent*(i+1)) + f"\"{dict_key}\": {dict_value}" + "\n"
        else:
            add_msg = dict_msg(i=i+1, indent=indent, d=dict_value, msg="{\n")
            msg = msg + " "*(indent*(i+1)) + f"\"{dict_key}\": {add_msg}"+ " "*(indent*(i+1)) + "}" + "\n"
    return msg


def drint(dict: dict = None, indent: int = 4):
    msg = ""
    i = 0
    print("\n")
    msg = msg + " "*(indent*i) + "{" + "\n"
    msg = dict_msg(i=i, indent=indent, msg=msg, d=dict)
    msg = msg + " "*(indent*i) + "}" + "\n"
    print(msg)
    

