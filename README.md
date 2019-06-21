# GANs-for-Image-enhancement
## Comparing supervised features in GANs with pretraining for image enhancement(superres)

GANs are hard to train. They are notoriously hard to train and require multiple GPUs and many hours to days, requiring tons of data. Here we compare two GANs whhose discriminator and generators are first pretrained, then put togetheer as GAN.

### DATA: 
High Resolution images used here are from the Flickr-Image-Dataset available at, https://www.kaggle.com/hsankesara/flickr-image-dataset. This is a very diverse dataset and generating photo realistic images from only using this dataset (30k images) is cannot be considered easy. <br>
Noisy(crappy) images are sythetically generated from high resolution images as in the notebook "Crappify-imgs", available in the repository and at https://www.kaggle.com/greenahn/crappify-imgs.
