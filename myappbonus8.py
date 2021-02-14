# Εισάγουμε το framework flask
from flask import Flask,render_template,request,session,g,url_for,redirect,flash
import time

# Εισάγουμε τη βιβλιοθήκη sense_emu (ή sense_hat)
from sense_hat import SenseHat
import random
import numpy as np

s=SenseHat()
s1=SenseHat()
s.set_rotation(180)
s.lowlight=False
# Ορισμός επιπλέον χρωμάτων:
blue=[0,0,200] # μονού παίκτη (μπλε)
red=[200,0,0]  # ζυγού παίκτη (κόκκινο)
bluehit=[0,200,200] # μονού παίκτη που «χτύπησε» πλοίο (κυανό)
redhit=[200,100,0]  # ζυγού παίκτη που «χτύπησε» πλοίο (κίτρινο)
ships = [0,4,0]
black = [0,0,0]

# Δημιουργούμε μια λίστα που περιέχει μικρότερες
# λίστες με τα στοιχεία του κάθε χρήστη.
# Αρχικοποιούμε τη λίστα users:
users= []
# Με την append() προσθέτουμε κάθε χρήστη ως
# μια μικρότερη λίστα αποτελούμενη από τρία πεδία.
# Το πρώτο πεδίο αφορά ένα μοναδικό αριθμό (user id).
# Το δεύτερο πεδίο αφορά το όνομα του χρήστη (username).
# Τέλος, το τρίτο αφορά τον κωδικό του χρήστη (password)
users.append([1, 'faid','faid1',blue,bluehit])
users.append([2, 'myr','myr1',red,redhit])
nmaparr=[]

nships=13
nblack=64-nships
ship_map=[ships]*nships+[black]*nblack
col=[0,0,0]
turn = 0
#message_hit='testmessagehit'
        


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
@app.route('/restart')
def restart():
    nmaparr=create_board()
    #return render_template('restart.html',nmaparr=nmaparr)
    return redirect(url_for('bonus_ships',nmaparr=nmaparr))
    

    
    
@app.route('/sense')
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    
        

        
    return render_template('info.html')  



def create_board():
    
    random.shuffle(ship_map)
    rmap=random.sample(ship_map, len(ship_map))
    maparr=np.array(rmap)
    nmaparr=np.resize(maparr,(8,8,3))
    #print(nmaparr)
    s.clear()
    #s.set_pixel(nmaparr)
#     
    for y, row in enumerate(nmaparr):
        for x, value in enumerate(row):
            s.set_pixel(x,y,value)
    #print(nmaparr[0,0])
    #print(nmaparr)
    #print(type(nmaparr))
    #if (nmaparr[0][0]==green).all():
        #print('true')
    #else:
        #print('false')
    #print(nmaparr)
    #return render_template('nmaparr.html')
    #return render_template('bonus_ships.html')
    return nmaparr



def count():
    
    g.ships=0
    g.redhit=0
    g.bluehit=0
    g.blue=0
    g.red=0
    
    cboard=s.get_pixels()
    for i in cboard:
        if i==ships:
            g.ships+=1
        if i==redhit:
            g.redhit+=1
        if i==bluehit:
            g.bluehit+=1
        if i==blue:
            g.blue+=1
        if i==red:
            g.red+=1
    g.message='Το σκορ του παίκτη '+str(users[0][1])+' είναι '+str(g.bluehit)+'\n Το σκορ του παίκτη '+str(users[1][1])+' είναι '+str(g.redhit)+' \n απομένουν '+str(64-g.ships-g.redhit-g.bluehit-g.blue-g.red)+' κενές θέσεις'



    if g.ships!=0:
        if g.redhit+g.ships<g.bluehit:
            g.message_turn='κέρδισε ο παίκτης '+str(users[0][1])
        if g.bluehit+g.ships<g.redhit:
            g.message_turn='κέρδισε ο παίκτης '+str(users[1][1])

    if g.ships==0:
        g.message_turn='Το παιχνίδι τελείωσε'
        if g.redhit>g.bluehit:
            g.message='κέρδισε ο '+str(users[1][1])
        else:
            g.message='κέρδισε ο '+str(users[0][1])
    

    else:
        return
        
    
    
        
       
            

def switch_turns():
    global turn
    
    if turn==0:
        turn=1
    else:
        turn=0
    
    return redirect(url_for('bonus_ships')),turn

@app.route('/bonus_ships/', methods=['POST','GET'])
def bonus_ships():
    global turn
    message_hit=''
    
    
    #g.color=['ΚΟΚΚΙΝΟ', 'ΜΠΛΕ'][g.user[0]%2]
    #color=[red, blue][g.user[0]%2]
    color=g.user
    if not g.user:
        return redirect(url_for('logme'))
    
    #if request.form.get(['action']=='Αρχικοποίηση'):
        #create_board()    
            
    if request.method=='POST':
        x=request.form['horiz']
        y=request.form['vert']
      #x=None
      #y=None
        if x.isdigit() and y.isdigit():
            if int(x)<=7 and int(y)<=7:
 
                x=int(x)
                y=int(y)
                #print(nmaparr)
                
                    #print(x,y,nmaparr[x,y])
                choice=s.get_pixel(x,y)
                
                if choice==ships:
                    
                    #color=[redhit,bluehit][g.user[0]%2]
                    color=g.user[4]
                    #s1.show_message(str(g.user[1]),text_colour=color)
                    #time.sleep(1)
                    s.set_pixel(x,y,color)
                    
                    message_hit='Βρήκες στόχο'
                    

                    
                    switch_turns()
                elif choice==black:
                    #color=[red,blue][g.user[0]%2]
                    color=g.user[3]
                    s.set_pixel(x,y,color)
                    
                    switch_turns()

                   
                elif choice==red or choice==redhit:
                    g.message1='Το σημείο (' +str(x)+'X' +str(y)+')είναι δεσμευμένο από τον παίκτη '+str(users[1][1])
                else:
                    g.message1='Το σημείο (' +str(x)+'X' +str(y)+')είναι δεσμευμένο από τον παίκτη '+str(users[0][1])

            else:
                g.message1='Εισάγετε τιμές <8'
        else:
            g.message1='Η τιμή που εισάγατε δεν είναι αριθμός'
    count()
    if g.ships!=0:
        
        g.message_turn='Είναι η σειρά του παίκτη',users[turn][1]
    return render_template('bonus_ships.html',message_hit=message_hit)

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

nmaparr=create_board()

if __name__ == '__main__' :
    app.run(debug=True,host='0.0.0.0')

