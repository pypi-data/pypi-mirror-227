class newHtmlObj():
    def __init__(self,htmlObj={"head":"<title>Hello world!</title>","body":"<h1>It's a HTML webpage!<body>"}):
        return("<DOCTYPE html>\n<html>\n<head>\n"+htmlObj["head"]+"\n</head>\n<body>\n"+htmlObj["body"]+"\n</body>\n</html>")

def title(c):
    return("<title>%s</title>")

def h(c,l=1):
    return("<h%d>"%(l)+c+"</h%d>"%(l))

def p(c):
    return("<p>"+c+"</p>")

def br():
    return("<br />")

def img(src,alt="An image"):
    return("<img src=\"%s\" alt=\"%s\" />"%(src,alt))

def a(c="",href="#"):
    return("<a href=%s>%s</a>"%(href,c))