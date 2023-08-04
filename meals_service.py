import re

NO_IMAGE_URL = 'https://placehold.co/600x400?text=No+Image'

def get_meal_image(txt):
    res = re.search(r"!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^\"])\")?\s*\)", txt)
    if res != None:
        return res.group(1)
    else:
        return NO_IMAGE_URL

def get_meal_title(txt: str):
    res = ''
    try:
        i = txt.index('!')
        res = txt[:i]
    except:
        res = txt.splitlines()[0]
    
    return res.strip()

def get_meal_description(txt: str):
    res = ''
    try:
        i = txt.index('**ingredients:**')
        res = txt[i:]
    except:
        pass    
    return res
    