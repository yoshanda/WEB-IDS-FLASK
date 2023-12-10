from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import (StandardScaler,LabelEncoder, OneHotEncoder)
from sklearn.decomposition import PCA
import tensorflow as tf
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

#fungsi transformasi data untuk pengkategorian serangan
def change_label(data):
  data.label.replace(['apache2','back','land','neptune','mailbomb','pod','processtable','smurf','teardrop','udpstorm','worm'],'Anomali',inplace=True) #Dos
  data.label.replace(['ftp_write','guess_passwd','httptunnel','imap','multihop','named','phf','sendmail','snmpgetattack','snmpguess','spy','warezclient','warezmaster','xlock','xsnoop'],'Anomali',inplace=True) #R2L
  data.label.replace(['ipsweep','mscan','nmap','portsweep','saint','satan'],'Anomali',inplace=True) #Probe
  data.label.replace(['buffer_overflow','loadmodule','perl','ps','rootkit','sqlattack','xterm'],'Anomali',inplace=True) #u@R


#fungsi preprocessing data
def preprocessing(file):
    #kolom untuk dataset
    cols = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
        'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
        'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
        'dst_host_srv_count', 'dst_host_same_srv_rate','dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
        'dst_host_srv_rerror_rate', 'label', 'difficulty_level'
    ]

    #daftar kolom numerik untuk standarisasi/normalisasi data
    numeric_columns = [
        "duration","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
        "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells",
        "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
        "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
        "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
        "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"
    ]
    
    #load dataset uji untuk klasifikasi
    file = pd.read_csv(file, header=None)
    file.columns = cols

    data_train = pd.read_csv('df_train.csv')

    file = pd.concat([file, data_train], ignore_index=True)

    #hapus kolom yang tidak digunakan untuk proses klasifikasi
    file.drop('difficulty_level', axis='columns', inplace=True)

    #standarisasi/normalisasi kolom numerik
    x = file.loc[:, numeric_columns].values
    normalized_data = StandardScaler().fit_transform(x)

    #reduksi dimensi data PCA
    pca = PCA(n_components=7)
    principal_components = pca.fit_transform(normalized_data)
    principal_df = pd.DataFrame(data=principal_components, columns=['Component 1', 'Component 2', 'Component 3', 'Component 4', 'Component 5', 'Component 6', 'Component 7'])

    #menggabungkan kembali data awal dengan hasil reduksi
    file_final = pd.concat([principal_df, file[['protocol_type', 'service', 'flag','label']]], axis=1)

    #transformasi data pengkategorian
    change_label(file_final)

    #transformasi data labeling
    multi_label = pd.DataFrame(file_final.label)
    le2 = LabelEncoder()
    enc_label = multi_label.apply(le2.fit_transform)
    file_final['intrusion'] = enc_label

    #hapus kolom yang tidak digunakan untuk proses klasifikasi
    file_final.drop('label', axis='columns', inplace=True)

    #transformasi data one-hot encoder
    file_final = pd.get_dummies(file_final, columns=['protocol_type', 'service', 'flag'], prefix="", prefix_sep="")

    #menghapus kolom intrusion
    file_final = file_final.drop(labels=['intrusion'], axis=1)
    
    file_final = file_final.iloc[:-345]

    #menjadikan file_final array
    file_final = np.array(file_final)

    #reshape file_final agar bisa diinput ke dalam model
    file_final = np.reshape(file_final, (file_final.shape[0], file_final.shape[1], 1))

    return file_final

@app.route("/", methods=["GET"])
@cross_origin()
def index() :
    return render_template("index.html")

@app.route('/home', methods=['POST'])
@cross_origin()
def hello_world():
    file = request.files["file"]
    data = preprocessing(file)
    model = tf.keras.models.load_model("model1.h5")
    result = model.predict(data)
    return jsonify(result.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0')