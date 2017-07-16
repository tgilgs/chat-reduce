import wordcloud as wc
import re
from os import path

inputTextPath='/Users/me123/python/wordcloud/word_cloud/examples/constitution.txt'
outputImgPath='/Users/me123/python/recap2/app/static/img/wordcloud.png'

wordcloud = wc.WordCloud(font_path = '/System/Library/Fonts/HelveticaNeue.dfont', 
		height = 800, width = 1600, background_color='white', 
		max_font_size=120, max_words=50)

#read text file as file
text = open(inputTextPath).read()

wordcloud.generate(text)
image = wordcloud.to_image()

image.save(outputImgPath, format='png')
	#with args.imagefile:
	#    out = args.imagefile if sys.version < '3' else args.imagefile.buffer
	#    image.save(outputImgPath, format='png')
filepath = re.sub(r'app/', '', outputImgPath)