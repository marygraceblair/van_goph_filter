import coldiff # source: https://gist.github.com/marygraceblair/ef858e0f8a314591100c8890cd5c8860
add_library('ColorHarmony')
def setup():
    global source, destination
    #update this size based on the size of the image you would like to use 
    size(1200,550)
    source = loadImage("But-Thats-None-Of-My-Business.jpg")
    destination = createImage(source.width, source.height, RGB)
    background(0)
    smooth()
    #noLoop() #run draw() once

#size of 'brushes' to use
pointillize = 16

def mouseClicked():
    noLoop()
        
def draw():
    global source, destination, pointillize
    #image(source,0,0)
    #destination.loadPixels()  
    ch = ColorHarmony(this)
    
    #loop through the pixels
    #counts number of times colors are similar in a row      
    # frequencyColorCounter = 0
    # for x in (a for a in xrange(source.width) if (a % 3 == 0)):
    #     for y in (b for b in xrange(source.height) if (b % 3 == 0)):
    #         #get the index of the current pixel in the pixel array and its RGB values  
    #         current = x + y*source.width 
    #         currentR = red(source.pixels[current])
    #         currentG = green(source.pixels[current])
    #         currentB = blue(source.pixels[current])  
            
    #         #convert current pixels into lab for use with coldiff 
    #         currentColor = coldiff.rgb2lab((currentR, currentG, currentB))

            # #for xx in range(x-1, x+2):
            # #    for yy in range(y-1, y+2): 
            # #        if (xx>=0 and xx<source.width and yy>=0 and yy<source.height and xx!=x and yy!=y):
            # #            #current pixel of the neighbor being examined and its RGB 
            #             neighbor = xx + yy*source.width 
            #             r = red(source.pixels[neighbor])
            #             g = green(source.pixels[neighbor])
            #             b = blue(source.pixels[neighbor])
            #             neighborColor = coldiff.rgb2lab((r,g,b))
            #             diff = coldiff.cie94(currentColor , neighborColor)
                
            #             #fill(r,g,b,100)
            #             #noStroke
            #             #ellipseMode(CENTER)
            #             # ellipse(x,y,pointSize,pointSize)
            #             #
            #             strokeWeight(12)
            #             strokeCap(ROUND)
            #             stroke(currentR, currentG, currentB)
            #             if (diff < 5):
            #                 frequencyColorCounter += 1 
            #                 if ((frequencyColorCounter) > 500):
            #                     analogousColors = ch.Monochromatic(color(current))
            #                     ps = (int)(random(8))
            #                     stroke(analogousColors[ps])
            #                 line(x,y,xx, yy)
            #             else:
            #                 #ps = (int)(random(4))
            #                 #pointSize = pointillize[ps]
            #                 frequencyColorCounter = 0 
            #                 #fill(r,g,b,100)
            #                 #noStroke
            #                 #ellipseMode(CENTER)
            #                 #ellipse(x,y,pointSize,pointSize)
        
            
            #    ps = int(random(200))
                #if (ps < 10):
            #    ps = int(random(4))
             #   pointSize = pointillize[ps]
              
                #  fill(r,g,b,100)
                #noStroke
                #ellipseMode(CENTER)
                #ellipse(x,y,pointSize,pointSize)
                
    #time to add strokes
    print('before loop')
    #destination.loadPixels()
    # for i in xrange(destination.width):
    #     for y in xrange(source.height):
    print('y loop')
    
    #make this loop for a while and apply over the other part of the painting that you ahve already done 
    i = int(random(source.width))
    y = int(random(source.height))

    
    pixelAX = (int)(random( destination.width))#a for a in xrange(destination.width) if (a % 3 == 0))
    pixelAY = (int)(random(destination.height)) #random(a for a in xrange(destination.height) if (a % 3 == 0))
    
    pixelBX = (int)(random(destination.width))
    pixelBY = (int)(random(destination.height))

    pixelA = i + y*destination.width
    pixelB = pixelBX + pixelBY*destination.width

    Ar = red(source.pixels[pixelA])
    Ag = green(source.pixels[pixelA])
    Ab = blue(source.pixels[pixelA])
    
    print('Ar pixel extracted')
    Br = red(source.pixels[pixelB])
    Bg = green(source.pixels[pixelB])
    Bb = blue(source.pixels[pixelB])

    AColor = coldiff.rgb2lab((Ar,Ag,Ab))
    BColor = coldiff.rgb2lab((Br,Bg,Bb))
    print('got color lab')
    
    diff = coldiff.cie94(AColor, BColor)
    print('color difference')
    if (diff < 3):
        strokeWeight(12)
        strokeCap(ROUND)
        lerColor = lerpColor(color(pixelA), color(pixelB), .3)
        stroke(Ar,Ag,Ab)
        line(i,y,pixelBX, pixelBY)
    else:
        print('no')
    for xx in range(i-1, i+2):
        for yy in range(y-1, y+2): 
            if (xx>=0 and xx<source.width and yy>=0 and yy<source.height and xx!=i and yy!=y):
                #current pixel of the neighbor being examined and its RGB 
                neighbor = xx + yy*source.width 
                r = red(source.pixels[neighbor])
                g = green(source.pixels[neighbor])
                b = blue(source.pixels[neighbor])
                neighborColor = coldiff.rgb2lab((r,g,b))
                diff = coldiff.cie94(AColor, neighborColor)
                strokeWeight(12)
                strokeCap(ROUND)
                stroke(Ar,Ag,Ab)
                if (diff < 5):
                    if (random(100) < 10):
                        analogousColors = ch.Monochromatic(color(pixelA))
                        ps = (int)(random(8))
                        stroke(analogousColors[ps])
                    line(i,y,xx, yy)
        
                