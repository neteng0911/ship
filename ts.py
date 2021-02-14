# Εισάγουμε το framework flask
from flask import Flask,render_template,request,session,g,url_for,redirect

# Εισάγουμε τη βιβλιοθήκη sense_emu (ή sense_hat)
from sense_hat import SenseHat
s=SenseHat()
s.low_light=False
s.clear()

import random # Εισάγουμε τη βιβλιοθήκη random.
green=[0,200,0] # Για τις θέσεις των στόχων χρησιμοποιούμε το πράσινο χρώμα,
black=[0,0,0]   # ενώ κανένα χρώμα για τις υπόλοιπες θέσεις. 
# Δημιουργούμε τη λίστα μεγέθους 64 στοιχείων
# που περιλαμβάνουν 10 θέσεις-στόχους:
shipmap=[green]*10+[black]*54

# Ορισμός επιπλέον χρωμάτων:
blue=[0,0,200] # μονού παίκτη (μπλε)
red=[200,0,0]  # ζυγού παίκτη (κόκκινο)
bluehit=[0,200,200] # μονού παίκτη που «χτύπησε» πλοίο (κυανό)
redhit=[200,200,0]  # ζυγού παίκτη που «χτύπησε» πλοίο (κίτρινο)

# Δημιουργούμε μια λίστα που περιέχει μικρότερες
# λίστες με τα στοιχεία του κάθε χρήστη.
# Αρχικοποιούμε τη λίστα users:
users= []
# Με την append() προσθέτουμε κάθε χρήστη ως
# μια μικρότερη λίστα αποτελούμενη από τρία πεδία.
# Το πρώτο πεδίο αφορά ένα μοναδικό αριθμό (user id).
# Το δεύτερο πεδίο αφορά το όνομα του χρήστη (username).
# Τέλος, το τρίτο αφορά τον κωδικό του χρήστη (password)
users.append([1, 'faid','faid1'])
users.append([2, 'myr','myr1'])

#Δίνουμε το όνομα app στο flask
app = Flask(__name__)
app.secret_key = "Μυστικό_Κλειδί_Κρυπτογράφησης"

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

# H @app.route() της βιβλιοθήκης Flask εκτελεί τη συνάρτηση που ακολουθεί,
# ανάλογα με τη διευθυνση URL που επισκέπτεται ο χρήστης
@app.route('/')
def welcome():
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
                # Έπειτα δρομολογούμε το χρήστη στη αρχική σελίδα.
                return redirect(url_for('welcome'))
    return render_template('login.html')

@app.route('/sense')
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('info.html')

@app.route('/ships', methods=['POST','GET'])
def ship_play():
    if not g.user:
        return redirect(url_for('logme'))
    # Τα περιεχόμενα της παρακάτω if θα εκτελεστούν
    # όταν ο χρήστης πατήσει το κουμπί ΑΠΟΣΤΟΛΗ...
    if request.method=='POST':
        # Αποθηκεύουμε τις τιμές που έχει δώσει
        # ο χρήστης στις αντίστοιχες μεταβλητές
        # αφού τις μετατρέψουμε σε ακέραιους
        # αριθμούς με τη χρήση της int():
        x = int(request.form['column'])
        y = int(request.form['row'])
        # Εκτελούμε τη συνάρτηση s.clear() ώστε να
        # να εμφανιστεί το επιλεγμένο χρώμα στη
        # συστοιχία LED.
        if x>7:
            s.clear()
            random.shuffle(shipmap)
            s.set_pixels(shipmap)
        else:
            s.set_pixel(x, y, 0, 0, 200)
    return render_template('ships.html')

@app.route('/bonus_ships/', methods=['POST','GET'])
def bonus_play():
    if not g.user:
        return redirect(url_for('logme'))
    # Μέτρηση των LED της συστοιχίας πριν την «κίνηση» του παίκτη.
    led_count()
    # Επιλογή χρωμάτων παικτών μονού - ζυγού παίκτη.
    # Η παράσταση g.user[0]%2 παίρνει την τιμή 0 για ζυγό και 1 για μονό παίκτη.
    # Τη χρησιμοποιώ λοιπόν ως δείκτη στις κατάλληλα διαμορφωμένες λίστες,
    # ώστε να «επιλεγεί» το σωστό χρώμα και στη μεταβλητή κειμένου g.color,
    # αλλά και στην μεταβλητή RGB color, γλιτώνοντας έτσι τα if...else!
    g.color=['ΚΟΚΚΙΝΟ', 'ΜΠΛΕ'][g.user[0]%2]
    color=[red, blue][g.user[0]%2]
    # Τα περιεχόμενα της παρακάτω if θα εκτελεστούν
    # όταν ο χρήστης πατήσει το κουμπί ΑΠΟΣΤΟΛΗ...
    if request.method=='POST':
        # Αποθηκεύουμε τις τιμές που έχει δώσει
        # ο χρήστης στις αντίστοιχες μεταβλητές:
        x = request.form['column']
        y = request.form['row']
        # Ελέγχω αν η τιμή του x είναι φυσικός αριθμός >7 για να ξεκινήσει νέο παιχνίδι,
        # πριν και ανεξάρτητα από του y για να λειτουργεί με ό,τι βάλει (ή δεν βάλει) ο παίκτης στο y.
        if x.isdigit():
            # Δεν μετατρέπω την μεταβλητή σε ακέραια, για να μπορώ να ξαναελέγξω
            # με την isdigit() παρακάτω, που με ενδιαφέρουν και τα μηνύματα.
            if int(x)>7:
                # Εκτελούμε τη συνάρτηση s.clear() ώστε να
                # να εμφανιστεί το επιλεγμένο χρώμα στη
                # συστοιχία LED.
                s.clear()
                random.shuffle(shipmap)
                s.set_pixels(shipmap)
                return render_template('bonus_ships.html')
        # Ελέγχω αν η τιμή των x & y είναι φυσικοί αριθμοί
        if x.isdigit() and y.isdigit():
            # και τους μετατρέψουμε σε αριθμούς
            # αριθμούς με τη χρήση της int():
            x = int(x)
            y = int(y)
            # Το ότι είναι θετικοί εξασφαλίζεται με την isdigit().
            # Το x εδώ είναι έτσι κι αλλιώς <=7, λόγω του ελέγχου παραπάνω.
            if y<=7:
                current=s.get_pixel(x,y)
                if g.green==0:
                    g.message='Δεν υπάρχουν πλοία στη συστοιχία! Ξεκινήστε νέο παιχνίδι!'
                elif current==green:
                    color=[redhit, bluehit][g.user[0]%2]
                    s.set_pixel(x,y,color)
                elif current==black:
                    color=[red, blue][g.user[0]%2]
                    s.set_pixel(x,y,color)
                elif current==blue or current==bluehit:
                    g.message='Η θέση ('+str(x)+'X'+str(y)+') είναι ήδη ενεργή από το ΜΠΛΕ'
                else:
                    g.message='Η θέση ('+str(x)+'X'+str(y)+') είναι ήδη ενεργή από το ΚΟΚΚΙΝΟ'
            else:
                # εκτελείται μόνο αν 0<=x<=7 ΚΑΙ y>7
                g.message='Η τιμή στα Κάθετα πρέπει να είναι μικρότερη ή ίση του 7!'
        else:
            # εκτελείται όταν κάποιο είναι κενό/αλφαριθμητικό/μη ακέραιος
            g.message='Λανθασμένοι είσοδοι, εισάγετε 2 φυσικούς αριθμούς!'
    # Μέτρηση των LED της συστοιχίας αμέσως μετά την «κίνηση» του παίκτη.
    led_count()
    return render_template('bonus_ships.html')

def led_count():
    # Η συνάρτηση καταμετρά τα LED της συστοιχίας ανά χρώμα
    g.blue=0
    g.red=0
    g.bluehit=0
    g.redhit=0
    g.green=0
    leds=s.get_pixels()
    for i in leds:
        if i==blue:
            g.blue+=1
        if i==red:
            g.red+=1
        if i==bluehit:
            g.bluehit+=1
        if i==redhit:
            g.redhit+=1
        if i==green:
            g.green+=1
    if g.green==0 and (g.bluehit!=0 or g.redhit!=0):
        g.message='Συγχαρητήρια! Το παιχνίδι τελείωσε.'

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

# Χρησιμοποιούμε app.run(debug=True) για πρόσβαση μέσα απ'το Pi
# ή app.run(debug=False,host='0.0.0.0') για πρόσβαση από LAN/WAN
# Στην τελική εργασία ήταν app.run(debug=True)
if __name__ == '__main__' :
    app.run(debug=False,host='0.0.0.0')