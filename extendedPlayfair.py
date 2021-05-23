from flask import Flask, render_template,request
app = Flask(__name__)

import string
def create_mat(key):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    
    #print(chars)
    #key = "playfair eg"
    mat = ['' for i in range(6)]

    i=0
    j=0

    key = ''.join(key.replace(" ",""))
    for k in key:
        if k in chars:
            mat[i]+= k
            chars = chars.replace(k,'')
            j+=1

            if j>5:
                i+=1
                j=0
    for k in chars:
        if k !='':
            mat[i]+=k

            j+=1

            if j>5:
                i+=1
                j=0
    return mat
	
def triplets(pt,f):
    pt = pt.lower()
    pt = pt.replace(" ","")
    
    i = 0
    p = []
    while i<len(pt):
        a = pt[i]
        b = ''
        c = ''
        if (i+1)==len(pt):
            b = 'y'
            c = 'z'
        elif (i+2)==len(pt):
            b = pt[i+1]
            c = 'x'
        else:
            b = pt[i+1]
            c = pt[i+2]
            
        if f==1:
            if a==c:
                p.append(a+b+'x')
                i+=2
            else:
                p.append(a+b+c)
                i+=3    
        else:
            p.append(a+b+c)
            i+=3
        
    return p
	
char_to_no = {
              'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,
              'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,
              'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,'0':27,'1':28,'2':29,'3':30,
              '4':31,'5':32,'6':33,'7':34,'8':35,'9':36
             }

def encrypt1(key1,key2,pt,f):
    mat = create_mat(key1)
    pt_triplets = triplets(pt,f)
    #print(pt_triplets)
    ct_triplets = []
    
    for p in pt_triplets:
        f = 0
        
        for i in mat:
            if(p[0] in i and p[2] in i):
                r = [x for x in mat if p[1] in x]
                ct_triplets.append(i[(i.find(p[0])+1)%6] + mat[(mat.index(r[0])+key2)%6][(r[0].find(p[1])+key2)%6] + i[(i.find(p[2])+1)%6])
                f = 1
        if f:
            continue
        
        for j in range(6):
            col = ''.join(mat[i][j] for i in range(6))
            if p[0] in col and p[2] in col:
                r = [x for x in mat if p[1] in x]
                ct_triplets.append(col[(col.find(p[0])+1)%6] + mat[(mat.index(r[0])+key2)%6][(r[0].find(p[1])+key2)%6] + col[(col.find(p[2])+1)%6])
                f = 1
        
        if f:
            continue
       
        j0 = 0
        j1 = 0
        j2 = 0
        i0 = 0
        i1 = 0
        i2 = 0
        for i in range(6):
            row = mat[i]
            if p[0] in row:
                i0 = i
                j0 = row.find(p[0])
            
            if p[2] in row:
                i1 = i
                j1 = row.find(p[2])
            
            if p[1] in row:
                i2 = (i + key2)%6
                j2 = (row.find(p[1]) + key2)%6
        ct_triplets.append(mat[i0][j1]+mat[i2][j2]+mat[i1][j0])
            
    return ct_triplets

def encrypt2(key1,key2,pt):
    fpt_triplets = []
    ct_triplets = encrypt1(key1,key2,''.join(pt),1)
    print(ct_triplets)
    
    for index,p in enumerate(ct_triplets):
        if len(fpt_triplets)==0:
            fpt_triplets.append(p)
        else:
            a2, b2, c2 = char_to_no.get(p[0]),char_to_no.get(p[1]),char_to_no.get(p[2])
            print(a2,b2,c2,end=' ')
            a3, b3, c3 = char_to_no.get(ct_triplets[index-1][0]), char_to_no.get(ct_triplets[index-1][1]), char_to_no.get(ct_triplets[index-1][2])
            print(a3,b3,c3,end=' ')
            
            a4, b4, c4 = (a2+a3), (b2+b3), (c2+c3)
            if a4==36 or a4==72:
                a4 = 36
            else:
                a4 = a4%36
            if b4==36 or b4==72:
                b4 = 36
            else:
                b4 = b4%36
            if c4==36 or c4==72:
                c4 = 36
            else:
                c4 = c4%36
                
            print(a4,b4,c4)
            a4 = list(char_to_no.keys())[list(char_to_no.values()).index(a4)]
            b4 = list(char_to_no.keys())[list(char_to_no.values()).index(b4)]
            c4 = list(char_to_no.keys())[list(char_to_no.values()).index(c4)]
            
            fpt_triplets.append(a4+b4+c4)
        print(fpt_triplets)
    return(encrypt1(key1,key2,''.join(fpt_triplets),0))

def decrypt1(key1,key2,ct_triplets):
    mat = create_mat(key1)
    pt_triplets = [] 
    for p in ct_triplets:
        f = 0
      
        for i in mat:
            if(p[0] in i and p[2] in i):
                r = [x for x in mat if p[1] in x]
                pt_triplets.append(i[(i.find(p[0])+5)%6] + mat[(mat.index(r[0])-key2)%6][(r[0].find(p[1])-key2)%6] + i[(i.find(p[2])+5)%6])
                f = 1
        if f:
            continue
        
        for j in range(6):
            col = ''.join(mat[i][j] for i in range(6))
            if p[0] in col and p[2] in col:
                r = [x for x in mat if p[1] in x]
                pt_triplets.append(col[(col.find(p[0])+5)%6] + mat[(mat.index(r[0])-key2)%6][(r[0].find(p[1])-key2)%6] + col[(col.find(p[2])+5)%6])
                f = 1
        
        if f:
            continue
       
        j0 = 0
        j1 = 0
        j2 = 0 
        i0 = 0
        i1 = 0
        i2 = 0
        for i in range(6):
            row = mat[i]
            if p[0] in row:
                i0 = i
                j0 = row.find(p[0])
            
            if p[2] in row:
                i1 = i
                j1 = row.find(p[2])
            
            if p[1] in row:
                i2 = (i - key2)%6
                j2 = (row.find(p[1]) - key2)%6
                
        pt_triplets.append(mat[i0][j1]+mat[i2][j2]+mat[i1][j0])
            
    return pt_triplets
     
def decrypt2(key1,key2,ct_triplets):
    fpt_triplets = []
    ct_triplets = decrypt1(key1,key2,ct_triplets)
    print(ct_triplets)
    
    for index,p in enumerate(ct_triplets):
        if len(fpt_triplets)==0:
            fpt_triplets.append(p)
        else:
            a2, b2, c2 = char_to_no.get(p[0]),char_to_no.get(p[1]),char_to_no.get(p[2])
            print(a2,b2,c2,end=' ')
            a3, b3, c3 = char_to_no.get(fpt_triplets[index-1][0]), char_to_no.get(fpt_triplets[index-1][1]), char_to_no.get(fpt_triplets[index-1][2])
            print(a3,b3,c3,end=' ')
           
            if a2<a3:
                a2+=36
                a4 = (a2-a3)%36
            elif a2==a3:
                a2 = 36
                a4 = a2
            else:
                a4 = (a2-a3)%36
                
            if b2<b3:
                b2+=36
                b4 = (b2-b3)%36
            elif b2==b3:
                b2 = 36
                b4 = b2
            else:
                b4 = (b2-b3)%36
                
            if c2<c3:
                c2+=36
                c4 = (c2-c3)%36
            elif c2==c3:
                c2 = 36
                c4 = c2
            else:
                c4 = (c2-c3)%36 
            
            print(a2-a3,b2-b3,c2-c3,end=' ')
            a4 = list(char_to_no.keys())[list(char_to_no.values()).index(a4)]
            b4 = list(char_to_no.keys())[list(char_to_no.values()).index(b4)]
            c4 = list(char_to_no.keys())[list(char_to_no.values()).index(c4)]
            
            print(a4,b4,c4)
            fpt_triplets.append(a4+b4+c4)
        print(fpt_triplets)
    #return(fpt_triplets)
    return(decrypt1(key1,key2,fpt_triplets))

@app.route('/ExtendedPlayfair',methods=['GET','POST'])
def ExtendedPlayfair():
	if request.method == 'POST':
		ip = request.form['plaintext']
		key_1 = request.form['key_1']
		key_2 = request.form['key_2']
		mat = create_mat(key_1)
		#print(mat)
		if request.form.get("submit_mat"):
			return render_template('ExtendedPlayfair.html', mat=mat)
		if request.form.get("submit_encrypt"):
			ct_triplets  = encrypt2(key_1,int(key_2),ip)
			ct = ''.join(ct_triplets)
			return render_template('ExtendedPlayfair.html', ct=ct,mat=mat)
		if request.form.get("submit_decrypt"):
			ct_triplets = (triplets(ip,0))
			pt = ''.join(decrypt2(key_1,int(key_2),ct_triplets))
			return render_template('ExtendedPlayfair.html', pt=pt,mat=mat)
	else:
		mat = create_mat('')		
		return render_template('ExtendedPlayfair.html',mat=mat)

if __name__ == '__main__':
	app.run(debug = True)
