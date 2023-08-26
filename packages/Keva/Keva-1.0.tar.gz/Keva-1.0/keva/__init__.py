import requests

db_key = ""

UnknownError = Exception
DatabaseDoesNotExistError = Exception

def get(key):

    """
    Gets a key from your Keva database and returns it
    """

    url = "https://keva.pancakedev.repl.co/get/" + db_key + "/" + key

    r = requests.get(url)

    if "error" not in r.text:
        data = r.json()
        return data[key]
    else:
        info = r.json()
        match info["error"]:
            case "unknown": raise UnknownError('An unknown error has ocurred')
            case "database does not exist": raise DatabaseDoesNotExistError('The key you provided is not linked to any Keva Database')
            case "key does not exist": raise KeyError('The key you provided does not exist in your Keva database')

def get_entire():

    """
    Fetches your entire Keva database and returns it as a dictionary
    """

    url = "https://keva.pancakedev.repl.co/get_entire/" + db_key

    r = requests.get(url)
    if "error" not in r.text:
        return r.json()
    else:
        info = r.json()
        match info["error"]:
            case "unknown": raise UnknownError('An unknown error has ocurred')
            case "database does not exist": raise DatabaseDoesNotExistError('The key you provided is not linked to any Keva Database')

def get_keys():

    """
    Fetches all the keys of the key-value pairs of your Keva database
    """

    url = "https://keva.pancakedev.repl.co/get_keys/" + db_key

    r = requests.get(url)
    if "error" not in r.text:
        return r.json()
    else:
        info = r.json()
        match info["error"]:
            case "unknown": raise UnknownError('An unknown error has ocurred')
            case "database does not exist": raise DatabaseDoesNotExistError('The key you provided is not linked to any Keva Database')


def set(key, value):

    """
    Sets a key to a certain value in your keva database
    """

    key = str(key)

    value_type = "str"

    if type(value) == str:
        value_type = "str"
        value = str(value)
    elif type(value) == int:
        value_type = "int"
        value = str(value)
    elif type(value) == float:
        value_type = "float"
        value = str(value)
    elif type(value) == bool:
        value_type = "bool"
        value = str(value).lower()
    elif type(value) == dict:
        value_type = "dict"
        value = str(value)
    elif type(value) == list:
        value_type = "list"
        value = str(value)
    else:
        value_type = "str"
        value = str(value)

    value = value.replace("%", "%25")
    value = value.replace("&", "%26")
    value = value.replace("?", "%3F")

    url = "https://keva.pancakedev.repl.co/set/" + db_key + "/" + key + "/" + value + "/" + value_type
    
    r = requests.get(url)
    if "error" not in r.text:
        return True
    else:
        info = r.json()
        match info["error"]:
            case "unknown": raise UnknownError('An unknown error has ocurred')
            case "database does not exist": raise DatabaseDoesNotExistError('The key you provided is not linked to any Keva Database')
            
def delete(key):
   
    """
    Deletes a certain key out of your Keva database
    """

    url = "https://keva.pancakdev.repl.co/del/" + db_key + "/" + key
   
    r = requests.get(url)
    if "error" not in r.text:
        return True
    else:
        info = r.json()
        match info["error"]:
            case "unknown": raise UnknownError('An unknown error has ocurred')
            case "database does not exist": raise DatabaseDoesNotExistError('The key you provided is not linked to any Keva Database')
            case "key does not exist": raise KeyError('The key you provided does not exist in your Keva database')

def reset():

    """
    Resets your whole KEva database back to zero
    """

    url = "https://keva.pancakedev.repl.co/reset/" + db_key

    r = requests.get(url)
    if "error" not in r.text:
        return True
    else:
        info = r.json()
        match info["error"]:
            case "unknown": raise UnknownError('An unknown error has ocurred')
            case "database does not exist": raise DatabaseDoesNotExistError('The key you provided is not linked to any Keva Database')