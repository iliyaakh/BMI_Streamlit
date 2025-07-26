import streamlit as st
import sqlite3

con = sqlite3.connect('BMI.db')
cursor = con.cursor()

sql_creat_table = ''' CREATE TABLE IF NOT EXISTS results 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  weight INTEGER, height INTEGER, BMI INTEGER,
                  body form TEXT, idea TEXT)
                              '''
cursor.execute(sql_creat_table)
con.commit()

def insert(weight, height, bmi, body, idea):
    cursor.execute('INSERT INTO results (weight, height, bmi, body, idea) VALUES (?,?,?,?,?)',(weight, height, bmi, body, idea))
    con.commit()

def delete(id):
    cursor.execute('DELETE FROM results WHERE id = ?', (id,))
    con.commit()

def delete_all():
    cursor.execute('DELETE FROM results')
    con.commit()
    
def read_where1(id):
    cursor.execute('SELECT * FROM results WHERE id = ?', (id,))
    return cursor.fetchall()

def read_full():
    cursor.execute('SELECT * FROM results')
    return cursor.fetchall()

st.sidebar.title('seting')
seting = st.sidebar.selectbox('diagrees', ('BMI','Delete from history','Delete all history','Search by ID','Make Table','About Us'))

if seting == 'BMI':
    st.title('Welcom to your Website')
    st.write("Let's check your BMI")
    
    weight = st.number_input("Enter your weight (kg):", min_value = 1.0, max_value = 550.0, step = 0.1)
    height = st.number_input("Enter your height (m):", min_value = 0.5, max_value = 2.5, step = 0.01)
    
    if weight and height:
        col1, col2 = st.columns(2)
        bmi = weight / pow(height, 2)

        col1.metric(f'your BMI', f'{bmi:.1f}')

        if bmi <= 18.5:
            body = "Underweight"
            idea = "Consider a balanced diet to gain weight"
        elif 18.5 < bmi <= 25:
            body = "Normal"
            idea = "Your weight is in a healthy range"
        elif 25 < bmi <= 30:
            body = "Overweight"
            idea = "Consider a fitness plan to manage weight"
        else:
            body = "Obese"
            idea = "Consult a healthcare professional for guidance"

        col2.metric(f'body form', f'{body}')
        st.write(idea)

        st.title('would you like to insert it to database?')
        x = st.button('yes')
        if x:
            insert(str(weight), height, bmi, body, idea)
            st.success('insert the table')

if seting == 'Delete from history':
    st.title('Delete by ID')

    id = st.number_input("Enter ID:", min_value=1, step=1)
    
    if st.button("Delete"):
        results = read_where1(id)
        if results:
            delete(id)
            st.success(f'Record with ID {id} deleted')
        else:
            st.error(f'No record found with ID {id}')

if seting == 'Delete all history':
    st.title("Delete All History")
    if st.button("Confirm deletion"):
        delete_all()
        st.success("All records cleared")

if seting == 'Search by ID':
    id = st.number_input('Enter id :', step = 1, min_value = 1)
    if st.button('search'):
        results = read_where1(id)
        if results:
            st.dataframe(results, column_config = {"0": "ID", "1": "Weight (kg)", "2": "Height (m)", "3": "BMI", "4": "body form", "5" : "idea"})
        else:
            st.info("No records found")
            
if seting == 'Make Table':
    st.title("All BMI Records")
    data = read_full()
    if data:
        st.dataframe(data, column_config = {"0": "ID", "1": "Weight (kg)", "2": "Height (m)", "3": "BMI", "4": "body form", "5" : "idea"})
    else:
        st.info("No records in database")

if seting == 'About Us':
    st.title('About This Project')
    st.write("This Streamlit project, developed by Iliya, calculates and tracks your BMI. Store your results, view history, and manage records easily.")
    st.title('Contact Us')
    st.write('You can contact us via:')
    st.link_button('Telegram', 'https://t.me/iliya_12344')
    st.link_button('Instagram', 'https://www.instagram.com/iliyakh177?igsh=dXpkNHM2OTl6OHho')
    if st.button('Email'):
        st.write('iliyakh660@gmail.com')