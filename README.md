# BW-Image-Colorisation-using-GANs
A Black and White Image colorisier using Generative Adversarial Networks

---
This Project was done under the <b>Crypt</b> Special Interest Group of <a href="https://iste.nitk.ac.in/">ISTE-NITK</a>

The Project was done entirely in <b>Python 3</b> and its various libraries<br>

---

### Website
To install and run simple flask server: 
1. Clone repo
2. Go to "Website" folder
3. Make a virtual environment (preferably) 
4. pip install -r requirements.txt
5. python app.py
6. localhost:5000 to access the website


### Model Weights
The best model weights (baseline,TPU) can be found [here](https://drive.google.com/drive/folders/1IG-QujUxtU7e56dDVic_-bWz6uBg1Uci?usp=sharing)

### Tfrecords Shards
The LAB version of dataset converted to tfrecord shards can be found [here](https://drive.google.com/drive/folders/1-vCQPdLhQwfge3WjYsal9jt6-Y_FwCux?usp=sharing)

---
### Methodology
The project can be broadly divided into the following phases:
<dl>
  <dt>1)Dataset Filtering and Input Pipeline</dt>
  <ul>
    <li>Used testing subset of the <a href="http://places2.csail.mit.edu/download.html">Places365 dataset</a> (256x256)</li>
    <li>Filtered ~8000 images which did not suit colorisation problem</li>
    <div>
    <img src="https://i.redd.it/koss642o8en61.jpg" width=200px>
      <sub> <em>*Sample bad image</em> </sub>
    </div>
    <li>Final dataset size ~300k images</li>
    <li>Converted dataset into LAB colorspace and stored into 28 tfrecord shards</li>
    
  </ul>
  
  <dt>2)Baseline UNET GAN</dt>
  <ul>
    <li>Implemented UNET based coloriser inspired from <a href="https://phillipi.github.io/pix2pix/">Pix2Pix</a></li>
    <li>Trained for 15hrs(2 epochs) on google colab GPU</li>
    <li>Results while impressive in some cases;were mostly inconsitent</li>
  <div>
  <img src="https://i.redd.it/4mxf9ne3ben61.jpg"><br>
    <sub> <em>*Sample generated image</em> </sub>
  </div>
  <li>Notebook used for training can be found here <a href="https://colab.research.google.com/drive/1q8jDyzCTW7yZrmuBaOepbeQQgHd6FUHH?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" align="center"></a></li>
  
  </ul>
  
  <dt>3)Evolutionary Generative Adverserial Networks</dt>
  <ul>
    <li>Attempted to improve upon previous result by novel training mechanism as suggested in <a href="https://drive.google.com/file/d/10fY8FnqepESzdd0NO__uPEZMqY8dMn8C/view?usp=sharing"> this paper </a> </li>
    <li>Failed to train model upto sufficient convergence due to extreme memory requirements and limited compute resources <ul><li><sub>After initial testing we expect at least 32GB of GPU memory and approximately 48hrs of train time would give substantial results</sub></li></ul></li>
  <div>
  <img src="https://i.redd.it/4ynx0eoegen61.png"><br>
    <sub> <em>*Sample generated image</em> </sub>
  </div>
  
   <li>Notebook used for training can be found here <a href="https://colab.research.google.com/drive/1zI4Eq0Docd4FLhs0PuCOJ9wpdJb1Mvoz?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" align="center"></a></li>
  </ul>
  
  <dt>4)DeOldify</dt>
  <ul>
    <li>Attempted to replicate results of <a href="https://github.com/jantic/DeOldify">DeOldify</a> by porting to Tensorflow</li>
    <li>Experimented with EfficientNet Backbones instead of Resnet based ones in original repository</li>
    <li>Since model has close to 300M parameters,we failed to train it to convergence due to insufficent compute resources<ul><li><sub>After initial testing we expect at least 32GB of GPU memory and approximately 48hrs of train time would give substantial results</sub></li></ul></li>
  <div>
  <img src="https://i.redd.it/dpbshotswen61.png"><br>
    <sub> <em>*Sample generated image</em> </sub>
  </div>
  
   <li>Notebook used for training can be found here <a href="https://colab.research.google.com/drive/1aCjKanfe1IPCtcZOaRIgX_P2R7NSDmpl?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" align="center"></a></li>
  </ul>
  
  <dt>5)Improve Baseline With TPU training</dt>
  <ul>
    <li>Same architecture as baseline</li>
    <li>Uploaded dataset to gcs bucket and trained using free colab TPU</li>
    <li>Train time ~6hrs(4epochs)</li>
  <li>Significantly improved results than baseline.However our analysis suggests tendencies of overfitting.Possible causes:<ul><li>Small Dataset</li><li>Overshoot GAN stability threshold </li></ul><br>
  <div>
  <img src="https://i.redd.it/uec0s3ivyen61.png"><br>
    <sub> <em>*Sample generated image</em> </sub>
  </div>
  
   <li>Notebook used for training can be found here <a href="https://colab.research.google.com/drive/1GAIAowBEQ2ZCq0lLAbLX8YgpvsR10MOS?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" align="center"></a></li>
  </ul>
  
  
</dl>

---

Libraries used:Tensorflow 2.4,opencv,numpy,Pandas,matplotlib

---
<br>
<em>NOTE: <br>While we failed to acheive the supposed theoretical improvements as proposed by DeOldify and EGANs,we strongly believe that given the appropriate compute resources,these models can produce results comparable(if not better) to current SOTA.
  <br>
  
</em>
