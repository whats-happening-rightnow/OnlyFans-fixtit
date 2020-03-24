import uuid
import string
import datetime
import re

def fix_file_name(valid_results):
    
    for result in valid_results:
        result["title"] = str(uuid.uuid4())

    for result in valid_results:

        # fixed title
        titfix = title_fix(result["text"])

        # datetime string
        dttmstr = datetime.datetime.strptime(result["postedAt"], "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H-%M")
        result["dttmstr"] = dttmstr

        # file extension
        result["ext"] = result["filename"].split('.')[1]

        titfix = "" if titfix.strip() == "" else " - " + titfix.strip()
        newtitle = f"{result['author']} - {dttmstr}{titfix}"
        
        titfound = list(filter(lambda rsl: rsl['title'] == newtitle, valid_results))
        #result["idx"] = 1 if not titfound else titfound.sort(key=lambda x: x["idx"], reverse=True)[0]["idx"] + 1

        if not titfound: 
            result["idx"] = 1
        else: 
            titfound.sort(key=lambda x: x["idx"], reverse=True)
            result["idx"] = titfound[0]["idx"] + 1

        result["title"] = newtitle

    for result in valid_results:

        titfound = list(filter(lambda rsl: rsl['title'] == result['title'], valid_results))
        numoccr = len(titfound)
        
        zeropad = 1

        if numoccr > 9:
            zeropad = 2
        elif numoccr > 99:
            zeropad = 3
        elif numoccr > 999:
            zeropad = 4

        tit = result['title']
        newtitle = ""
        if numoccr > 1:
            newtitle = f"{tit} - {str(result['idx']).zfill(zeropad)}-{numoccr}.{result['ext']}"
        else:
            newtitle = f"{tit}.{result['ext']}"

        result["filename"] = newtitle

    return valid_results

def title_fix(tit):

    # strip out emoji tags
    TAG_RE = re.compile(r'<[^>]+>')
    tit = TAG_RE.sub('', tit)

    # strip out newline and tabs
    tit = tit.replace('\n', ' ')
    tit = tit.replace('\t', ' ').strip()

    # remove filesystem disallowed characters
    valid_chars = "!,-_.() %s%s" % (string.ascii_letters, string.digits)
    newtit = ''.join(c for c in tit if c in valid_chars)

    # truncate long titles
    if len(newtit) > 60:
        newtitarr = newtit.split(' ')
        newtit = ''

        ct = 0
        while len(newtit) < 60:
            newtit += newtitarr[ct] + ' '
            ct += 1

        newtit = newtit.strip() + '...'

    return newtit
