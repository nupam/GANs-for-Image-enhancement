# GANs-for-Image-enhancement
## Comparing supervised features in GANs with pretraining for image enhancement(superres)

GANs are hard to train. They are notoriously hard to train, require multiple GPUs and training time ranges from many hours to days, and also requiring tons of data. Here we compare two GANs whhose discriminator and generators are first pretrained, then put together as GAN.

Two models are trained, there is only one major differene between the model is that of loss function used for pretraining GAN, all other hyper-parameters are same unless otherwise stated.

### DATA 
High Resolution images used here are from the Flickr-Image-Dataset available at, https://www.kaggle.com/hsankesara/flickr-image-dataset. This is a very diverse dataset and generating photo realistic images from only using this dataset (30k images) is cannot be considered easy. <br>
Noisy(crappy) images are sythetically generated from high resolution images as in the notebook "Crappify-imgs", available in the repository and at https://www.kaggle.com/greenahn/crappify-imgs.<br>
nbviewer link: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/Crappify-imgs.ipynb<br>
These images are then used as data for training.<br><br>

### Model
#### Generator
The generator is a UNET with pretrained resnet-34 as backbone. Here we take advantage of the super dynamic class unet_learner of fastai with weight normalization.<br>
#### Discriminator
The discriminator is a gan_critic() also available in fastai library which has spectral normalization built into it, this is usually sufficent for most cases of DCGAN. It is left with its default hyperparameters.<br><br>

### Training
First of all, models are pretrained.
#### Pretraining
##### Generator
The first one uses Mean Squared Error(MSE) as loss. The unet is trained by freezing the pretrained resnet-34 part. Then all of the model is unfreezed and finetuned using smaller learning rate. The image size used in beginning is 128X128, Then the size is increasedd to 256X256 and trained again. The notebook is available at https://www.kaggle.com/greenahn/pretrain-gan-mse in addition to the repository.<br>
The other model uses the same training process but the loss function is sum of MAE(l1_loss) and feature loss based on VGG-16 model, as in the famous paper on neural art transfer, https://arxiv.org/abs/1508.06576. The notebook is available at https://www.kaggle.com/greenahn/pretrain-gan-feature-loss in addition to the repository.<br>
nbviewer link: https://nbviewer.jupyter.org/github/nupam/GANs-for-Image-enhancement/blob/master/pretrain-gan-feature-loss.ipynb
##### Discriminator
Images generated by generator are saved to disk and then these images in addition to original high resolution images are used to train it.<br>
#### GAN training
The discriminator and generator are then put together as Gan and trained.
It is trained by switching adaptively between discriminator and generator wheneverever discriminator loss drops below certain threshold.<br>
Learning rate used is the standard LR for GANs, i.e, 0.0002, after training for some time it is then reduced to 0.0001.

