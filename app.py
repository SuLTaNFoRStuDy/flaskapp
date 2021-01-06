from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///post.db'

db=SQLAlchemy(app)

class BlogPost(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text, nullable=False)
    author=db.Column(db.String ,nullable=False,default='N/A')
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post '+str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts/newPost', methods=['GET','POST'])
def new_post():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        author=request.form['author'] 
        if title and content is not '':       
            postNew=BlogPost(title=title,content=content,author=author)
            db.session.add(postNew)
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('new_post.html',title=title,content=content,author=author)
            
    else :
        
        return render_template('new_post.html')

@app.route('/posts', methods=['GET'])
def posts():
    all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html',posts=all_posts)
@app.route('/posts/delete/<int:id>')
def delete(id):
    post_for_delete= BlogPost.query.get_or_404(id)
    db.session.delete(post_for_delete)
    db.session.commit()
    return redirect('/posts')
@app.route('/posts/edit/<int:id>' ,methods=['GET','POST'])
def edit(id):
    post_for_edit=BlogPost.query.get_or_404(id)

    if request.method=='POST':
        post_for_edit.title=request.form['title']
        post_for_edit.author=request.form['author']
        post_for_edit.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post_for_edit)

    


if __name__ == "__main__":
    app.run(debug=True)