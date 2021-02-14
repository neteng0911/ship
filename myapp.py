# Εισάγουμε το framework flask
from flask import Flask,render_template,request,session,g,url_for,redirect

# Εισάγουμε τη βιβλιοθήκη sense_emu (ή sense_hat)
from sense_hat import SenseHat
import random
import numpy as np

s=SenseHat()
s.set_rotation(180)

# Δημιουργούμε μια λίστα που περιέχει μικρότερες
# λίστες με τα στοιχεία του κάθε χρήστη.
# Αρχικοποιούμε τη λίστα users:
users= []
# Με την append() προσθέτουμε κάθε χρήστη ως
# μια μικρότερη λίστα αποτελούμενη από τρία πεδία.
# Το πρώτο πεδίο αφορά ένα μοναδικό αριθμό (user id).
# Το δεύτερο πεδίο αφορά το όνομα του χρήστη (username).
# Τέλος, το τρίτο αφορά τον κωδικό του χρήστη (password)
users.append([1, 'evan','code1'])
users.append([2, 'Maria','kodikos_Marias'])
nmaparr=[]
green = [0,200,0]
black = [0,0,0]
ship_map=[green]*10+[black]*54


def create_board():
    global nmaparr
    random.shuffle(ship_map)
    rmap=random.sample(ship_map, len(ship_map))
    maparr=np.array(rmap)
    nmaparr=np.resize(maparr,(8,8,3))
    return nmaparr


create_board()
#print(nmaparr)


#Δίνουμε το όνομα app στο flask
app = Flask(__name__)
app.secret_key = "vag1"
s.clear()
@app.before_request
def before_request():
    # Αρχικοποιούμε το αντικείμενο g.user:
    g.user=None
    # Ελέγχουμε αν είναι κατειλημμένο το session cookie,
    # αν δηλαδή έχει συνδεθεί ο χρήστης.
    if 'user_id' in session:
        # Διατρέχουμε τη λίστα των χρηστών, ώστε να εντοπίσουμε σε ποιον ανήκει
        # ο μοναδικός αριθμός που είναι αποθηκευμένος στο session cookie.
        for user in users:
            if user[0] == session['user_id']:
                # Αποθηκεύουμε τη λίστα που αφορά τα στοιχεία του χρήστη
                # στο g.user, ώστε να είναι προσβάσιμα από όλες τις σελίδες.
                g.user = user
                # Με τον ίδιο τρόπο που γνωστοποιούμε
                # τα στοιχεία του χρήστη σε όλες τις σελίδες,
                # γνωστοποιούμε και το αντικείμενο s ώστε
                # να έχουμε πρόσβαση στα δεδομένα του Sense HAT
                g.s=s

# H @app.route() της βιβλιοθήκης Flask  εκτελεί τη συνάρτηση που ακολουθεί,
# ανάλογα με τη διευθυνση URL που επισκέπτεται ο χρήστης
@app.route('/')
def check_user():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('index.html')
        

# Χρησιμοποιούμε το όρισμα methods για να δηλώσουμε ότι
# μπορούμε να δεχθούμε δεδομένα από τη φόρμα μας.
@app.route('/logme', methods=['POST','GET'])
def logme():
    # Μόλις ένας χρήστης επισκέπτεται τη σελίδα login
    # αφαιρούμε το τυχόν session cookie που έχει
    # αποθηκευτεί στον υπολογιστή του χρήστη.
    # Το πετυχαίνουμε αυτό με τη session.pop:
    session.pop('user_id', None)
    # Τα περιεχόμενα της παρακάτω if θα εκτελεστούν όταν ο
    # χρήστης επιλέξει το κουμπί ΕΙΣΟΔΟΣ.
    if request.method=='POST':
        # Αποθηκεύουμε το username και τον κωδικό
        # από το χρήστη που συμπλήρωσε τη φόρμα.
        username = request.form['username']
        password = request.form['password']
        for user in users:
           # Διατρέχουμε τη λίστα των χρηστών για να ελέγξουμε αν υπάρχει
           # χρήστης σύμφωνα με τα στοιχεία που λάβαμε από την φόρμα:
            if user[1]==username and user[2]==password:
                # Αν τα στοιχεία που έχει δώσει ο χρήστης είναι σωστά,
                # τότε δημιουργούμε ένα session cookie με όνομα user_id
                # και αποθηκεύουμε εκεί το μοναδικό αριθμό που αντιστοιχεί
                # στο χρήστη.
                session['user_id'] = user[0]
                # Έπειτα δρομολογούμε το χρήστη στη σελίδα που θα
                # είναι διαθέσιμα τα δεδομένα του sense HAT.
                return redirect(url_for('check_user'))
    return render_template('login.html')

@app.route('/sense')
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    
        

        
    return render_template('info.html')  

@app.route('/ships', methods=['POST','GET'])
def ships():
     
     if not g.user:
         return redirect(url_for('logme'))
        
            
     if request.method=='POST':
         
        x=int(request.form['horiz'])
        y=int(request.form['vert'])
        if x<=7:
            s.set_pixel(x,y,[0,0,255])
        else:
            s.clear()
            create_board()
            for y, row in enumerate(nmaparr):
                for x, value in enumerate(row):
                    s.set_pixel(x,y,value)
                    
                    
                
        
        
     return render_template('ships.html')

@app.context_processor
# Αρχικά φτιάχνουμε μια βασική συνάρτηση:
def a_processor():
    # Μέσα στη βασική συνάρτηση υλοποιούμε μια συνάρτηση με όνομα
    # roundv()  (ή κάποιο άλλο όνομα της επιλογής σας) που δέχεται
    # δύο ορίσματα: μια τιμή και το πλήθος των δεκαδικών ψηφίων.
    def roundv(value,digits):
        # Τα ορίσματα αυτά τα περνάμε στη συνάρτηση round() της
        #  python, η οποία κάνει τη ζητούμενη εργασία.
        return round(value,digits)
    # Τέλος, η βασική συνάρτηση επιστρέφει υπό μορφή λεξικού το όνομα της
    # συνάρτησης roundv() που υλοποιήσαμε, ώστε να είναι διαθέσιμη στα templates.
    return {'roundv':roundv}

if __name__ == '__main__' :
    app.run(debug=False,host='0.0.0.0')
