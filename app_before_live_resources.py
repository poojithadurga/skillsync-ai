from flask import Flask, render_template, request, redirect
import sqlite3
from resources import RESOURCES

app = Flask(__name__)


# =========================================================
# CAREER SKILL DATABASE
# =========================================================

CAREER_SKILLS = {

    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Statistics", "Pandas", "Tableau"
    ],

    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning",
        "Pandas", "R", "Algorithms"
    ],

    "Software Developer": [
        "Python", "Java", "SQL", "Git",
        "Problem Solving", "Data Structures", "Algorithms"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript",
        "Python", "Git", "REST API"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "TensorFlow",
        "PyTorch", "SQL", "Statistics", "Deep Learning"
    ],

    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "NLP",
        "Data Structures", "Algorithms", "Git"
    ],

    "Cybersecurity Analyst": [
        "Networking", "Linux", "Python",
        "Cybersecurity", "Ethical Hacking",
        "Cryptography", "Git"
    ],

    "Cloud Engineer": [
        "AWS", "Azure", "Linux", "Networking",
        "Docker", "Kubernetes", "Python",
        "Cloud Computing", "Git"
    ],

    "DevOps Engineer": [
        "Linux", "Git", "Docker", "Kubernetes",
        "Jenkins", "AWS", "DevOps", "Python"
    ],

    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Node.js", "SQL", "REST API", "Git"
    ],

    "Computer Vision Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "Computer Vision",
        "Git"
    ],

    "Generative AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "Generative AI", "LLM", "NLP",
        "Git", "REST API"
    ],

    "Business Analyst": [
        "Excel", "SQL", "Statistics",
        "Power BI", "Tableau", "Problem Solving"
    ],

    "Network Engineer": [
        "Networking", "Linux", "Python",
        "Cloud Computing", "Cybersecurity"
    ],

    "UI/UX Designer": [
        "UI/UX", "Problem Solving"
    ]
}


# =========================================================
# BASIC RECOMMENDATIONS
# =========================================================

RECOMMENDATIONS = {

    "Python": "Learn Python programming, functions, data structures and practice coding projects.",

    "SQL": "Learn SQL queries, joins, subqueries, database operations and practice with datasets.",

    "Excel": "Learn Excel formulas, charts, pivot tables and data analysis techniques.",

    "Power BI": "Learn Power BI dashboards, data visualization, data modeling and reports.",

    "Statistics": "Study statistics, probability, distributions and statistical data analysis.",

    "Machine Learning": "Learn supervised and unsupervised learning, model training and evaluation.",

    "Pandas": "Learn Pandas for data cleaning, transformation and data analysis.",

    "Java": "Learn Java programming, object-oriented programming and application development.",

    "Git": "Learn Git and GitHub for version control, branching and collaborative development.",

    "Problem Solving": "Practice logical reasoning, coding problems and algorithmic problem solving.",

    "HTML": "Learn HTML structure, forms, semantic elements and web page development.",

    "CSS": "Learn CSS styling, layouts, Flexbox, Grid and responsive web design.",

    "JavaScript": "Learn JavaScript fundamentals, DOM manipulation and web interactivity.",

    "TensorFlow": "Learn TensorFlow, neural networks and basic deep learning model development.",

    "Deep Learning": "Learn neural networks, CNNs, RNNs and deep learning model training.",

    "PyTorch": "Learn PyTorch tensors, neural networks and deep learning model development.",

    "NLP": "Learn Natural Language Processing, text processing, embeddings and language models.",

    "R": "Learn R programming, statistical analysis and data visualization.",

    "Tableau": "Learn Tableau dashboards, data visualization and interactive reports.",

    "AWS": "Learn AWS cloud fundamentals, EC2, S3, IAM and basic cloud deployment.",

    "Azure": "Learn Microsoft Azure fundamentals, cloud services and application deployment.",

    "Linux": "Learn Linux commands, file systems, permissions and basic server administration.",

    "Docker": "Learn Docker images, containers, Dockerfiles and container deployment.",

    "Kubernetes": "Learn Kubernetes pods, services, deployments and container orchestration.",

    "Networking": "Learn TCP/IP, DNS, routing, switching and computer networking fundamentals.",

    "Cybersecurity": "Learn cybersecurity fundamentals, common threats, security controls and protection methods.",

    "Ethical Hacking": "Learn ethical hacking fundamentals, vulnerability assessment and security testing.",

    "Cryptography": "Learn encryption, hashing, digital signatures and basic cryptography concepts.",

    "React": "Learn React components, props, state and modern frontend application development.",

    "Node.js": "Learn Node.js, backend development, modules and server-side applications.",

    "REST API": "Learn REST API design, HTTP methods, JSON and application-to-application communication.",

    "Data Structures": "Learn arrays, linked lists, stacks, queues, trees, graphs and hash tables.",

    "Algorithms": "Learn searching, sorting, recursion, complexity analysis and algorithm design.",

    "Computer Vision": "Learn image processing, object detection, image classification and computer vision techniques.",

    "Generative AI": "Learn generative AI concepts, foundation models and AI application development.",

    "LLM": "Learn large language models, prompting, embeddings and LLM-based application development.",

    "Cloud Computing": "Learn cloud concepts, virtualization, storage, computing and cloud service models.",

    "DevOps": "Learn CI/CD, automation, deployment, monitoring and DevOps practices.",

    "Jenkins": "Learn Jenkins pipelines, continuous integration and continuous deployment.",

    "UI/UX": "Learn user interface design, user experience principles, wireframing and prototyping."
}


# =========================================================
# DATABASE
# =========================================================

def create_database():

    conn = sqlite3.connect("skillsync.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            degree TEXT,
            branch TEXT,
            cgpa TEXT,
            technical_skills TEXT,
            soft_skills TEXT,
            certifications TEXT,
            projects TEXT,
            interests TEXT,
            target_career TEXT,
            completed_skills TEXT
        )
    """)

    # Add the column if the database was created earlier
    try:
        conn.execute(
            "ALTER TABLE students ADD COLUMN completed_skills TEXT"
        )
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


# =========================================================
# HOME / PROFILE + ANALYSIS
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        degree = request.form["degree"]
        branch = request.form["branch"]
        cgpa = request.form["cgpa"]
        technical_skills = request.form["technical_skills"]
        soft_skills = request.form["soft_skills"]
        certifications = request.form["certifications"]
        projects = request.form["projects"]
        interests = request.form["interests"]
        target_career = request.form["target_career"]

        # Initially no skills are completed
        completed_skills = ""

        # Save student profile
        conn = sqlite3.connect("skillsync.db")

        conn.execute("""
            INSERT INTO students
            (
                name,
                degree,
                branch,
                cgpa,
                technical_skills,
                soft_skills,
                certifications,
                projects,
                interests,
                target_career,
                completed_skills
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            degree,
            branch,
            cgpa,
            technical_skills,
            soft_skills,
            certifications,
            projects,
            interests,
            target_career,
            completed_skills
        ))

        conn.commit()
        conn.close()

        # Convert student skills into lowercase set
        student_skills = {
            skill.strip().lower()
            for skill in technical_skills.split(",")
            if skill.strip()
        }

        # Get skills required for selected career
        required_skills = CAREER_SKILLS.get(
            target_career.strip(),
            []
        )

        matched_skills = []
        missing_skills = []

        # Compare student skills with career skills
        for skill in required_skills:

            if skill.lower() in student_skills:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        # Calculate readiness score
        if required_skills:

            readiness_score = round(
                (len(matched_skills) / len(required_skills)) * 100
            )

        else:
            readiness_score = 0

        # Generate personalized recommendations
        recommendations = []

        for skill in missing_skills:

            recommendation = RECOMMENDATIONS.get(
                skill,
                "Find a suitable course and practice this skill."
            )

            resource = RESOURCES.get(skill)

            recommendations.append({
                "skill": skill,

                "recommendation": recommendation,

                "course": (
                    resource["course"]
                    if resource
                    else "Recommended learning resource"
                ),

                "project": (
                    resource["project"]
                    if resource
                    else "Practice project related to this skill"
                ),

                "certification": (
                    resource["certification"]
                    if resource
                    else "Relevant certification"
                ),

                "level": (
                    resource["level"]
                    if resource
                    else "Beginner"
                )
            })

                # Redirect to results page
        return redirect("/results")

    return render_template("profile.html")
    # =========================================================
# RESULTS PAGE
# =========================================================

@app.route("/results")
def results():

    conn = sqlite3.connect("skillsync.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC LIMIT 1"
    )

    student = cursor.fetchone()

    conn.close()

    if student:

        name = student[1]
        technical_skills = student[5]
        target_career = student[10]

        student_skills = {
            skill.strip().lower()
            for skill in technical_skills.split(",")
            if skill.strip()
        }

        required_skills = CAREER_SKILLS.get(
            target_career,
            []
        )

        matched_skills = []
        missing_skills = []

        for skill in required_skills:

            if skill.lower() in student_skills:
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

        if required_skills:

            readiness_score = round(
                (len(matched_skills) / len(required_skills)) * 100
            )

        else:

            readiness_score = 0

        recommendations = []

        for skill in missing_skills:

            resource = RESOURCES.get(skill)

            recommendations.append({
                "skill": skill,

                "recommendation": RECOMMENDATIONS.get(
                    skill,
                    "Find a suitable course and practice this skill."
                ),

                "course": (
                    resource["course"]
                    if resource
                    else "Recommended learning resource"
                ),

                "project": (
                    resource["project"]
                    if resource
                    else "Practice project related to this skill"
                ),

                "certification": (
                    resource["certification"]
                    if resource
                    else "Relevant certification"
                ),

                "level": (
                    resource["level"]
                    if resource
                    else "Beginner"
                )
            })

        return render_template(
            "result.html",
            name=name,
            career=target_career,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            score=readiness_score,
            recommendations=recommendations
        )

    return redirect("/")






# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("skillsync.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC LIMIT 1"
    )

    student = cursor.fetchone()

    conn.close()

    if student:

        name = student[1]
        technical_skills = student[5]
        target_career = student[10]
        completed_skills_text = student[11] or ""

        # Student's original skills
        student_skills = {
            skill.strip().lower()
            for skill in technical_skills.split(",")
            if skill.strip()
        }

        # Skills completed by the student
        completed_skills = {
            skill.strip().lower()
            for skill in completed_skills_text.split(",")
            if skill.strip()
        }

        # Career requirements
        required_skills = CAREER_SKILLS.get(
            target_career,
            []
        )

        # Skills the student currently has
        matched_skills = []

        for skill in required_skills:
            if skill.lower() in student_skills:
                matched_skills.append(skill)

        # Add completed skills to matched skills
        for skill in required_skills:
            if (
                skill.lower() in completed_skills
                and skill not in matched_skills
            ):
                matched_skills.append(skill)

        # Skills still remaining
        missing_skills = [
            skill
            for skill in required_skills
            if skill not in matched_skills
        ]

        # Calculate readiness score
        if required_skills:

            readiness_score = round(
                len(matched_skills)
                / len(required_skills)
                * 100
            )

        else:
            readiness_score = 0

        # Recommendations only for remaining skills
        recommendations = []

        for skill in missing_skills:

            if skill in RESOURCES:

                recommendations.append({
                    "skill": skill,
                    "course": RESOURCES[skill]["course"],
                    "project": RESOURCES[skill]["project"],
                    "certification": RESOURCES[skill]["certification"],
                    "level": RESOURCES[skill]["level"]
                })

        return render_template(
            "dashboard.html",
            student=student,
            name=name,
            target_career=target_career,
            readiness_score=readiness_score,
            matched_count=len(matched_skills),
            improve_count=len(missing_skills),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            recommendations=recommendations
        )

    return render_template(
        "dashboard.html",
        student=None,
        name="Student",
        target_career="Not selected",
        readiness_score=0,
        matched_count=0,
        improve_count=0,
        matched_skills=[],
        missing_skills=[],
        recommendations=[]
    )
# =========================================================
# MARK SKILL AS COMPLETED
# =========================================================

@app.route("/complete/<skill>")
def complete_skill(skill):

    conn = sqlite3.connect("skillsync.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, completed_skills FROM students ORDER BY id DESC LIMIT 1"
    )

    student = cursor.fetchone()

    if student:
        student_id = student[0]
        completed = student[1] or ""

        completed_list = [
            item.strip()
            for item in completed.split(",")
            if item.strip()
        ]

        if skill not in completed_list:
            completed_list.append(skill)

        updated_completed = ", ".join(completed_list)

        cursor.execute(
            "UPDATE students SET completed_skills = ? WHERE id = ?",
            (updated_completed, student_id)
        )

        conn.commit()

    conn.close()

    return redirect("/dashboard")


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)



