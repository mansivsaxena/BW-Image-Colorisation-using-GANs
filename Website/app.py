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


def imgConversion(image):
    image = base64.b64encode(image)
    img_data = base64.b64decode(image)
    nparr = np.fromstring(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    image = image.decode('UTF-8')
    return image, img_np


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
            context["img"] = curImg
            #print(imgNp)

            # imgNp is the np array from the image
            #############################################
            # Fill in prediction stuff                  #
            # img.img is the image object in blob form  #
            #############################################

        if session.get("noPic"):
            context["noImg"] = True
            session.pop("noPic")
            return render_template("index.html", context=context)
        if session.get("badPic"):
            context["badImg"] = True
            session.pop("badPic")
            return render_template("index.html", context=context)
        # Deleting the picture from db after usage
        if flag and id != 1:
            delImg = Img.query.get(id)
            db.session.delete(delImg)
            db.session.commit()
        return render_template("index.html", context=context)


if __name__ == "__main__":
    app.run(debug=True)
