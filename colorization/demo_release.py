
from colorization.colorizers.base_color import *
from colorization.colorizers.eccv16 import *
from colorization.colorizers.siggraph17 import *
from colorization.colorizers.util import *

# load colorizers
colorizer_siggraph17 = siggraph17(pretrained=True).eval()

if(False):
	colorizer_siggraph17.cuda()


def colorizier(img: Image):
	global out_img_siggraph17
	(tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256, 256))

	out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

	return numpy_array_to_pil_image(out_img_siggraph17)

if __name__ == "__main__":
	img = load_img(Image.open("D:\\pycharmprojects\\fic_hack_12\\colorization\\images.jpg"))

	pil_image = colorizier(img)
	pil_image.show()
