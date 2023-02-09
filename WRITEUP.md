# Solution

The first thing that I noticed when I looked at the images, this is a rare type of dataset. The task is so unfamiliar and may related to bioinformatics. \
I tried to find similar resources such as datasets and model weights. None of them are available. \
I decided to use image processing to get the region of the interest and the color of the vibrio. \

The processed image is simple and done this before for doing OCR:
1. We need to define the color range of green, yellow and black. Based on my observation, these three colors that appear in the dataset. So the program is limited to certain color of vibrio. If the color of the vibrio is out of this range, it simply doesn't recognize it.
2. The image was dilated to fill the gap between small dots and creates a distinction between the object and the background.
3. cThen, the findContour() method was used to detect the object and draw the bounding boxes of the object.
4. Since we already set the image range, then we just classify the vibrio color based on the range and count how many bounding boxes in the image.
5. We set a filter the has area between 100 and 15000 to remove false positive object and I also calculate the coordinate inside the mirror by measuring the distance from the central in a shape of circle.

The program is far from perfect, but it is good as a proof of concept and can be a starting point to build object detection dataset and later to be used for deep learning approach. This program shows that this is something that doable and help aquaculture experts to identify vibrio color, size and totals.