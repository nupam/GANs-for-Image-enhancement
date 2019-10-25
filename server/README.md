download the trained model, export.pkl from the link in provided in github repository and put it in models folder.

run the application using command "python server.py serve" to start the server.
The server can be then found on port 5042.
A copy of all enhanced images are saved in ./view/enhanced folder.

requirements:
	numpy
	torchvision
	https://download.pytorch.org/whl/cpu/torch-1.0.1.post2-cp37-cp37m-linux_x86_64.whl
	fastai
	starlette
	uvicorn==0.3.32
	python-multipart
	aiofiles
	aiohttp
	
This web app is a modified version of the sample app availabe on https://fastai-v3.onrender.com.

