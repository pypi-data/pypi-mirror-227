class newHtmlObj(object):
    def __init__(self,htmlObj={"head":"<title>Hello world!</title>","body":"<h1>It's a HTML webpage!<body>"}):
        self.code="<!DOCTYPE html>\n<html>\n<head>\n"+htmlObj["head"]+"</head>\n<body>\n"+htmlObj["body"]+"</body>\n</html>"

def title(c):
    return("<title>%s</title>\n"%c)

def charset(t="utf-8"):
    return("<meta charset=\"%s\" />\n"%t)

def entities(t):
    return("&%s;"%t)

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
    return("<div>\n%s</div>\n"%c)

def span(c):
    return("<span>\n%s</span>\n"%c)

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

def audio(c,height=400,width=100,useControls=True):
    if useControls:
        return("<audio height=\"%d\" width=\"%d\" controls=\"controls\">\n%s</audio>\n"%(height,width,c))
    else:
        return("<audio height=\"%d\" width=\"%d\">\n%s</audio>\n"%(height,width,c))

def video(c,height=320,width=240,useControls=True):
    if useControls:
        return("<video height=\"%d\" width=\"%d\" controls=\"controls\">\n%s</video>\n"%(height,width,c))
    else:
        return("<video height=\"%d\" width=\"%d\">\n%s</video>\n"%(height,width,c))

def source(src,type="video",format="mp4"):
    return("<source src=\"%s\" type=\"%s/%s\" />\n"%(src,type,format))

def b(c):
    return("<b>%s</b>\n"%c)

def big(c):
    return("<big>%s</big>\n"%c)

def em(c):
    return("<em>%s</em>\n"%c)

def i(c):
    return("<i>%s</i>\n"%c)

def small(c):
    return("<small>%s</small>\n"%c)

def strong(c):
    return("<strong>%s</strong>\n"%c)

def sub(c):
    return("<sub>%s</sub>\n"%c)

def sup(c):
    return("<sup>%s</sup>\n"%c)

def ins(c):
    return("<ins>%s</ins>\n"%c)

def del_text(c):
    return("<del>%s</del>\n"%c)

def code(c):
    return("<code>%s</code>\n"%c)

def kbd(c):
    return("<kbd>%s</kbd>\n"%c)

def samp(c):
    return("<samp>%s</samp>\n"%c)

def tt(c):
    return("<tt>%s</tt>\n"%c)

def var(c):
    return("<var>%s</var>\n"%c)

def pre(c):
    return("<pre>\n%s</pre>\n"%c)

def abbr(c,title):
    return("<abbr title=\"%s\">%s</abbr>\n"%(title,c))

def address(c):
    return("<address>%s</address>\n"%c)

def bdo(c,dir):
    return("<bdo dir=\"%s\">%s</bdo>\n"%(dir,c))

def address(c):
    return("<address>%s</address>\n"%c)