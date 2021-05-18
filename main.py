from flask import Flask
from flask import request, escape
from flask import send_file
import csv

app = Flask(__name__)

@app.route("/raw",methods=['GET','POST'])
def index():
    txt = """<h1>BILAG Testing App</h1><h2>made by EB and JH</h2></br>
                **Instructions**</br> 
                1. Fill out <a href=/download>BILAG_template.csv</a> and save. </br>
                2. Open BILAG_template.csv in notepad. </br>
                3. Copy and paste to the text box below and click submit! </br> 
                (Click <a href=/>HERE</a> to submit in file) </br> </br> </br>
                <form action="/raw"method="post">
                <textarea id="input_text" name="input_text"></textarea></br>
                <input type="submit" value="Submit">
                </form>"""
    if request.method=='GET':
        return txt
    elif request.method =='POST':
        input_text = request.form['input_text']
        # print(input_text)
        if input_text:
            bilag_cat_out = bilag_categorize(input_text)
            # print("BILAGCATOUT",bilag_cat_out)
            if bilag_cat_out:
                [constitutional, mucocutaneous, neuropsychiatric, musculoskeletal, cardiorespiratory, gastrointestinal, ophthalmic, renal, hem] = bilag_cat_out
                output_text = "constitutional: "+constitutional+"</br>"+"mucocutaneous: "+mucocutaneous+"</br>"+"neuropsychiatric: "+neuropsychiatric+"</br>"+"musculoskeletal: "+musculoskeletal+"</br>"+"cardiorespiratory: "+cardiorespiratory+"</br>"+"gastrointestinal: "+gastrointestinal+"</br>"+"ophthalmic: "+ophthalmic+"</br>"+"renal: "+renal+"</br>"+"hem: "+hem
            else:
                output_text = "Invalid input. Follow the instructions and try again."
        else:
            output_text = ""
        return txt+output_text

# <input type="text" name="input_text">

# https://niceman.tistory.com/150 참고
@app.route("/",methods=['GET','POST'])
def uploadfile():
    txt = """<h1>BILAG Testing App</h1><h2>made by EB and JH</h2></br>
                **Instructions**</br> 
                1. Fill out <a href=/download>BILAG_template.csv</a> and save. </br>
                2. Upload the saved file and click submit! </br>
                (Click <a href=/raw>HERE</a> to submit in text) </br> </br> </br>
                <form action="" method="post" enctype="multipart/form-data">
                <input type = "file" name = "file"/>
                <input type="submit" value="Submit"/>
                </form>"""
    if request.method == 'GET':
        return txt
    elif request.method == 'POST':
        f = request.files['file']
        input_text=f.read().decode("utf-8-sig")
        print(input_text)
        f.close()
        # print(input_text)
        if input_text:
            bilag_cat_out = bilag_categorize(input_text)
            # print("BILAGCATOUT",bilag_cat_out)
            if bilag_cat_out:
                [constitutional, mucocutaneous, neuropsychiatric, musculoskeletal, cardiorespiratory, gastrointestinal, ophthalmic, renal, hem] = bilag_cat_out
                output_text = "constitutional: "+constitutional+"</br>"+"mucocutaneous: "+mucocutaneous+"</br>"+"neuropsychiatric: "+neuropsychiatric+"</br>"+"musculoskeletal: "+musculoskeletal+"</br>"+"cardiorespiratory: "+cardiorespiratory+"</br>"+"gastrointestinal: "+gastrointestinal+"</br>"+"ophthalmic: "+ophthalmic+"</br>"+"renal: "+renal+"</br>"+"hem: "+hem
            else:
                output_text = "Invalid input. Follow the instructions and try again."
        else:
            output_text = ""
        return txt+output_text

@app.route("/form",methods=['GET','POST'])
def form():
    txt = """<h1>BILAG Testing App</h1><h2>made by EB and JH</h2></br>
                **Instructions**</br> 
                1. Fill out the form below. </br>
                2. Click submit! </br> </br>
                * Record</br>
                0: not present</br>
                1: improving </br>
                2: same </br>
                3: worse </br>
                4: new </br> </br> </br>
                <form action=""method="post">
                <textarea id="" name="input_text"></textarea></br>
                <input type="submit" value="Submit">
                </form>"""
    if request.method=='GET':
        return txt
    elif request.method =='POST':
        input_text = request.form['input_text']
        # print(input_text)
        if input_text:
            bilag_cat_out = bilag_categorize(input_text)
            # print("BILAGCATOUT",bilag_cat_out)
            if bilag_cat_out:
                [constitutional, mucocutaneous, neuropsychiatric, musculoskeletal, cardiorespiratory, gastrointestinal, ophthalmic, renal, hem] = bilag_cat_out
                output_text = "constitutional: "+constitutional+"</br>"+"mucocutaneous: "+mucocutaneous+"</br>"+"neuropsychiatric: "+neuropsychiatric+"</br>"+"musculoskeletal: "+musculoskeletal+"</br>"+"cardiorespiratory: "+cardiorespiratory+"</br>"+"gastrointestinal: "+gastrointestinal+"</br>"+"ophthalmic: "+ophthalmic+"</br>"+"renal: "+renal+"</br>"+"hem: "+hem
            else:
                output_text = "Invalid input. Follow the instructions and try again."
        else:
            output_text = ""
        return txt+output_text

@app.route("/download",methods=['GET'])
def download():
    return send_file('BILAG_template.csv',
                     mimetype='text/csv',
                     attachment_filename='BILAG_template.csv',
                     as_attachment=True)

def bilag_categorize(input_text):
    try:
        # print("INPUTTEXTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",input_text)
        itemlist = []
        renal_p =[]
        textlines = input_text.splitlines()
        csv_reader = csv.reader(textlines, delimiter=',')
        line_count = 0
        # print("-----------------------------------------------------------------------------------------")
        # print(input_text)
        # print(textlines)
        for row in csv_reader:
            # print("linecount",line_count)
            # print("row",row)
            if line_count >=110 and line_count <=121:
                renal_p.append(float(row[2]))
            if line_count>=19 and row[1]!='':
                itemlist.append(float(row[1]))
            else:
                itemlist.append(-100)
            line_count+=1
        # print("---------------------------------------------------------------------------------------------------------")
        # print(itemlist)
        ## Constitutional
        pyr = itemlist[19]
        weight_l = itemlist[20]
        lym = itemlist[21]
        ano = itemlist[22]

        constitutional = 'N'

        # constitutional
        sum_wla = (1 if weight_l>1 else 0) + (1 if lym >1 else 0) + (1 if ano>1 else 0)
        if pyr >=2 and sum_wla >= 2:
            constitutional = 'A'
        elif pyr>=2 or sum_wla>=2:
            constitutional = 'B'
        elif pyr == 1 or weight_l >0 or lym > 0 or ano>0:
            constitutional = 'C'
        else:
            constitutional = 'DE'

        # print("constitutional",constitutional)



        ## Mucocutaneous
        se_s = itemlist[25]
        se_m = itemlist[26]
        agdema_s = itemlist[27]
        agdema_m = itemlist[28]
        mu_s=itemlist[29]
        mu_m=itemlist[30]
        panbul_s=itemlist[31]
        panbul_m=itemlist[32]
        c_vasc=itemlist[33]
        dig_inf=itemlist[34]
        alp_s=itemlist[35]
        alp_m=itemlist[36]
        puer=itemlist[37]
        splh=itemlist[38]

        mucocutaneous = 'N'

        # Mucocutaneous
        if se_s >=2 or agdema_s>=2 or mu_s>=2 or mu_s>=2 or  panbul_s >= 2 or c_vasc >=2:
            mucocutaneous = 'A'
        elif (se_s ==1 or agdema_s ==1 or mu_s ==1 or mu_s==1 or  panbul_s==1 or c_vasc==1) or (se_m>=2 or panbul_m>=2 or dig_inf>=2 or alp_s>=2):
            mucocutaneous = 'B'
        elif se_m==1 or panbul_m==1 or dig_inf==1 or alp_s==1:
            mucocutaneous = 'C'
        else:
            mucocutaneous = 'DE'

        # print("mucocutaneous",mucocutaneous)

        ## neuropsychiatric
        mening = itemlist[41]
        cvasc = itemlist[42]
        dmls = itemlist[43]
        myel = itemlist[44]
        confusion=itemlist[45]
        psychosis=itemlist[46]
        aidmlrad=itemlist[47]
        mneurop=itemlist[48]
        crneurop=itemlist[49]
        plex=itemlist[50]
        pneurop=itemlist[51]
        seizure=itemlist[52]
        sepilep=itemlist[53]
        cvd=itemlist[54]
        cogn=itemlist[55]
        movement=itemlist[56]
        auton=itemlist[57]
        cerebell=itemlist[58]
        headache=itemlist[59]
        headache_IC=itemlist[60]



        neuropsychiatric= 'N'

        # neuropsychiatric
        if mening >=2 or cvasc >=2 or dmls>=2 or myel >=2 or confusion >= 2 or psychosis >=2 or aidmlrad >=2 or mneurop >=2 or crneurop >=2 or plex >=2 or pneurop >=2 or sepilep >=2 or cerebell >=2:
            neuropsychiatric  = 'A'
        elif (mening ==1 or cvasc ==1 or dmls==1 or myel ==1 or confusion == 1 or psychosis ==1 or aidmlrad ==1 or mneurop ==1 or crneurop ==1 or plex ==1 or pneurop ==1 or sepilep ==1 or cerebell ==1) or (seizure >=2 or cvd >=2 or cogn >=2 or movement >=2 or auton >=2 or auton >=2 or cerebell >=2 or headache >=2 or headache_IC >=2):
            neuropyschiatric = 'B'
        elif seizure ==1  or cvd ==1 or cogn ==1 or movement ==1 or auton ==1 or auton ==1 or cerebell ==1 or headache ==1 or headache_IC ==1:
            neuropsychiatric = 'C'
        else:
            neuropsychiatric = 'DE'

        # print("neuropsychiatric",neuropsychiatric)


        ## musculoskeletal
        myositis_s = itemlist[63]
        myositis_m = itemlist[64]
        arthritis_s = itemlist[65]
        arthritis_mod = itemlist[66]
        arthritis_m=itemlist[67]


        musculoskeletal= 'N'

        # musculoskeletal
        if myositis_s >=2 or arthritis_s >=2:
            musculoskeletal  = 'A'
        elif (myositis_s ==1 or arthritis_s ==1) or (myositis_m >=2 or arthritis_mod >=2):
            musculoskeletal    = 'B'
        elif (myositis_m ==1 or arthritis_mod ==1)  or arthritis_m >0:
            musculoskeletal = 'C'
        else:
            musculoskeletal = 'DE'

        # print("musculoskeletal",musculoskeletal)


        ## Cariosrespiratory
        myocarditis_m= itemlist[70]
        myocarditis_s= itemlist[71]
        arrythemia = itemlist[72]
        valve= itemlist[73]
        pepce=itemlist[74]
        cardiactampon=itemlist[75]
        pedyspnea=itemlist[76]
        pulhem=itemlist[77]
        alveolitis=itemlist[78]
        shrinkinglung=itemlist[79]
        aortitis=itemlist[80]
        coropnaryvasc=itemlist[81]


        cardiorespiratory= 'N'

        # cardiorespiratory
        if myocarditis_s >=2 or arrythemia >=2 or valve >=2 or cardiactampon >=2 or pedyspnea >= 2 or pulhem >=2 or alveolitis >=2 or shrinkinglung >=2 or aortitis >=2 or coropnaryvasc >=2:
            cardiorespiratory  = 'A'
        elif (myocarditis_s ==1 or arrythemia ==1 or valve==1 or cardiactampon ==1 or pedyspnea ==1 or pulhem ==1 or alveolitis ==1 or shrinkinglung ==1 or aortitis ==1 or coropnaryvasc ==1)  or (pepce >=2 or myocarditis_m >=2):
            cardiorespiratory = 'B'
        elif pepce ==1 or myocarditis_m ==1:
            cardiorespiratory = 'C'
        else:
            cardiorespiratory = 'DE'

        # print("cardiorespiratory",cardiorespiratory)

        ## gastrointestinal
        peritonitis= itemlist[84]
        ascites= itemlist[85]
        enteritis = itemlist[86]
        malabs= itemlist[87]
        proteinlosing=itemlist[88]
        pobstruction=itemlist [89]
        hepatitis=itemlist[90]
        cholecystitis=itemlist[91]
        pancreatitis=itemlist[92]


        gastrointestinal= 'N'

        # gastrointestinal
        if peritonitis >=2 or enteritis >=2 or pobstruction >=2 or cholecystitis >=2 or pancreatitis >= 2 :
            gastrointestinal  = 'A'
        elif (peritonitis ==1 or enteritis ==1 or pobstruction ==1 or cholecystitis ==1 or pancreatitis ==1 )  or (ascites >=2 or malabs >=2 or proteinlosing>=2 or hepatitis >=2):
            gastrointestinal = 'B'
        elif ascites ==1 or malabs ==1 or proteinlosing ==1 or hepatitis ==1:
            gastrointestinal = 'C'
        else:
            gastrointestinal = 'DE'

        # print("gastrointestinal",gastrointestinal)

        ## Ophthamic
        orbitali = itemlist[95]
        keratitis_s = itemlist[96]
        keratitis_m = itemlist[97]
        antuveitis = itemlist[98]
        postuveitis_s=itemlist[99]
        postuveitis_m=itemlist[100]
        episcl=itemlist[101]
        scl_s=itemlist[102]
        scl_m=itemlist[103]
        vasoccl=itemlist[104]
        cottonwool=itemlist[105]
        oneuritis=itemlist[106]
        aioneuritis=itemlist[107]


        ophthalmic= 'N'

        # ophthamic
        if orbitali >=2 or keratitis_s >=2 or postuveitis_s>=2 or scl_s >=2 or vasoccl >= 2 or oneuritis >=2 or aioneuritis >=2:
            ophthalmic  = 'A'
        elif (orbitali ==1 or keratitis_s ==1 or postuveitis_s==1 or scl_s ==1 or vasoccl ==1 or oneuritis ==1 or aioneuritis ==1)  or (keratitis_m >=2 or antuveitis >=2 or postuveitis_m >=2 or scl_m >=2):
            ophthalmic = 'B'
        elif (keratitis_m ==1 or antuveitis ==1 or postuveitis_m ==1 or scl_m ==1) or (episcl> 0 or cottonwool >0):
            ophthalmic = 'C'
        else:
            ophthalmic = 'DE'

        # print("ophthalmic",ophthalmic)


        ## Renal
        SBP_c = itemlist[110]
        DBP_c = itemlist[111]
        accBP_c = itemlist[112]
        udipstick_c = itemlist[113]
        uACR_c=1.131*itemlist[114]
        uPCR_c=1.131*itemlist[115]
        u24hour_c=itemlist[116]
        NS_c=itemlist[117]
        sCr_c=88.42*itemlist[118]
        GFR_c=itemlist[119]
        uSed_c=itemlist[120]
        Hist_c = itemlist[121]


        SBP_p = renal_p[0]
        DBP_p = renal_p[1]
        accBP_p = renal_p[2]
        udipstick_p = renal_p[3]
        uACR_p=1.131*renal_p[4]
        uPCR_p=1.131*renal_p[5]
        u24hour_p=renal_p[6]
        NS_p=renal_p[7]
        sCr_p=88.42*renal_p[8]
        GFR_p=renal_p[9]
        uSed_p=renal_p[10]
        Hist_p = renal_p[11]


        renal= 'N'

        # renal

        A1 = (udipstick_c - udipstick_p >= 2) or (u24hour_c>1 and u24hour_c>0.75*u24hour_p) or (uPCR_c>100 and uPCR_c>0.75*uPCR_p) or (uACR_c>100 and uACR_c>0.75*uACR_p)
        A2 = True if accBP_c == 1 else False
        A3 = (sCr_c>130 and sCr_c>1.3*sCr_p) or (GFR_c<80 and GFR_c<0.67*GFR_p) or (GFR_c<50 and (GFR_p>50 or GFR_p==-1))
        A4 = True if uSed_c == 1 else False
        A5 = True if Hist_c == 1 else False
        A6 = True if NS_c == 1 else False

        B1 = A1 or A2 or A3 or A4 or A5 or A6
        B2 = (udipstick_c>=2 and udipstick_c-udipstick_p==1) or (u24hour_c>=0.5 and u24hour_c>0.75*u24hour_p) or (uPCR_c>=50 and uPCR_c>0.75*uPCR_p) and (uACR_c>=50 and uACR_c>0.75*uACR_p)
        B3 = sCr_c >= 130 and sCr_c>1.15*sCr_p and sCr_c<1.3*sCr_p

        C1=(udipstick_c>=1) or (u24hour_c>0.25) or (uPCR_c>25) or (uACR_c>25)
        C2= (SBP_c>140) and (SBP_c-SBP_p>30) and (DBP_c>90) and(DBP_c-DBP_p>15)
        # category A
        if (A1 or A4 or A5) and A1+A2+A3+A4+A5+A6>=2:
            renal = 'A'

        # category B
        elif B1 or B2 or B3:
            renal = 'B'

        #category C
        elif C1 or C2:

            renal = 'C'
        else:
            renal = 'DE'

        # print("renal",renal)

        ## hematology
        Hb_c = itemlist[124]
        WBC_c = itemlist[125]/1000
        Neut_c = itemlist[126]/1000
        Lymph_c = itemlist[127]/1000
        Plt_c=itemlist[128]
        TTP_c=itemlist[129]
        Hemolysis_c=itemlist[130]
        Coombs_c=itemlist[131]

        hem= 'N'

        # Hematologic 

        if (TTP_c >1) or (Hemolysis_c==1 and Hb_c <8) or (Plt_c <25): 
            hem = 'A' 
        elif (TTP_c==1) or (Hemolysis_c==1 and Hb_c >=8 and Hb_c <9.9) or (Hemolysis_c==0 and Hb_c <8) or (WBC_c<1.0) or (Neut_c< 0.5) or (Plt_c >=25 and Plt_c <49):
            hem = 'B' 
        elif (Hemolysis_c==1 and Hb_c >10) or (Hemolysis_c==0 and Hb_c>8 and  Hb_c<10.9) or (WBC_c>1.0 and WBC_c <3.9) or (Neut_c> 0.5 and Neut_c>1.9)  or (Lymph_c <1.0) (Plt_c >=50 and Plt_c <149) or (Coombs_c==1):
            hem= 'C' 
        else:
            hem = 'DE'

        # print("hematology", hem)

        return [constitutional, mucocutaneous, neuropsychiatric, musculoskeletal, cardiorespiratory, gastrointestinal, ophthalmic, renal, hem]
    
    except:
        return []

    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)