from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO
import torch
import fastai
from fastai import *
from fastai.vision import *
from helpers import *
from pathlib import Path

export_file_name = 'export.pkl'

path = Path(__file__).parent

app = Starlette()
app.debug = True
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='static'))
app.mount('/images', StaticFiles(directory='view/images'))

MAX_SIZE = 896


def enhance(img):
	print('input img size ',img.size)
	if img.size[0] > MAX_SIZE or img.size[1] > MAX_SIZE:
		img.resize((3, *resize_to(img, MAX_SIZE)))
		img.refresh()
	if img.size[0]%2 == 1 or img.size[1]%2 ==1:
		h = img.size[0]-1 if img.size[0]%2 ==1 else img.size[0]
		w = img.size[1]-1 if img.size[1]%2 ==1 else img.size[1]
		img.resize((3, h, w))
		img.refresh()
		
	print('rezized img size ',img.size)
	fname = ''.join(random.choices(string.ascii_uppercase, k=10))+'.jpg'
	print('fname', fname)
	#img.save('view/images/original' +fname)
	out0 = learn.predict(img)
	img.flip_lr()
	out1 = learn.predict(img)
	out1[0].flip_lr()
	temp = (out0[0].data + out1[0].data)/2
	temp = fastai.vision.image2np(temp)
	plt.imsave( 'view/images/enhanced/' + fname, temp)
	return fname
	

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    fastai.device = torch.device('cpu')
    #await download_file(export_file_url, path/export_file_name)
    try:
        learn = load_learner("./models")
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()



@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()
    img_bytes = await (data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = enhance(img)
    print('returning' , prediction)
    return JSONResponse({'result': str(prediction)})

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)
