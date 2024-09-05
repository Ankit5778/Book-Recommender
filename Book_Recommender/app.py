from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
 
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html',
                            book_name=list(popular_df['Book-Title'].values),
                            book_author=list(popular_df['Book-Author'].values),
                            image=list(popular_df['Image-URL-M'].values),
                            num_rating=list(popular_df['num_ratings'].values),
                            avg_rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_book', methods=['POST'])
def recommend_recommend():
    user_input=request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    similar_item=sorted(list(enumerate(similarity_score[index])),key= lambda x:x[1],reverse=True)[1:9]

    data=[]
    for i in similar_item:
        item=[]
        temp=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)


if __name__=="__main__":
    app.run(debug=True)