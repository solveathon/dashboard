from utils.db import Db
from flask_bcrypt import generate_password_hash

db = Db('database.db')

judges = [
    ["davidraj.micheal@vit.ac.in", "Dr. David Raj Micheal", "judge_1", 'judge'],
    ["felix.a@vit.ac.in", "Dr. A Felix", "judge_2", 'judge'],
    ["velmathi.g@vit.ac.in", "Dr. Velmathi G", "judge_3", 'judge'],
    ["vijayalakshmi.v@vit.ac.in", "Dr. Vijayalakshmi V", "judge_4", 'judge'],
    ["raviprakash.dwivedi@vit.ac.in", "Dr. Ravi Prakash Dwivedi", "judge_5", 'judge'],
    ["ravi.v@vit.ac.in", "Dr. Ravi V", "judge_6", 'judge'],
    ["pattabiraman.v@vit.ac.in", "Dr. Pattabiraman V", "judge_7", 'judge'],
    ["suganya.g@vit.ac.in", "Dr. Suganya G", "judge_8", 'judge'],
    ["venkatesh.k@vit.ac.in", "Mr. Venkatesh", "judge_9", 'judge'],
    ["christyjackson.j@vit.ac.in", "Dr. Christy Jackson", "judge_10", 'judge'],
    ["thomasabraham.jv@vit.ac.in", "Dr. Thomas Abraham", "judge_11", 'judge'],
    ["devaprakasam.d@vit.ac.in", "Dr. Devaprakasam D", "judge_12", 'judge'],
    ["raghukiran@vit.ac.in", "Dr. Raghukiran Nadimpalli","judge_13", 'judge'],
    ["lenin.babu@vit.ac.in", "Dr. Lenin Babu M C", "judge_14", 'judge'],
    ["jamuna.k@vit.ac.in", "Dr. Jamuna K", "judge_15", 'judge'],
    ["sathiyanarayanan.s@vit.ac.in", "Dr. Sekar Sathiya Narayanan", "judge_16", 'judge'],
    ["mohan.kuppusamy@vit.ac.in", "Dr. Mohan K", "judge_17", 'judge'],
    ["mohan.r@vit.ac.in", "Dr. Mohan R", "judge_18", 'judge'],
    ["saraswathi.d@vit.ac.in", "Dr. Saraswathi D", "judge_19", 'judge'],
    ["jayarangan.l@vit.ac.in", "Dr Jayarangan L", "judge_20", 'judge'],
]

for judge in judges:
    query = f"""
        INSERT INTO users (email, name, password, teamID, role) VALUES
        ('{judge[0]}', '{judge[1]}', '{generate_password_hash("judge@solveathon").decode("utf-8")}', '{judge[2]}', '{judge[3]}')
    """

    db.query(query, commit=True)

