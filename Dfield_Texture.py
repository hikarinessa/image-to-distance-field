# WORK IN PROGRESS

from scipy import ndimage as ndi
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.distance_transform_edt.html#scipy.ndimage.distance_transform_edt
from numpy import asarray
from PIL import Image

# Parameters
IMG_WIDTH = 512
IMG_HEIGHT = 256
SOURCE = 'res/Space.png'
DESTINATION = 'res/DistanceFieldTexture.png'


source = Image.open(SOURCE)
gray = source.convert('L')  # Convert your image to a grayscale image if not already

# turn the image into an array and perform the distance operation
# the values will be between 0 and 255
# the distance operation is performed twice, once for the outside of the shape and once for the inside
array = asarray(gray)
distance_in = ndi.distance_transform_edt(array, sampling=6)
array_inverted = 255 - array  # for the distance function to work for the outside we need to invert the array
distance_out = ndi.distance_transform_edt(array_inverted, sampling=6)

# we blend the two arrays by adding them and dividing by 2
for x in range(len(distance_out)):
    row = distance_out[x]
    for y in range(len(row)):
        pi1 = 255 - distance_out[x][y]  # we invert the out array again to get back to the correct range
        pi2 = distance_in[x][y]
        pi3 = (pi2 + pi1) * 0.5
        distance_out[x][y] = pi3  # reusing the array out for simplicity

# transform the array back into an image
distance_out = Image.fromarray(distance_out)
distance_out = distance_out.convert('L')  # convert to a grayscale

# resize and save the image
output = distance_out.resize((IMG_WIDTH, IMG_HEIGHT), resample=1)
output = output.save(DESTINATION)
