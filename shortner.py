from flask import Flask, render_template,flash,request,redirect,url_for
import redis
import random
import time


app = Flask(__name__)
r1 = redis.Redis(host = 'localhost' , port=6379, db = 1)
r2 = redis.Redis(host = 'localhost' , port =6379, db =2 )
random.seed(time.time())
rn = str(int(random.random() * 100))
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/shorten',methods = ['GET'])
def home_redirect():
    return render_template('homepage.html')

@app.route('/shorten', methods = ['POST'])
def url_shorten():
    error = None
    if request.method == 'POST' :
        print(request.form)
        if request.form['link'] == '' :
            error  = "link cant be empty"
            return render_template("homepage.html",error = error)
        else :
            link1 = request.form['link']
            if "http://" not in link1 :
                link1 = "http://" + link1
            url = url_generator(link1)
            print(url)
            return redirect(url_for('admin_panel',hash=url.split('/')[-1]))
    return redirect('/')

def url_generator(link):
    hash = rn + str(int(time.time()))
    url = "/r/"+hash
    r1.set(hash, link)
    r2.set(hash,0)
    print(link)
    return url

@app.route("/r/<string:hash>", methods = ['GET'])
def redirection_service(hash):
    link1 = r1.get(hash)
    print(link1)
    if link1 == None:
        return redirect("/Invalid-link")
    else :
        link = str((link1).decode("utf-8"))
        visits = int((r2.get(hash)).decode("utf-8")) + 1
        r2.set(hash,visits)
        return redirect(link)
@app.route('/a/<hash>')
def admin_panel(hash):
    print(hash)
    v = (r2.get(hash)).decode("utf-8")
    url = "/r/"+hash
    urld = "0.0.0.0:5000/r/"+hash
    del_url = "/d/"+hash
    return render_template("admin_page.html",urld = urld,views=v, url = url, del_link = del_url)

@app.route("/d/<hash>")
def delete_url(hash):
    print(hash)
    r1.delete(hash)
    r2.delete(hash)
    return redirect("/")

@app.route('/Invalid-link')
def invalid_page():
    return render_template("error_page.html")


if __name__ == '__main__' :
    app.run(host='0.0.0.0',port=5000, debug=True)