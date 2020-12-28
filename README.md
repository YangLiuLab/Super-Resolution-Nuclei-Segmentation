# Super-Resolution-Nuclei-Segmentation
## Convenient Colab notebooks for conducting computational segmentation of super-resolution cell nuclei

### Links for Colab Files:

### Mask R-CNN
https://colab.research.google.com/drive/1myJzki7mBYHMKVXrLO71iBRum26sZ6io?usp=sharing

### Mask R-CNN Local
https://colab.research.google.com/drive/14DB2rdVcmJ_ivkJIOr8NHX3x7J3_KxiT?usp=sharing

### ANCIS
https://colab.research.google.com/drive/1NWgd2DKlQETOQ7M8on_2KY3H0HSkoWXC?usp=sharing

### UNet
https://colab.research.google.com/drive/1FFy5WCqr1taCBQtnyIozinyzRwHkZHAd?usp=sharing

### UNet Local
https://colab.research.google.com/drive/1AGK0Q_0ywWgb3-QaEu3gZrSR0lPAKPcj?usp=sharing

### Image Tile
https://colab.research.google.com/drive/1bKRAsfe3zTPUmidUgi5116pbGH9TLDVZ?usp=sharing

### Image Tile Local
https://colab.research.google.com/drive/17bZ5Mdre74oVXY_SR4byhUSOxjjBOW4A?usp=sharing

*Local Files require connecting to local PC, to use local resources, see instructions in notebook header.

Use reselectPredictions.py for editing neural network predictions using python on local pc.

## General Instructions

### Testing

Have a folder ready containing super-resolution images.  When running code on the Colab (non-local) network, select each image to upload or place images in your Drive folder and note the path.

### Training

Have a folder containing your training images and another containing a training label for each image.  See examples folder.  Images and Labels should share the same name. Labels can be created with sequential numbering (e.g. 1,2,3...) (see Tissue --> Labels) or binary (see Cell Line --> Labels).

### Pre-Trained Weights

We are including some pre-trained weights for each network, accessible here: https://drive.google.com/drive/folders/1yKxyXkk4ceXoDpd647i1_-JWLjzKOY7t?usp=sharing
Weights can be used for testing or as a base for additional training (for Mask R-CNN).
