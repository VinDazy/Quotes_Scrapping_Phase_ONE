from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image

text = open("tags.txt", "r").read()
python_mask = np.array(PIL.Image.open("logo.jpg"))
colormap = ImageColorGenerator(python_mask)  
word_cloud = WordCloud(
    stopwords=STOPWORDS,
    mask=python_mask,
    background_color='white',
    contour_color='steelblue',
    contour_width=2,
    min_font_size=5,
).generate(text)
#word_cloud.recolor(color_func=colormap)
plt.imshow(word_cloud)
plt.axis("off")
plt.show()

