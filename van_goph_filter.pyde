import coldiff # source: https://gist.github.com/marygraceblair/ef858e0f8a314591100c8890cd5c8860
add_library('ColorHarmony')
def setup():
    global source, destination, edge
    threshold = 127
    #update this size based on the size of the image you would like to use 
    size(1200,550)
    source = loadImage("forrest.jpg")
    destination = createImage(source.width, source.height, RGB)
    edge = createImage(source.width, source.height, RGB)
    edge.loadPixels()
    edge.filter(THRESHOLD)
    edge.updatePixels()
    background(0)
    smooth()
    frameRate(80)
    
    for x in xrange(source.width):
        for y in xrange(source.height): 
            loc = x + y*source.width
            # Test the brightness against the threshold
            if (brightness(source.pixels[loc]) > threshold):
                destination.pixels[loc]  = color(255) # White
            else:
                destination.pixels[loc]  = color(0)   # Black
    #destination.updatePixels()
    #noLoop() #run draw() once

#size of 'brushes' to use
pointillize = [5,8,12,16,14]
brush = [10, 16, 20, 25]

def mouseClicked():
    filter(BLUR)
    noLoop()
        
def draw():
    global source, destination, pointillize, brush
    
    #image(source,0,0)
    destination.loadPixels()  
    ch = ColorHarmony(this)


    #time to add strokes

    destination.updatePixels()
    # for i in xrange(destination.width):
    #     for y in xrange(source.height):
    
    
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
    

    Br = red(source.pixels[pixelB])
    Bg = green(source.pixels[pixelB])
    Bb = blue(source.pixels[pixelB])

    AColor = coldiff.rgb2lab((Ar,Ag,Ab))
    BColor = coldiff.rgb2lab((Br,Bg,Bb))
    
    
    diff = coldiff.cie94(AColor, BColor)

    if (diff < 3):
        print('yes')
        strokeWeight(12)
        strokeCap(ROUND)
        lerColor = lerpColor(color(pixelA), color(pixelB), .3)
        stroke(Ar,Ag,Ab)
        distance = (float)(dist(i,y, pixelBX, pixelBY))
        approved = False
        for a in xrange(10): 
            approved = True
            checkX = lerp(i, pixelBX, a/distance) + distance
            checkY = lerp(y, pixelBY, a/distance)
            #what number is this pixel
            checkPixel = (int)(checkX + checkY*edge.width)
            if(color(destination.pixels[checkPixel]) != color(0)):
                print(color(destination.pixels[checkPixel]))
                approved = False
                return 
        if (color(destination.pixels[pixelA]) != color(0) and color(destination.pixels[pixelB]) != color(0)):
            approved = False
        if approved:
            strokeWeight(brush[(int)(random(4))])
            line(i,y,pixelBX, pixelBY)

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
                strokeWeight(pointillize[(int)(random(4))])
                strokeCap(ROUND)
                stroke(Ar,Ag,Ab)
                if (diff < 5):
                    if (random(100) < 1):
                        analogousColors = ch.Monochromatic(color(pixelA))
                        ps = (int)(random(8))
                        stroke(analogousColors[ps])
                    line(i,y,xx,yy)
        
                