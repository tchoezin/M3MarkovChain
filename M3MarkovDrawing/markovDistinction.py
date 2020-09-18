import sys
import os
import random
from PIL import Image, ImageDraw

# Tenzin Choezin, 9/18/2020

#global variables
startingProbList = []
markovChain = {}


# Purpose: Takes an image and by looping through every pixel in the image, creates a starting probability list
# list and a markov chain dictionary.
# Argument: artwork -> an image file
# Return: None, updates global variables
def haloMapSystemCreator(artwork):
    global startingProbList
    global markovChain

    #creates an Image object from the given image and converts it into pixels with RGB values
    haloMap = Image.open(artwork).convert("RGB")

    width, height = haloMap.size

    # current image's pixel list
    pixelRGB = []

    # adding pixels of current image to the pixel list
    for i in range(0, width):
        for j in range(0, height):
            pixelRGB.append(haloMap.getpixel((i,j)))

    # updating starting probability list
    startingProbList = startingProbList + pixelRGB

    # stores what pixel comes directly after every current pixel
    for i in range(0, len(pixelRGB) - 2):
        if pixelRGB[i] in markovChain:
            markovChain[pixelRGB[i]].append(pixelRGB[i+1])
        else:
            markovChain[pixelRGB[i]] = [pixelRGB[i+1]]

# Purpose: from the given starting probability list and markov chain dictionary, constructs an image
# Argument: none
# Return: newHaloMap -> Image object of the newly constructed image
def newHaloMapCreator():
    global startingProbList
    global markovChain

    #new image dimensions
    height = 768
    width = 1024

    #construct Image object
    newHaloMap = Image.new("RGB", (width, height))

    #loads pixel data of Image object
    pixelsHalo = newHaloMap.load()

    #color in the first pixel with a random color from the starting probabilities list
    pixelsHalo[0, 0] = (random.choice(startingProbList))
    
    #fill in the rest of the column utilizing the markov chain dictionary
    for j in range(1, height):
        pixelsHalo[0,j] = (random.choice(markovChain[newHaloMap.getpixel((0,j-1))]))
    
    #fill in the rest of the image using the markov chain dictionary
    for i in range(1, width):
        for j in range(0, height):
            if j == 0:
                pixelsHalo[i,j] = (random.choice(markovChain[newHaloMap.getpixel((i-1, height-1))]))
            else:
                pixelsHalo[i,j] = (random.choice(markovChain[newHaloMap.getpixel((i,j-1))]))
    
    return newHaloMap


def main():

    #loop through every ".jpg" image in the folder identified by the absolute path
    for imageName in os.listdir("/Users/tenzinchoezin/Desktop/ComputationalCreativity/M3MarkovDrawing"):
        if imageName.endswith(".jpg"):
            haloMapSystemCreator(imageName)

    #saves the image under the new image name
    newHaloMapCreator().save("NewHaloMap4.jpg")

if __name__ == "__main__":
    main()