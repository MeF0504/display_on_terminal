BG = {'k':'\033[40m','w':'\033[47m','r':'\033[41m','g':'\033[42m','b':'\033[44m','m':'\033[45m','c':'\033[46m','y':'\033[43m'}
FG = {'k':'\033[30m','w':'\033[37m','r':'\033[31m','g':'\033[32m','b':'\033[34m','m':'\033[35m','c':'\033[36m','y':'\033[33m'}
END = '\033[0m'

def BG256(n):
    return '\033[48;5;%dm' % n

def FG256(n):
    return '\033[38;5;%dm' % n

def put(x,y,str,color):
    print '\033[%d;%dH%s%s%s' % (y,x,color,str,END)

def clear():
    print "\033[2J"

def getsize():
    import curses

    stdscr = curses.initscr()
    max_y,max_x = stdscr.getmaxyx()
    min_y,min_x = stdscr.getbegyx()
    curses.endwin()
    return (min_x,max_x),(min_y,max_y)

def setcolor(rgb,ctype='default'):
    ### ctype...{default or 256_colors} default...8colors(w,k,r,g,b,c,m,y)
    if len(rgb) == 3: r,g,b = rgb
    elif len(rgb)>3: r,g,b = rgb[:3]
    if ctype=='256_colors':
        r = (r+25)/51
        g = (g+25)/51
        b = (b+25)/51
        return r*6*6+g*6+b+16
    elif ctype=='default':
        r = r/100
        g = g/100
        b = b/100
        if r and g and b: return 'w'
        elif r and g: return 'y'
        elif r and b: return 'm'
        elif g and b: return 'c'
        elif r: return 'r'
        elif g: return 'g'
        elif b: return 'b'
        else: return 'k'

def getdata(fig,raw):
    ### return dfigure_data[x][y]
    from PIL import Image
    if raw:
        res = []
        im = Image.open(fig)
        xsize = im.size[0]
        ysize = im.size[1]
        for i in range(xsize):
            sub = []
            for j in range(ysize):
                sub.append(im.getpixel((i,j)))
            res.append(sub)
    else:
        xlim,ylim = getsize()
        xsize = int((xlim[1]-xlim[0])/2)
        ysize = int(ylim[1]-ylim[0])
        im = Image.open(fig)
        #data = im.getdata()
        rx = im.size[0]/float(xsize)
        ry = im.size[1]/float(ysize)
    
        rate = int(max((rx,ry)))+1
        xs = range(0,im.size[0],rate)
        ys = range(0,im.size[1],rate)
        res = []
        #print xsize,ysize,im.size
        for i in range(len(xs)):
            sub = []
            for j in range(len(ys)):
                try:
                    r = 0
                    g = 0
                    b = 0
                    x_sub = range(xs[i],xs[i]+rate)
                    y_sub = range(ys[j],ys[j]+rate)
                    l = 0
                    for x in x_sub:
                        for y in y_sub:
                            #print 'a',x,y,im.size,len(x_sub),len(y_sub)
                            r += im.getpixel((x,y))[0]
                            g += im.getpixel((x,y))[1]
                            b += im.getpixel((x,y))[2]
                            l += 1
                except IndexError:
                    x_sub = range(xs[i],im.size[0]-1)
                    y_sub = range(ys[j],im.size[1]-1)
                    for x in x_sub:
                        for y in y_sub:
                            #print 'b',x,y,im.size,len(x_sub),len(y_sub)
                            r += im.getpixel((x,y))[0]
                            g += im.getpixel((x,y))[1]
                            b += im.getpixel((x,y))[2]
                            l += 1
                r /= l
                g /= l
                b /= l
                sub.append((r,g,b))
            #print sub
            res.append(sub)
        #print len(xs),len(ys)
    return res

if __name__ == '__main__':
    import os

    func = raw_input('size, color,data:\n')

    if func == 'size':
        print getsize()
    elif func == 'color':
        r = input('red=')
        g = input('green=')
        b = input('blue=')
        if os.environ.has_key('TERM') and os.environ['TERM']=='xterm-256color':
            ctype='256_colors'
        else:
            ctype='default'
        print setcolor([r,g,b],ctype)
    elif func == 'data':
        fig = raw_input('select file:\n')
        data = getdata(fig,raw=True)
        print data[0][0]

