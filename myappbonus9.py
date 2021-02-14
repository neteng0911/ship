# Εισάγουμε το framework flask
from flask import Flask,render_template,request,session,g,url_for,redirect

# Εισάγουμε τη βιβλιοθήκη sense_emu (ή sense_hat)
from sense_hat import SenseHat
import random
import numpy as np

s=SenseHat()
s.set_rotation(180)
s.lowlight=False
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
#nmaparr=[]
green = [0,200,0]
black = [0,0,0]
red = [200,0,0]
ship_map=[green]*63+[black]*1
col=[0,0,0]
turn = 0
      


#Δίνουμε το όνομα app στο flask
app = Flask(__name__)
app.secret_key = "vag1"

s.clear()
@app.before_request
def before_request():
    # Αρχικοποιούμε το αντικείμενο g.user:
    g.user=None
    g.message1=''
    
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



def create_board():
    #global nmaparr
    nmaparr=[]
    nmaparr=random.shuffle(ship_map)
    print(nmaparr)
#     rmap=random.sample(ship_map, len(ship_map))
#     maparr=np.array(rmap)
#     nmaparr=np.resize(maparr,(8,8,3))
    #print(nmaparr)
    s.clear()
   
#     
#     for y, row in enumerate(nmaparr):
#         for x, value in enumerate(row):
#             s.set_pixel(x,y,value)
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
    
    g.green=0
    g.redhit=0
    g.bluehit=0
    g.blue=0
    g.red=0
    
#     for y, row in enumerate(nmaparr):
#         for x, value in enumerate(row):
#             if nmaparr[x,y]==green:
#                 g.green+=1
#             if nmaparr[x,y]==redhit:
#                 g.redhit+=1
#             if nmaparr[x,y]==bluehit:
#                 g.bluehit+=1
#             if nmaparr[x,y]==red:
#                 g.red+=1
#             if nmaparr[x,y]==blue:
#                 g.blue+=1
            
#     
#     
#     cboard=s.get_pixels()
#     for i in cboard:
#         if i==green:
#             g.green+=1
#         if i==redhit:
#             g.redhit+=1
#         if i==bluehit:
#             g.bluehit+=1
#         if i==blue:
#             g.blue+=1
#         if i==red:
#             g.red+=1
    g.message='Το σκορ του παίκτη '+str(users[0][1])+' είναι '+str(g.redhit)+'\n Το σκορ του παίκτη '+str(users[1][1])+' είναι '+str(g.bluehit)
     
    if g.green==0:
        g.message_turn='Το παιχνίδι τελείωσε'
        if g.redhit>g.bluehit:
            g.message='κέρδισε ο '+str(users[0][1])
        else:
            g.message='κέρδισε ο '+str(users[1][1])
       
            

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
    global nmaparr
    g.color=['ΚΟΚΚΙΝΟ', 'ΜΠΛΕ'][g.user[0]%2]
    color=[red, blue][g.user[0]%2]
    if not g.user:
        return redirect(url_for('logme'))
    
    #if request.form.get(['action']=='Αρχικοποίηση'):
        #create_board()    
            
    if request.method=='POST':
        x=request.form['horiz']
        y=request.form['vert']
      #x=None
      #y=None
        if x.isdigit():
            if int(x)>7:
                create_board()
                g.message1='Νέο παιχνίδι'

            
                
        if x.isdigit() and y.isdigit():
            x=int(x)
            y=int(y)
            if not nmaparr:
                print("nmaparr is empty")
            
            if y <=7:
                #print(x,y,nmaparr[x,y])
                

                choice=nmaparr[x][y]
                #print(choice)
                if choice==green:
                    color=[redhit,bluehit][g.user[0]%2]                  
                    s.set_pixel(x,y,color)
                    g.messsage_hit='hit'
                    nmaparr[x][y]=black
                    switch_turns()
                    
                    
                elif choice==black:
                    color=[red,blue][g.user[0]%2]
                    s.set_pixel(x,y,color)
                    nmaparr[x][y]=color
                    switch_turns()

                   
                elif choice==red or choice==redhit:
                    g.message1='Το σημείο (' +str(x)+'X' +str(y)+')είναι δεσμευμένο από τον παίκτη '+str(users[0][1])
                else:
                    g.message1='Το σημείο (' +str(x)+'X' +str(y)+')είναι δεσμευμένο από τον παίκτη '+str(users[1][1])
            else:
                g.message1='H τιμή στα κατακόρυφα πρέπει να είναι <7'

        else:
            g.message1='Η τιμή που εισάγατε δεν είναι αριθμός'
    count()
    if g.green!=0:
        
        g.message_turn='Είναι η σειρά του παίκτη',users[turn][1]
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

nmaparr=create_board()

if __name__ == '__main__' :
    app.run(debug=True,host='0.0.0.0')

