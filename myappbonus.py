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
users.append([1, 'evan','code1',[0,0,200],[]])
users.append([2, 'mar','code2',[200,200,0],[]])
nmaparr=[]
green = [0,200,0]
black = [0,0,0]
red = [200,0,0]
ship_map=[green]*10+[black]*54
col=[0,0,0]
turn=0
        

# def check_hit(x,y):
#     global col
#     #if (nmaparr[x,y]==[0,200,200]).all() or (nmaparr[x,y]==[200,200,0]).all():
#     
#     #g.message1='θεση κατειλημμένη'
#     
#     if (nmaparr[x,y]==green).all():
#         
#         #nmaparr[x,y]=red
#         col=red
#         
#         #nmaparr[x,y]=red
#         
#         g.messsage1='hit'
#         #s.set_pixel(x,y,col)
#     else:
#         #nmaparr[x,y]=g.user[3]
#         col=g.user[3]
#         #s.set_pixel(x,y,col)
#     return g.message1,col
    
    
    


#print(nmaparr)


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


#@app.route('/create', methods=['POST'])
def create_board():
    
    random.shuffle(ship_map)
    rmap=random.sample(ship_map, len(ship_map))
    maparr=np.array(rmap)
    nmaparr=np.resize(maparr,(8,8,3))
    print(nmaparr)
    s.clear()
    
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
    #g.message1='αρχικοποίηση'
    #return (render_template('bonus_ships.html'))
def switch_turns():
    global turn
    if turn==0:
        turn=1
    else:
        turn=0
    return turn


@app.route('/bonus_ships/', methods=['POST','GET'])
def bonus_ships():
    
    global turn
    global nmaparr

    if not g.user:
        return redirect(url_for('logme'))
    
    if request.form.get(['action']=='Αρχικοποίηση'):
        create_board()    
    
    
    g.message1='Είναι η σειρά του πάκτη',users[turn]
    
    if request.method=='POST':
      #x=None
      #y=None
        #try:       
        x=int(request.form['horiz'])
        y=int(request.form['vert'])

            
        #except:
            #g.message1='Δεν είναι ακέραιος. Δοκίμασε ξανα'
    #except:
            
        #g.message1='Δεν είναι ακέραιος. Δοκίμασε ξανα'
            
        #else:       

            #print(nmaparr)
        if x in range (0,8) and y in range(0,8):
                #print(x,y)
                #print(x,y,nmaparr[x,y])
            
            if (nmaparr[x,y]==[0,0,200]).all() or (nmaparr[x,y]==[200,200,0]).all() or (nmaparr[x,y]==[200,0,0]).all():
#     
                g.message1='θεση κατειλημμένη'
                
#     
            if (nmaparr[x,y]==green).all():
#         
                
                
#         
#         #nmaparr[x,y]=red
#
                    nmaparr[x,y]=red
                    g.messsage1='hit'
                    s.set_pixel(x,y,red)
                    switch_turns()
            if (nmaparr[x,y]==black).all():
#         #nmaparr[x,y]=g.user[3]
                col=g.user[3]
                nmaparr[x,y]=col
                s.set_pixel(x,y,col)
                switch_turns()
            


            if x>8 or y>8:
                create_board()

            

            
            if x<0 or y<0:
                g.message1='Δώσε τιμές >0. Δοκιμασε ξανά'
    
   #g.message1='Δοκιμάστε ξανά'

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

create_board()

if __name__ == '__main__' :
    app.run(debug=True,host='0.0.0.0')
