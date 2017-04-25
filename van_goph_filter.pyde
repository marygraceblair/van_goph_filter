import coldiff # source: https://gist.github.com/marygraceblair/ef858e0f8a314591100c8890cd5c8860 

def setup():
    global source, destination
    #update this size based on the size of the image you would like to use 
    size(1200,550)
    source = loadImage("river.jpg")
    destination = createImage(source.width, source.height, RGB)
    background(0)
    smooth()
    noLoop() #run draw() once
    loadPixels()

#size of 'brushes' to use
pointillize = [16,5,12,8] 
    
def draw():
    global source, destination, pointillize
    destination.loadPixels()  
    
    #loop through the pixels             
    for x in (a for a in xrange(source.width) if (a % 3 == 0)):
        for y in (b for b in xrange(source.height) if (b % 3 == 0)):
            #get the index of the current pixel in the pixel array and its RGB values  
            current = x + y*source.width 
            currentR = red(source.pixels[current])
            currentG = green(source.pixels[current])
            currentB = blue(source.pixels[current])  
            
            #convert current pixels into lab for use with coldiff 
            currentColor = coldiff.rgb2lab((currentR, currentG, currentB))

            for xx in range(x-1, x+2):
                for yy in range(y-1, y+2): 
                    if (xx>=0 and xx<source.width and yy>=0 and yy<source.height and xx!=x and yy!=y):
                        #current pixel of the neighbor being examined and its RGB 
                        neighbor = xx + yy*source.width 
                        r = red(source.pixels[neighbor])
                        g = green(source.pixels[neighbor])
                        b = blue(source.pixels[neighbor])
                        neighborColor = coldiff.rgb2lab((r,g,b))
                        diff = coldiff.cie94(currentColor , neighborColor)
                
                        #fill(r,g,b,100)
                        #noStroke
                        #ellipseMode(CENTER)
                        # ellipse(x,y,pointSize,pointSize)
                        #
                        if (diff < 3):
                            strokeWeight(12)
                            strokeCap(ROUND)
                            stroke(currentR, currentG, currentB)
                            if (random(100) < 10):
                                stroke(lerpColor(color(current), color(neighbor),.33))
                            line(x,y,xx, yy)   
            destination.pixels[current] = color(current)
            
            #    ps = int(random(200))
                #if (ps < 10):
            #    ps = int(random(4))
             #   pointSize = pointillize[ps]
              
                #  fill(r,g,b,100)
                #noStroke
                #ellipseMode(CENTER)
                #ellipse(x,y,pointSize,pointSize)
                
    #time to add strokes
    #for i in (a for a in xrange(destination.width)):
    # for y in (b for b in xrange(source.height)):
    #        #pixelAX = random.randrange(0, destination.width, 3 ) #a for a in xrange(destination.width) if (a % 3 == 0))
     #       #pixelAY = random.randrange(0, destination.height, 3 ) #random(a for a in xrange(destination.height) if (a % 3 == 0))
      #      
       #     pixelBX = random.randrange(0, destination.width, 3 )
        #    pixelBY = random.randrange(0, destination.height, 3 )
            
            
            
         #   if pixelBX > destination.width:
          #      break
           # if pixelBY > destination.height:
            #    break
            
        #    pixelA = i + y*destination.width
        #    pixelB = pixelBX + pixelBY*destination.width
        
        #    Ar = red(destination.pixels[pixelA])
         #   Ag = green(destination.pixels[pixelA])
          #  Ab = blue(destination.pixels[pixelA])
           # Br = red(destination.pixels[pixelB])
            #Bg = green(destination.pixels[pixelB])
            #Bb = blue(destination.pixels[pixelB])
            
            #curIntensityA = (int)((((Ar+Ag+Ab)/3)/80))
            #curIntensityB = (int)((((Br+Bg+Bb)/3)/80))
            #diff = abs(curIntensityA - curIntensityB)
       #     diff = colorDist(color(pixelA), color(pixelB))
       #     distance=dist(x,y, pixelBX, pixelBY)
            #if (1):
            #    strokeWeight(12)
            #    strokeCap(ROUND)
               
            #    lineColor = None
                #if index == 0:
                #    lineColor = color(pixelA)
                #else:
                #    lineColor = color(pixelB)
           #     stroke(color(Ar,Ag,Ab))
           #     line(x,y,pixelBX, pixelBY)

    destination.updatePixels()