import coldiff # source: https://gist.github.com/marygraceblair/ef858e0f8a314591100c8890cd5c8860
add_library('ColorHarmony')
def setup():
    global source, destination, edge
    threshold = 127
    #update this size based on the size of the image you would like to use 
    size(1200,987)
    source = loadImage("river.jpg")
    destination = createImage(source.width, source.height, RGB)
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

#size of 'brushes' to use
pointillize = [5,8,12,16,14]
brush = [8, 16, 20, 12]

def mouseClicked():
    filter(BLUR)
    noLoop()
        
def draw():
    global source, destination, pointillize, brush
    
    #image(source,0,0)
    destination.loadPixels()  
    ch = ColorHarmony(this)

    destination.updatePixels()
    
    #make this loop for a while and apply over the other part of the painting that you ahve already done 
    i = int(random(source.width))
    y = int(random(source.height))
    
    pixelAX = (int)(random( destination.width))
    pixelAY = (int)(random(destination.height))
    
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
    
    grayColorA = color(destination.pixels[pixelA])
    grayColorB = color(destination.pixels[pixelB])
    
    if ((int)(random(100)) < 40):
        if (diff < 3 and grayColorA==grayColorB):
            print('yes')
            strokeWeight(12)
            strokeCap(ROUND)
            lerColor = lerpColor(color(pixelA), color(pixelB), .3)
            stroke(Ar,Ag,Ab)
            distance = (float)(dist(i,y, pixelBX, pixelBY))
            approved = False
            
            #draw a straight line
            for a in xrange(10): 
                approved = True
                checkX = lerp(i, pixelBX, a/10) + 10   #this was changed from distance but maybe i need to change it later 
                checkY = lerp(y, pixelBY, a/10)
                #what number is this pixel
                checkPixel = (int)(checkX + checkY*destination.width)
                if(color(destination.pixels[checkPixel]) != grayColorA):
                    print(color(destination.pixels[checkPixel]))
                    approved = False
                    return
            if approved:
                if ((int)(random(100)) > 80):
                    strokeWeight(brush[(int)(random(4))])
                    line(i,y,pixelBX, pixelBY)
                else:
                    #draw a bezier curve 
                    #get 2 sets of control points with x/y
                    cptr1X = (int)(random(destination.width))
                    cptr1Y = (int)(random(destination.height))
                    
                    cptr2X = (int)(random( destination.width))
                    cptr2Y = (int)(random(destination.height))
                    
                    midX = (pixelAX + cptr1X)/2 #should i make all of these a float? 
                    midY = (pixelAY + cptr1Y)/2 
                    endX = (pixelBX + cptr2X)/2
                    endY = (pixelBY + cptr2Y)/2
                    
                    cptrMidX = (cptr1X + cptr2X)/2
                    cptrMidY = (cptr1Y + cptr2Y)/2
                    
                    bezStartX = (midX + cptrMidX)/2
                    bezStartY = (midY + cptrMidY)/2
                    bezEndX = (endX + cptrMidX)/2
                    bezEndY = (endY+ cptrMidY)/2
                    
                    midOfPointsX = (pixelAX + pixelBX)/2
                    midOfPointsY = (pixelAY + pixelBY)/2
                    
                    bexMiddlePoint = i + y*destination.width
                    
                    #time to check rgb of the actual middle point 
                    midR = red(source.pixels[bexMiddlePoint])
                    midG = green(source.pixels[bexMiddlePoint])
                    midB = blue(source.pixels[bexMiddlePoint])
    
                    midColor = coldiff.rgb2lab((midR,midG,midB))
    
                    diff = coldiff.cie94(AColor, midColor)
                    
                    if (diff< 3):
                        approved = False
                        for a in xrange(10):
                            approved = True
                            checkX = lerp(i, midOfPointsX, a/10) + 10   #this was changed from distance but maybe i need to change it later 
                            checkY = lerp(y, midOfPointsY, a/10)
                            #what number is this pixel
                            checkPixel = (int)(checkX + checkY*source.width)
                            if(color(destination.pixels[checkPixel]) != grayColorA):
                                print(color(destination.pixels[checkPixel]))
                                approved = False
                                return 
                            #check the rgb of the current pixel 
                            checkR = red(source.pixels[checkPixel])
                            checkG = green(source.pixels[checkPixel])
                            checkB = blue(source.pixels[checkPixel])
                            checkColor = coldiff.rgb2lab((checkR,checkG,checkB))
    
                            diff = coldiff.cie94(AColor, checkColor)
                            if(diff >= 3): 
                                approved = False
                                return
                            if approved:
                                strokeWeight(brush[(int)(random(4))])
                                noFill()
                                bezier(pixelAX, pixelAY, cptr1X, cptr1Y, cptr2X, cptr2Y, pixelBX, pixelBY)
                
                #this is a little bit of an approximation but i can always make it better later 
    
                # startVector = PVector(pixelAX, pixelAY)
                # cptr1Vector = PVector(cptr1X, cptr1Y)
                # endVector = PVector(pixelBX, pixelBY)
                # cptr2Vector = PVector(cptr2X, cptr2Y)
                
                # startAngle = angleBetween(startVector, cptr1Vector)
                # endAngle = angleBetween(endVector, cptr2Vector)
            
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
        
                