# Texere: This is the start of a new Module
Currently it has two function 1.Text Removal from Images and generate mask 2.Marking Edges in Images

Texere is a Python package that provides functionality for removing text from images and marking edges, along with the option to generate a mask for further processing.

## Installation

You can install Texere using pip:

```
pip install texere
```

## Usage: 
# Removing Text from Images
```
from texere.purge import txt

modified_image, mask = txt('image_path.jpg',pixels,threshold)

# 'modified_image' contains the image with text removed
# 'mask' is a binary image indicating the regions where text was removed
# Further processing using the 'mask' image can be done here
```
# Marking Edges in the image
```
from texere.edges import mark

# Replace 'image_path.jpg' with the path to your input image
marked_image = mark('image_path.jpg',threshold)

# 'marked_image' contains the image with marked edges
# You can further process or visualize the edges here
```
## Example:
# Removing Text from Images
```
from texere.purge import txt

# Replace 'input_image.jpg' with the path to your input image
modified_image, mask = txt('input_image.jpg',7,10)

#threshold value is from 0-100
#pixels value >0
#depending on these two value the image will turn out Good 
# Save the modified image
cv2.imwrite('output_image.jpg', modified_image)

# Save the mask as a binary image its a grayscaled image so it can be used for impainting the text area
cv2.imwrite('mask_image.jpg', mask)
```

# Marking Edges in the image
```
from texere.edges import mark

# Replace 'input_image.jpg' with the path to your input image
marked_image = mark('input_image.jpg',threshold)
#threshold value can be between 0-255 also images i tried on works best with 70 
# Save the marked image
marked_image.save('marked_image.jpg')
```
# Contributing:
Contributions to Texere are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request on GitHub.

# License:
This project is licensed under the MIT License - see the LICENSE file for details.
