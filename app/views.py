import re
from flask import render_template
from app import app
#from celery import Celery
from PIL import Image, ImageDraw
from io import BytesIO
import wordcloud as wc


# Celery configuration
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)

#@celery.task(bind=True)
#def load_word_cloud(self):
#	"""Background task that generates the wordcloud image"""


@app.route('/<dimensions>')
@app.route('/<filepath>')

# Experimental image generation
def generate_image(dimensions, filepath):
	#pic = Image.load_image('/Users/me123/python/recap2/app/static/img/breb.jpg');
	#return(pic)
	sizes = [int(s) for s in re.findall(r'\d+', dimensions)]
	if len(sizes) != 2:
		abort(400)

	width = sizes[0]
	height = sizes[1]
	image = Image.new("RGB", (width, height))
	draw = ImageDraw.Draw(image)
	#Position text roughly in the center
	draw.text((width/2 - 25, height/2 - 5), dimensions)
	byte_io = BytesIO()

	image.save(filepath, format='png')
	#image.save(byte_io, 'PNG')
	#byte_io.seek(0)

	#replace the 'app/' with '' using regex 
	filepath = re.sub(r'app/', '', filepath)
	return(filepath)
	#return send_file(byte_io, mimetype='image/png')

#Generate wordcloud
@app.route('/<outputImgPath>')
@app.route('/<imgDimensions>')
@app.route('/<inputTextPath>')
def generate_wordcloud(outputImgPath, imgDimensions, inputTextPath):
	filepath = open(inputTextPath).read()
	
	wordcloud = wc.WordCloud(font_path = '/System/Library/Fonts/HelveticaNeue.dfont', 
		height = 800, width = 1600, background_color='white', 
		max_font_size=180, font_step=1, max_words=40, relative_scaling=0.3)
	wordcloud.generate(filepath)
	image = wordcloud.to_image()

	image.save(outputImgPath, format='png')
	#with args.imagefile:
	#    out = args.imagefile if sys.version < '3' else args.imagefile.buffer
	#    image.save(outputImgPath, format='png')
	filepath = re.sub(r'app/', '', outputImgPath)
	return(filepath)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Tom'}
    
    path = generate_wordcloud('app/static/img/wordcloudimage.png', 'test', 'app/static/files/a_new_hope.txt')
    path2 = generate_wordcloud('app/static/img/wordcloudimage2.png', 'test', 'app/static/files/constitution.txt')

    return render_template('index.html',
            title='Home',
            user=user,
            imga=path,
            imgb=path2)




