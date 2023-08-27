class newHtmlObj(object):
    def __init__(self,htmlObj={"head":"<title>Hello world!</title>","body":"<h1>It's a HTML webpage!<body>"}):
        self.code="<!DOCTYPE html>\n<html>\n<head>\n"+htmlObj["head"]+"</head>\n<body>\n"+htmlObj["body"]+"</body>\n</html>"

def title(c):
    return("<title>%s</title>\n"%c)

def h(c,l=1):
    return("<h%d>%s</h%d>\n"%(l,c,l))

def p(c):
    return("<p>"+c+"</p>\n")

def br():
    return("<br />\n")

def img(src,alt="An image"):
    return("<img src=\"%s\" alt=\"%s\" />\n"%(src,alt))
    
def a(c="",href="#"):
    return("<a href=%s>%s</a>\n"%(href,c))

def div(c):
    return("<div>%s</div>\n"%c)

def span(c):
    return("<span>%s</span>\n"%c)

def ul(c):
    return("<ul>\n%s</ul>\n"%c)

def ol(c):
    return("<ol>\n%s</ol>\n"%c)

def li(c):
    return("<li>%s</li>\n"%c)

def table(c,border=1):
    return("<table border=\"%d\">\n%s</table>\n"%(border,c))

def tr(c):
    return("<li>\n%s</li>\n"%c)

def td(c):
    return("<li>%s</li>\n"%c)