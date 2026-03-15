import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
from flask import Flask, render_template, session, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sqlite3

def init_db():

    conn = sqlite3.connect("gradvox.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        feedback TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


app = Flask(__name__)
app.secret_key = "gradvox_secret"

# Home
@app.route("/")
def index():
    return render_template("getstarted.html")


# Name page
@app.route("/name", methods=["GET","POST"])
def name():

    if request.method == "POST":

        username = request.form.get("username")

        if username:   # make sure name is not empty
            session["username"] = username

        return redirect(url_for("dashboard"))

    return render_template("name.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    username = session.get("username","User")

    return render_template(
        "dashboard.html",
        username=username
    )

with open("questions.json") as f:
    db = json.load(f)

current_test=[]


@app.route("/aptitude")
def aptitude():
    return render_template("aptitude.html")


@app.route("/start_test/<category>")
def start_test(category):

    global current_test

    category_questions=[q for q in db if q["category"]==category]

    current_test = random.sample(category_questions, min(50, len(category_questions)))

    return render_template(
        "aptitude_test.html",
        questions=current_test
    )


@app.route("/submit_test", methods=["POST"])
def submit_test():

    score = 0
    results = []

    for i, q in enumerate(current_test, 1):

        user = request.form.get(f"q{i}", "Not Answered")
        correct = q["answer"]

        if user == correct:
            score += 1

        results.append({
            "question": q["question"],
            "user": user,
            "correct": correct
        })

    return render_template(
        "aptitude_result.html",
        score=score,
        total=len(current_test),
        results=results
    )
# Company Preparation
@app.route("/company_prep")
def company_prep():
    companies = [
        {
            "name": "Google",
            "focus": "Algorithms and System Design",
            "logo": "/static/google.png",
            "link": "/company_detail/Google"
        },
        {
            "name": "Amazon",
            "focus": "Data Structures and Leadership Principles",
            "logo": "/static/amazon.png",
            "link": "/company_detail/Amazon"
        },
        {   # <-- Added opening brace here
            "name": "Microsoft",
            "focus": "Coding and Problem Solving",
            "logo": "/static/microsoft.png",
            "link": "/company_detail/Microsoft"
        },
        {
            "name": "TCS",
            "focus": "Aptitude and Technical Basics",
            "logo": "/static/tcs.png",
            "link": "/company_detail/TCS"
        }
    ]

    return render_template(
        "company_prep.html",
        companies=companies
    )

# Company detail page route
@app.route("/company_detail/<company_name>")
def company_detail(company_name):
    skills = {
        "Google": ["Algorithms", "System Design", "Coding", "Problem Solving"],
        "Amazon": ["Data Structures", "Leadership Principles", "Coding", "Aptitude"],
        "Microsoft": ["Coding", "Problem Solving", "System Design", "Technical Questions"],
        "TCS": ["Aptitude", "Technical Basics", "Coding"],
        "Other": ["General Aptitude", "Coding", "Technical Knowledge"]
    }

    company_skills = skills.get(company_name, skills["Other"])
    logo = f"/static/{company_name.lower()}.png" if company_name != "Other" else "/static/other.png"

    return render_template(
        "company_detail.html",
        company_name=company_name,
        company_skills=company_skills,
        logo=logo
    )
# Interview Setup
@app.route("/interview_setup", methods=["GET","POST"])
def interview_setup():

    if request.method == "POST":

        domain = request.form.get("domain")

        session["domain"] = domain

        return redirect(url_for("interview"))

    return render_template("interview_setup.html")


# Question Bank
questions_bank = {

"Data Scientist":[
"What is Machine Learning?",
"What is the difference between supervised and unsupervised learning?",
"What is feature engineering?",
"What is feature selection?",
"What is overfitting?",
"What is underfitting?",
"What is clustering in machine learning?",
"What is the difference between classification and regression?",
"What is a decision tree?",
"What is random forest?",
"What is the purpose of training and testing datasets?",
"What is data preprocessing?"
],

"Data Analyst":[
"What is data analysis?",
"What is data cleaning?",
"What is exploratory data analysis?",
"What is data visualization?",
"What tools are commonly used in data analysis?",
"What is the difference between data analysis and data analytics?",
"What is a dashboard in data analytics?",
"What is the purpose of SQL in data analysis?",
"What is the difference between structured and unstructured data?",
"What is a pivot table?",
],

"HR Interview":[
"Tell me about yourself",
"What are your strengths?",
"What are your weaknesses?",
"Why should we hire you?",
"Why do you want to work for our company?",
"Where do you see yourself in 5 years?",
"What motivates you?",
"Describe a challenging situation you faced",
"How do you handle stress at work?",
"Tell me about a time you worked in a team",
"What are your career goals?",
],

"Full Stack Developer":[
"What is the difference between frontend and backend development?",
"What is REST API?",
"What is the MVC architecture?",
"What is the difference between SQL and NoSQL databases?",
"What is version control and why is Git used?",
"What is the difference between client-side and server-side rendering?",
"What is middleware in web development?",
"What is authentication and authorization?",
"What is the difference between monolithic and microservices architecture?",
"What are environment variables in web applications?"
],

"Backend Developer":[
"What is an API and how does it work?",
"What is the difference between GET, POST, PUT and DELETE methods?",
"What is database indexing?",
"What is the difference between SQL and NoSQL databases?",
"What is caching and why is it important?",
"What is a server and how does it work?",
"What is authentication using JWT?",
"What is load balancing?",
"What is microservices architecture?",
"What are asynchronous operations in backend development?"
],

"Frontend Developer":[
"What is HTML, CSS and JavaScript?",
"What is the DOM (Document Object Model)?",
"What is responsive web design?",
"What is the difference between inline, block and inline-block elements?",
"What is CSS Flexbox?",
"What is CSS Grid?",
"What is event delegation in JavaScript?",
"What is the difference between let, const and var?",
"What is a JavaScript framework?",
"What is the purpose of React or Angular in frontend development?"
],

"Software Engineer":[
"What is object oriented programming?",
"What are the principles of OOP?",
"What is polymorphism?",
"What is inheritance in programming?",
"What is encapsulation?",
"What is abstraction?",
"What is a design pattern?",
"What is the difference between stack and queue?",
"What is multithreading?",
"What is the difference between compiled and interpreted languages?"
],

"UI/UX Designer":[
"What is the difference between UI and UX design?",
"What is wireframing?",
"What is a prototype in design?",
"What is user-centered design?",
"What is usability testing?",
"What is the importance of typography in UI design?",
"What is the difference between low fidelity and high fidelity prototypes?",
"What is design thinking?",
"What is accessibility in UI design?",
"What tools are commonly used in UI/UX design?"
]
}


# Interview Page
@app.route("/interview")
def interview():

    domain = session.get("domain")

    questions = questions_bank.get(domain, [])

    return render_template(
        "interview.html",
        domain=domain,
        questions=questions
    )


# Result
@app.route("/result")
def result():

    domain = session.get("domain")

    score = random.randint(60,95)

    skills = {

    "Communication": random.randint(60,90),
    "Technical": random.randint(65,95),
    "Confidence": random.randint(60,90),
    "Clarity": random.randint(60,90)

    }

    domain_skills = {

    "Data Scientist":[
"Python programming",
"Statistics and probability",
"Machine learning algorithms",
"Data preprocessing and cleaning",
"Feature engineering",
"Model evaluation techniques",
"Data visualization",
"SQL and database querying",
"Deep learning basics",
"Business problem solving"
],

"Data Analyst":[
"Excel and spreadsheet analysis",
"SQL and database querying",
"Data cleaning and preprocessing",
"Exploratory data analysis (EDA)",
"Data visualization tools",
"Dashboard creation",
"Statistical analysis",
"Business intelligence tools",
"Reporting and storytelling with data",
"Problem solving with data"
],

"HR Interview":[
"Communication skills",
"Confidence and body language",
"Self introduction and storytelling",
"Teamwork and collaboration",
"Problem solving ability",
"Leadership qualities",
"Time management",
"Adaptability",
"Professional ethics",
"Career goal clarity"
],

"Full Stack Developer":[
"HTML CSS and JavaScript",
"Frontend frameworks like React",
"Backend development with Node.js or similar",
"REST API development",
"Database design (SQL or NoSQL)",
"Authentication and security",
"Version control with Git",
"Deployment and cloud basics",
"Debugging and testing",
"System design fundamentals"
],

"Backend Developer":[
"Server side programming",
"API design and development",
"Database management",
"Authentication and authorization",
"Performance optimization",
"Caching techniques",
"Microservices architecture",
"Cloud services basics",
"Security best practices",
"Scalability concepts"
],

"Frontend Developer":[
"HTML CSS and JavaScript",
"Responsive web design",
"JavaScript frameworks like React or Angular",
"DOM manipulation",
"State management",
"Cross browser compatibility",
"Web performance optimization",
"UI component design",
"Accessibility standards",
"Frontend debugging"
],

"Software Engineer":[
"Data structures and algorithms",
"Object oriented programming",
"System design",
"Version control (Git)",
"Software development lifecycle",
"Problem solving and coding",
"Testing and debugging",
"Database concepts",
"Operating system basics",
"Networking fundamentals"
],

"UI/UX Designer":[
"User research",
"Wireframing and prototyping",
"Design thinking",
"User interface design",
"Typography and color theory",
"Usability testing",
"Interaction design",
"Accessibility principles",
"Design tools like Figma",
"User centered design"
]


    }

    attempt = {

    "domain":domain,
    "score":score

    }

    history = session.get("history",[])

    history.append(attempt)

    session["history"] = history

    return render_template(
"result.html",
score=score,
domain=domain,
domain_skills=domain_skills,
speaking_time=75,
confidence=85,
clarity=80,
answer_length=70
)


# History
@app.route("/history")
def history():

    history = session.get("history",[])

    return render_template(
        "history.html",
        history=history
    )


# Analytics
@app.route("/analytics")
def analytics():

    history = session.get("history",[])

    scores = [attempt["score"] for attempt in history]

    avg_score = 0

    if scores:
        avg_score = sum(scores)/len(scores)

    return render_template(
        "analytics.html",
        scores=scores,
        avg_score=avg_score
    )


# Feedback
@app.route("/feedback", methods=["GET","POST"])
def feedback():

    if request.method == "POST":

        rating = request.form.get("rating")

        return redirect(url_for("dashboard"))

    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():

    username = session.get("username")

    rating = request.form.get("rating")
    feedback = request.form.get("feedback")

    conn = sqlite3.connect("gradvox.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feedback (name, rating, feedback) VALUES (?, ?, ?)",
        (username, rating, feedback)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/owner_feedback")
def owner_feedback():

    conn = sqlite3.connect("gradvox.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, rating, feedback FROM feedback")

    data = cursor.fetchall()

    conn.close()

    return render_template("owner_feedback.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)