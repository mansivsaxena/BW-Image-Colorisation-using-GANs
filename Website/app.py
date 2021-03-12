from flask import Flask, request, Response, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
import base64
import numpy as np
from io import BytesIO
import cv2


from db import db_init, db
from models import Img

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)
app.secret_key = "ISTENITK"
import tensorflow as tf

WEIGHTSPATH='weights/gentpu_model.h5'

gen=tf.keras.models.load_model(WEIGHTSPATH)

def imgConversion(image):
    image = base64.b64encode(image)
    img_data = base64.b64decode(image)
    nparr = np.fromstring(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    image = image.decode('UTF-8')
    return image, img_np

def preprocess(img):
    #l_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY )
    l_img_small=cv2.resize(img,(256,256))
    l_img_small=(l_img_small/127.5)-1
    l_img_small=np.reshape(l_img_small,(1,256,256,1))
    return l_img_small

def postprocess(input,pred):
    print(input.shape,pred.shape)
    l_img=pred[:,:,0]
    a_img=pred[:,:,1]
    b_img=pred[:,:,2]
    a_img=((a_img+1)*105.5)+34
    l_img=((l_img+1)*127.5)
    b_img=((b_img+1)*120)+2
    display=np.dstack((l_img,a_img,b_img))
    display=display.astype(np.uint8)
    display=cv2.cvtColor(display, cv2.COLOR_Lab2BGR)
    #display=cv2.resize(display,input.shape)
    return input,display
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        pic = request.files['pic']
        if not pic:
            session["noPic"] = True
            return redirect(url_for("home"))

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            session["badPic"] = True
            return redirect(url_for("home"))

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        session["id"] = img.id
        return redirect(url_for("home"))
    else:
        context = {}
        flag = True
        id = 1
        if session.get("id"):
            id = session["id"]
        img = Img.query.get(id)
        if not img:
            context["badImg"] = True
            img = Img.query.get(1)
            flag = False
        if img:
            curImg, imgNp = imgConversion(img.img)
            context["imgin"] = curImg
            #print(imgNp)

            # imgNp is the np array from the image
            #############################################
            # Fill in prediction stuff                  #
            # img.img is the image object in blob form  #
            input_img=preprocess(imgNp)
            prediction=gen(input_img,training=False).numpy()[0]
            question,answer=postprocess(imgNp,prediction)
            #cv2.imshow("input",question)
            #cv2.waitKey(1)
            #cv2.imshow("output",answer)
            #cv2.waitKey(1)
            outImg=cv2.imencode('.jpg',answer)[1].tobytes()
            outImg,_=imgConversion(outImg)
            context["imgout"]=outImg

            #############################################
           






        if session.get("noPic"):
            context["noImg"] = True
            session.pop("noPic")
            return render_template("index.html", context=context)
        if session.get("badPic"):
            context["badImg"] = True
            session.pop("badPic")
            return render_template("index.html", context=context)
        ## Deleting the picture from db after usage
        if flag and id != 1:
            delImg = Img.query.get(id)
            db.session.delete(delImg)
            db.session.commit()
        return render_template("index.html", context=context)


if __name__ == "__main__":
    app.run(debug=True)
