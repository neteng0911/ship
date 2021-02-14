#Εισάγουμε το framework flask
from flask import Flask,render_template, request, session, g, url_for, redirect
app = Flask(__name__)

from sense_hat import SenseHat
s=SenseHat()
s.low_light=True

s.clear()       # Ζητούμενο-1 :  Σβήνει τα LED στην συστοιχία 

import random   # Εισάγουμε τη βιβλιοθήκη random.
green=[0,200,0] # Για τις θέσεις των στόχων χρησιμοποιούμε το πράσινο χρώμα,
black=[0,0,0]   # ενώ κανένα χρώμα για τις υπόλοιπες θέσεις. 
# Δημιουργούμε τη λίστα μεγέθους 64 στοιχείων
# που περιλαμβάνουν 10 θέσεις-στόχους:
shipmap=[green]*10+[black]*54                 # Από τις 64 θέσεις, οι 10 είναι πράσινες

# Δημιουργούμε μια λίστα που περιέχει μικρότερες
# λίστες με τα στοιχεία του κάθε χρήστη.
# Αρχικοποιούμε τη λίστα users:
users= []
# Με την append() προσθέτουμε κάθε χρήστη ως
# μια μικρότερη λίστα αποτελούμενη από τρία πεδία. 
# Το πρώτο πεδίο αφορά ένα μοναδικό αριθμό (user id).
# Το δεύτερο πεδίο αφορά το όνομα του χρήστη (username).
# Τέλος, το τρίτο αφορά τον κωδικό του χρήστη (password)
users.append([1, 'Giannis','kodikos_Gianni'])
users.append([2, 'Maria','kodikos_Marias'])

# Ορίζουμε ένα δικό μας μυστικό κλειδί κρυπτογράφησης
app.secret_key = "Μυστικό_Κλειδί_Κρυπτογράφησης"

###############################################################################
colors = {"ΜΑΥΡΟ": [0, 0, 0], "ΑΣΠΡΟ": [255, 255, 255], "ΜΠΛΕ": [0, 0, 255],
          "KOKKINO": [255, 0, 0], "ΠΡΑΣΙΝΟ": [0, 255, 0],
          "BLUEGOAL": [0, 200, 200], "REDGOAL": [200, 200, 0]}

goal_blue = "BLUEGOAL"
goal_red = "REDGOAL"

start_game = False
msg_err1, msg_err2, all_shots, cur_shots, double_shots, activeLed = '', '', [], [], [], []

def check_in(r, c):
    ''' έλεγχος input τιμών '''
    if (r < 0 or c < 0): return False
    if (0 <= r < 8) and (c > 7): return False
    if (0 <= r < 8 and 0 <= c < 8): pass
    if r > 7 and (c <= 0 or c > 0): pass
    return True

def double_rec(all_shots, shot):
    ''' ελέγχει για διπλοεγγραφές των χτυπημάτων'''
    # Διευκρίνηση Δομής :
    # - prev : ['Αποθηκευμένο χρώμα', ['τρέχων χρώμα', x, y]]
    # - Συνολική λίστα, all_shots : ['τρέχων χρώμα', x, y] 
    prev = []             
    for h in all_shots:
        if h[1]==shot[0][1] and h[2]==shot[0][2]:
            prev.append([h[0], shot[0]])
    return prev

def get_pixels(all_shots, double_shot):
    ''' Καταμέτρηση ενεργών LEDs'''
    global msg_err1, msg_err2
    g, b, k, bg, rg, m = 10,0,0,0,0,0
    pat, msg_win, msg_b, col_err, pos_err  = '', '', '', '', ''
    color_dbl, pos_dbl = '', ''
    winner = "Συγχαρητήρια! Το παιχνίδι τελείωσε."
    pat = "Ισοπαλία! Το παιχνίδι τελείωσε."
    result = []

    if len(double_shot) > 0:   # Bonus ζητούμενο-5: εμφάνιση σχετικού μηνύματος
        color_dbl = double_shot[0][0] 
        pos_dbl = str(double_shot[0][1][1]) + 'x' + str(double_shot[0][1][2])
        if color_dbl == 'BLUEGOAL' or color_dbl == 'ΜΠΛΕ':
            color_dbl = 'ΜΠΛΕ'
            msg_err1 = "Η θέση {} είναι ήδη ενεργή από το {}".format(pos_dbl, color_dbl)
        if color_dbl == 'REDGOAL' or  color_dbl == 'KOKKINO':
            color_dbl = 'KOKKINO'
            msg_err2 = "Η θέση {} είναι ήδη ενεργή από το {}".format(pos_dbl, color_dbl)

    for x in all_shots:
        if x[0] == 'ΜΠΛΕ': b +=1
        elif x[0] == 'KOKKINO': k +=1
        elif x[0] == 'BLUEGOAL':
            bg +=1
            g -=1
        elif x[0] == 'REDGOAL':
            rg +=1
            g -=1

    msg_1 = "{} ΜΠΛΕ LED".format(b)
    msg_2 = "{} ΚΟΚΚΙΝΑ και".format(k)
    msg_3 = "Απομένουν {} πλοία (με πράσινο χρώμα)".format(g)
    msg_4 = "Το ΜΠΛΕ έχει πετύχει {} πλοία".format(bg)
    msg_5 = "Το ΚΟΚΚΙΝΟ έχει πετύχει {} πλοία".format(rg)
    if len(msg_err1) > 0:
        msg_b = msg_err1
        msg_err1 = "Η θέση {} είναι ήδη ενεργή από το {}".format(pos_dbl, color_dbl)
    if len(msg_err2) > 0:
        msg_b = msg_err2
        msg_err2 = "Η θέση {} είναι ήδη ενεργή από το {}".format(pos_dbl, color_dbl)
    
    if g==0 and bg == rg: msg_win = pat                        # Bonus ζητούμενο-6:
        
    if g==0:                                                   # Τέλος παιχνιδιού
        if bg > rg: msg_win =  winner + " Νίκησαν τα ΜΠΛΕ"     # σχετικό μήνυμα
        if bg < rg: msg_win =  winner + " Νίκησαν τα KOKKINΑ"  # σχετικό μήνυμα
    
    result.append(msg_1)
    result.append(msg_2)
    result.append(msg_3)
    result.append(msg_4)
    result.append(msg_5)
    result.append(msg_b)
    result.append(msg_win)
    return result

def display_result():
    ''' Εμφάνιση αποτελεσμάτων καταμέτρησης '''
    g.msg_1 = activeLed[0] 
    g.msg_2 = activeLed[1]
    g.msg_3 = activeLed[2]
    g.msg_4 = activeLed[3]
    g.msg_5 = activeLed[4]
    g.msg_b = activeLed[5]
    g.msg_win = activeLed[6]
    

###############################################################################
@app.before_request
def before_request():
    # Αρχικοποιούμε το αντικείμενο g.user:
    g.user=None
    g.color=''
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
                
                if (user[0] % 2) == 0: g.color = "KOKKINO"     # Bonus ζητούμενο-3: 
                else: g.color = "ΜΠΛΕ"                         # Παίχτες για ζυγά και μονά
                # Με τον ίδιο τρόπο που γνωστοποιούμε
                # τα στοιχεία του χρήστη σε όλες τις σελίδες,
                # γνωστοποιούμε και το αντικείμενο s ώστε 
                # να έχουμε πρόσβαση στα δεδομένα του Sense HAT
                g.s=s

# H @app.route() της βιβλιοθήκης Flask  εκτελεί τη συνάρτηση που ακολουθεί, 
# ανάλογα με τη διευθυνση URL που επισκέπτεται ο χρήστης
@app.route('/')                            # Ζητούμενο-2: Διαδρομή '/', 
def index():                               # αντιστοιχίζεται η Νέα σελίδα
    
    if not g.user:                         # Ζητούμενο-6: Έλεγχος σύνδεσης χρήστη
        return redirect(url_for('logme'))
    
    return render_template('index.html')   # Ζητούμενο-2: Νέα σελίδα (συνέχεια)


# Η @app.route(‘/logme’) δημιουργεί τη διεύθυνση /logme. Έτσι, όταν επισκέπτομαι 
# τη διεύθυνση http://127.0.0.1:5000/logme, εκτελείται η συνάρτηση logme(), η οποία  
# επιστρέφει τα περιεχόμενα του login.html.  Επίσης χρησιμοποιούμε το όρισμα methods 
# για να δηλώσουμε ότι μπορούμε να δεχθούμε δεδομένα από τη φόρμα μας.
@app.route('/logme', methods=['POST','GET'])
def logme():
    # Μόλις ένας χρήστης επισκέπτεται τη σελίδα login αφαιρούμε το τυχόν 
    # session cookie  που έχει 
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
                
                # Βρίσκει το χρώμα, ανάλογα το user_id του χρήστη (ζυγό ή μονό) 
                if (user[0] % 2) == 0: g.color = "KOKKINO"
                else: g.color = "ΜΠΛΕ"
                
                session['user_id'] = user[0]
                # Έπειτα δρομολογούμε το χρήστη στη σελίδα που θα 
                # είναι διαθέσιμα τα δεδομένα του sense HAT.
                return redirect(url_for('index'))
            
    return render_template('login.html')

# Εδώ η @app.route('/sense', δημιουργεί τη διεύθυνση /sense, και εκτελείται η συνάρτηση 
# sense_data(), ΑΛΛΑ ΜΟΝΟΝ ΜΕΣΩ της logme(). Αυτή είναι η λογική του προγράμματος.
# ΔΗΛΑΔΗ ΈΣΤΩ κι αν δώσω διεύθυνση : http://127.0.0.1:5000/sense, θα εκτελεστεί πρώτα
# η συνάρτηση logme(), κι αν ικανοποιηθεί ο έλεγχος θα εκτελεσθεί η sense_data()
@app.route('/sense', methods=['POST','GET'])  # Ζητούμενο-3: Διαδρομή '/sense',
def sense_data():                             # αντιστοιχίζεται με το info.html
    if not g.user:
        return redirect(url_for('logme'))
    # Τα περιεχόμενα της παρακάτω if θα εκτελεστούν
    # όταν ο χρήστης πατήσει το κουμπί ΑΠΟΣΤΟΛΗ...
    if request.method=='POST':
        s.clear() 
    return render_template('info.html')       # Ζητούμενο-3: συνέχεια


@app.route('/ships', methods=['POST','GET']) # Ζητούμενο-4: Διαδρομή '/ships',
def seafight():                              # αντιστοιχίζεται με το ships.html
    if not g.user:
        return redirect(url_for('logme'))
    
    if request.method=='POST':
        ori = int(request.form['orizontal']) #Αποθήκευση τιμής οριζόντιου άξονα  
        ver = int(request.form['vertical'])  #Αποθήκευση τιμής κάθετου άξονα
        if ori < 8:
            s.set_pixel(ori,ver,[0,0,200])   #Μπλέ εμφάνιση ενός στοιχείου LED 
        else:
            random.shuffle(shipmap)          #Τυχαία επιλογή 10 πράσινων και
                                             #54 μαύρων στοιχείων LED
            s.set_pixels(shipmap)            #Εμφάνιση λίστας στη συστοιχία LED
            
    return render_template('ships.html')     # Ζητούμενο-4: συνέχεια


@app.route('/bonus_ships/', methods=['POST','GET'])
def bonus_seafight():
    if not g.user:
        return redirect(url_for('logme'))

    global curr_player, start_game, activeLed
    
    color = g.color                              # Bonus ζητούμενο-3: Χρώμα
    curr_player = g.user[0]                      # ορισμός παίχτη

    if activeLed: display_result()               # Εμφάνιση καταμέτρησης
        
    if request.method=='POST':
        p1 = users[0][0]                         # ορισμός παίχτη
        
        try:
            ori = int(request.form['orizontal']) #Αποθήκευση τιμής οριζόντιου άξονα
            ver = int(request.form['vertical'])  #Αποθήκευση τιμής κάθετου άξονα
        except ValueError:
            g.msg_err = 'Μη αποδεκτές τιμές'
            return render_template('bonus_ships.html')

        if ori > 7:                          # Ζητούμενο-5 : 
            global all_shots, cur_shot, double_shots
            g.msg_1, g.msg_2, g.msg_3, g.msg_4, g.msg_5, g.msg_b, \
                     g.msg_win = '', '', '', '', '', '', ''
            msg_err1, msg_err2, all_shots, double_shots, activeLed = '', '', [], [], []
            start_game = True
            
            s.clear()                        # Ζητούμενο-5 : Αρχικοποίηση συστοιχίας LED 
            random.shuffle(shipmap)          #     ''        Τυχαία επιλογή 10 πράσινων
            s.set_pixels(shipmap)            #     ''        Εμφάνιση λίστας στη συστοιχία LED
            
            return render_template('bonus_ships.html')
        
        if not start_game:                          # Bonus ζητούμενο-2: Έλεγχος έναρξης  
            g.msg_err = "Έναρξη παχνιδιού: τιμή > 7 σε οριζόντιο άξονα, τυχαία τιμή σε κάθετο."
            return render_template('bonus_ships.html')
        
        valid_in = check_in(ori, ver)               # Bonus ζητούμενο-1: Έλεγχος τιμών 
        if not valid_in:
            g.msg_err = "Λανθασμένη είσοδος, δοκιμάστε ξανά"
            return render_template('bonus_ships.html')

        cur_shot = []
        color = g.color
        cur_shot.append([color, ori, ver])          # λίστα με χρώμα & τη νέα θέση
        curr_player = g.user[0]                     # Ορίζει τον παίκτη που θα παίξει            
        
        # Δομή λίστας double_shot, π.χ. : ['Αποθηκευμένο χρώμα', ['τρέχων χρώμα', x, y]]
        double_shot = []
        double_shot = double_rec(all_shots, cur_shot)       # Bonus ζητούμενο-5: Έλεγχος ήδη ενεργού LED

        if not double_shot:                                 # αν η βολή είναι μοναδική
            if shipmap[ver*8 + ori] == green:                 # εξετάζει αν βρέθηκε στόχος
                if curr_player == p1:                         # για τον παίχτη με τα μπλέ
                    s.set_pixel(ori, ver, [0,200,200])        # Bonus ζητούμενο-4: χρώμα επιτυχιμένης βολής του μπλε
                    all_shots.append([goal_blue, ori, ver])   # προσθέτει την επιτυχιμένη βολή στη συνολική λίστα
                else:
                    s.set_pixel(ori, ver, [200,200,0])        # Bonus ζητούμενο-4: χρώμα επιτυχιμένης βολής του κόκκινου
                    all_shots.append([goal_red, ori, ver])    # προσθέτει την επιτυχιμένηβολή στη συνολική λίστα
            else:                                             # αν δεν βρει στόχο
                s.set_pixel(ori, ver, colors[g.color])        # εμφανίζει τη βολή στο senseHat
                all_shots.append(cur_shot[0])                 # προσθέτει τη βολή στη συνολική λίστα
        
        # Bonus ζητούμενο-7: Καταμέτρηση ενεργών LEDs
        activeLed = get_pixels(all_shots, double_shot)
        
        # Εμφάνιση καταμέτρησης
        display_result()
        if len(activeLed[6]) > 0:               # Αν το παιχνίδι τελείωσε                       
            start_game = False
        
        return render_template('bonus_ships.html')              

    return render_template('bonus_ships.html')


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
    app.run(debug=False, host='0.0.0.0')
                        # το όρισμα ‘0.0.0.0’ πρακτικά σημαίνει ότι
                        # το flask μπορεί να δεχτεί αιτήματα από οποιαδήποτε διεύθυνση.

