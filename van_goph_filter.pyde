# van_goph_filter
# author: Mary Grace Blair 

import coldiff #source: https://gist.github.com/fikr4n/368f2f2070e0f9a15fb4

add_library('ColorHarmony')
def setup():
    global source, destination, edge
    threshold = 127
    #update this size based on the size of the image you would like to use 
    size(1200,987)
    #update this with the name of the image you would like to filter 
    source = loadImage("forrest.jpg")
    destination = createImage(source.width, source.height, RGB)
    background(0)
    smooth()
    frameRate(80)
    
    # ********************************************************************
    # code for creating THRESHOLD FILTER for use with edge-detection from
    # https://processing.org/tutorials/pixels/
    # Brightness Threshold Example 
    for x in xrange(source.width):
        for y in xrange(source.height): 
            loc = x + y*source.width
            # Test the brightness against the threshold
            if (brightness(source.pixels[loc]) > threshold):
                destination.pixels[loc]  = color(255) # White
            else:
                destination.pixels[loc]  = color(0)   # Black
    #**********************************************************************
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
    
    #pick random points to draw a line between
    i = int(random(source.width))
    y = int(random(source.height))
    
    pixelAX = (int)(random( destination.width))
    pixelAY = (int)(random(destination.height))
    
    pixelBX = (int)(random(destination.width))
    pixelBY = (int)(random(destination.height))

    #get index of pixel from pixel array
    pixelA = i + y*destination.width
    pixelB = pixelBX + pixelBY*destination.width

    #get rgb values from the two pixels
    Ar = red(source.pixels[pixelA])
    Ag = green(source.pixels[pixelA])
    Ab = blue(source.pixels[pixelA])
    
    Br = red(source.pixels[pixelB])
    Bg = green(source.pixels[pixelB])
    Bb = blue(source.pixels[pixelB])

    #convert RGB values to lab and take color difference
    AColor = coldiff.rgb2lab((Ar,Ag,Ab))
    BColor = coldiff.rgb2lab((Br,Bg,Bb))
    diff = coldiff.cie94(AColor, BColor)
    
    #get color of the pixels from the edge array
    grayColorA = color(destination.pixels[pixelA])
    grayColorB = color(destination.pixels[pixelB])
    
    if ((int)(random(100)) < 50): #ratio of dots to lines/curves 
        #if the colors are similar and both pixels are either black or white in edge array either attempt a line or curve 
        if (diff < 3 and grayColorA==grayColorB):
            strokeWeight(12)
            strokeCap(ROUND)
            #colors are similar enough to choose onne
            stroke(Ar,Ag,Ab)
            approved = False
            
            #draw a straight line
            #check that there are no edges preventing the lines from being drawn
            for a in xrange(10): 
                approved = True
                #get X and Y values of pixel along the line under consideration 
                checkX = lerp(i, pixelBX, a/10) + 10   
                checkY = lerp(y, pixelBY, a/10)
                #check what index pixel is in the pixel array
                checkPixel = (int)(checkX + checkY*destination.width)
                #pixel must have the same color as the endpoints of the line
                if(color(destination.pixels[checkPixel]) != grayColorA):
                    print(color(destination.pixels[checkPixel]))
                    approved = False
                    return
            #if the line passes edge-detection criteria
            if approved:
                if ((int)(random(100)) > 50): #ratio of straight lines to curves 
                    strokeWeight(brush[(int)(random(4))])
                    line(i,y,pixelBX, pixelBY) #draw the line
                else:
                    #draw a bezier curve 
                    #get 2 sets of random control points with x/y
                    cptr1X = (int)(random(destination.width))
                    cptr1Y = (int)(random(destination.height))
                    cptr2X = (int)(random( destination.width))
                    cptr2Y = (int)(random(destination.height))
                    
                    #find midpoints to determine top of the bezier curve 
                    midX = (pixelAX + cptr1X)/2 
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
                    
                    #find index of top of the Bezier curve into pixel array 
                    bexMiddlePoint = i + y*destination.width
                    
                    #check RGB of this point, convert to lab, check color difference
                    midR = red(source.pixels[bexMiddlePoint])
                    midG = green(source.pixels[bexMiddlePoint])
                    midB = blue(source.pixels[bexMiddlePoint])
                    midColor = coldiff.rgb2lab((midR,midG,midB))
                    diff = coldiff.cie94(AColor, midColor)
                    
                    #if colors are similar enough
                    if (diff< 3):
                        approved = False
                        #check from bottom of the curve to the top against edge and color differences 
                        for a in xrange(10):
                            approved = True
                            #get X/Y values of point being tested 
                            checkX = lerp(i, midOfPointsX, a/10) + 10 
                            checkY = lerp(y, midOfPointsY, a/10)
                            #find index of pixel into pixel array 
                            checkPixel = (int)(checkX + checkY*source.width)
                            if(color(destination.pixels[checkPixel]) != grayColorA):
                                print(color(destination.pixels[checkPixel]))
                                approved = False
                                return 
                            #check the rgb of the current pixel, convert to lab, take color difference
                            checkR = red(source.pixels[checkPixel])
                            checkG = green(source.pixels[checkPixel])
                            checkB = blue(source.pixels[checkPixel])
                            checkColor = coldiff.rgb2lab((checkR,checkG,checkB))
                            diff = coldiff.cie94(AColor, checkColor)
                            if(diff >= 3): 
                                approved = False
                                return
                            if approved:
                                #draw the bezier curve 
                                strokeWeight(brush[(int)(random(4))])
                                noFill()
                                bezier(pixelAX, pixelAY, cptr1X, cptr1Y, cptr2X, cptr2Y, pixelBX, pixelBY)
    
    #check neighboring pixels and draw a line(dot) if colors are similar 
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
                    #occasionally change the color of the dots to a similar color 
                    if (random(100) < 1):
                        analogousColors = ch.Monochromatic(color(pixelA))
                        ps = (int)(random(8))
                        stroke(analogousColors[ps])
                    line(i,y,xx,yy)
        
                