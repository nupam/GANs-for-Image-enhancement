# GANs-for-Image-enhancement
## Comparing supervised features in GANs with pretraining for image enhancement(superres and decrappify)

GANs are hard to train. They are notoriously hard to train, require multiple GPUs and training time ranges from many hours to days, and also requiring tons of data. Here we compare two GANs whhose discriminator and generators are first pretrained, then put together as GAN.

Two models are trained, there is only one major differene between the model is that of loss function used for pretraining GAN, all other hyper-parameters are same unless otherwise stated.

### DATA 
High Resolution images used here are from the Flickr-Image-Dataset available at, https://www.kaggle.com/hsankesara/flickr-image-dataset. This is a very diverse dataset and generating photo realistic images from only using this dataset (30k images) cannot be considered easy. <br>
Noisy(crappy) images are sythetically generated from high resolution images as in the notebook 'Crappify-imgs', available in the repository and at https://www.kaggle.com/greenahn/crappify-imgs.<br>
nbviewer link: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/Crappify-imgs.ipynb<br>
These images are used for training models.<br>
The dataset of generated images along with their high resolution counter-parts is available at: https://www.kaggle.com/greenahn/flickrproc<br>

### Model
#### Generator
The generator is a UNET with pretrained resnet-34 as backbone. Here we take advantage of the super dynamic class unet_learner of fastai with weight normalization.<br>
#### Discriminator
The discriminator is a gan_critic() also available in fastai library which has spectral normalization built into it, this is usually sufficent for most cases of DCGAN. It is left with its default hyperparameters.<br><br>

### Training
First of all, models are pretrained.

#### Pretraining
##### Generator
The first one uses Mean Squared Error(MSE) as loss. first, the unet is trained by freezing the pretrained resnet-34 part. Then, all of the model is unfreezed and finetuned using smaller learning rate. The image size used in beginning is 128X128, Then the size is increasedd to 256X256 and trained again in a similar way. The notebook is available at https://www.kaggle.com/greenahn/pretrain-gan-mse in addition to the repository.<br>
nbviewer link: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/pretrain-gan-mse.ipynb<br>

The other model uses the same training process but the loss function is sum of Mean Absolute Error(MAE or l1_loss) and feature loss based on VGG-16 model, as in the famous paper on neural art transfer, https://arxiv.org/abs/1508.06576. The notebook is available at https://www.kaggle.com/greenahn/pretrain-gan-feature-loss in addition to the repository.<br>
nbviewer link: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/pretrain-gan-feature-loss.ipynb

##### Discriminator
Images generated by generator are saved to disk and then these images in addition to original high resolution images are used to train it.<br>
#### GAN training
The discriminator and generator are then put together as Gan and trained.
It is trained by switching adaptively between discriminator and generator wheneverever discriminator loss drops below certain threshold.<br>
Learning rate used is the standard LR for GANs, i.e, 0.0002, after training for some time it is then reduced to 0.0001.
Original notebook for model pretrained with MSE: https://www.kaggle.com/greenahn/train-gan-mse<br>
nbviewer: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/train-gan-mse.ipynb<br>
and for pretrained with Feature-loss https://www.kaggle.com/greenahn/train-gan-l1-and-features<br>
nbviewer: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/train-gan-l1-and-features.ipynb<br>
in addition to this repository.<br><br>

#### All trained models are saved and available as part of the notebooks on kaggle and can be downloaded (links above).<br>
In addition generator models are also exported as 'export.pkl'.<br><br>

### Observations
Training was fast.<br>
Considering the time required for training GANs, these models trained faster, total of around 9hrs(per model, including pretraining on 1 GPU)<br>
The model trained with feature loss perfomed much better than without it.<br>
High level features like fur, textures of objects, eyes were more clear in almost every case than that of with MSE.<br>

### Compromises and things that could have been better
We can use WGAN inplace of standard GAN loss(optimization of JS divergence).<br>
and oviously more training.<br>
