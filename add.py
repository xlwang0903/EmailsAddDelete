from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Asunto(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    asunto=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Asunto %r>' % self.id
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        Asunto_asunto=request.form['asunto']
        Asunto_email=request.form['email']
        new_Asunto=Asunto(asunto=Asunto_asunto,email=Asunto_email)
        try:
            db.session.add(new_Asunto)
            db.session.commit()
            return redirect('/')
        except:
            return 'Hubo un error'
    else:
        asuntos=Asunto.query.order_by(Asunto.id).all()
        return render_template('Index.html', asuntos=asuntos)
@app.route('/delete/<int:id>')
def delete(id):
    asuntotodelete=Asunto.query.get_or_404(id)
    try:
        db.session.delete(asuntotodelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ha ocurrido un error al eliminar'
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    #This  name is going to be useful for the update action we have to use the name that we put below
    asunto=Asunto.query.get_or_404(id)
    if request.method=='POST':
        #Using the name that is up for update the informaction with sqlalchemy
         asunto.asunto=request.form['asunto']
         asunto.email=request.form['email']
         try:
             db.session.commit()
             #The information is update in this moment and we return to the index
             return redirect('/')
         except:
            return 'Hubo un problema'
    else:
        return render_template('update.html',asunto=asunto)




if __name__ == "__main__":
    app.run(debug=True)
