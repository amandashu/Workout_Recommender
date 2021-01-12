from flask import Flask, render_template
app = Flask(__name__)

# dummy_data
data = [
    {
        'name': "Daniel's Upper Body...",
        #'calorie':
        #'duration': 39
        #'difficulty':,
        #'equipment':
        #'training type'
    },
    {
        'name': "HIIT Pilates Strength...",
    }

]



@app.route('/')
def recommendation_page():
    return render_template('recommendation_page.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
