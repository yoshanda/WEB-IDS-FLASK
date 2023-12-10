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

#fungsi preprocessing data
def preprocessing(file):
    #daftar kolom numerik untuk standarisasi/normalisasi data
    numeric_columns = [
        'dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl',
       'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit',
       'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean',
       'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src',
       'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm',
       'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd',
       'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports'
    ]
    
    #load dataset uji untuk klasifikasi
    file = pd.read_csv(file)

    data_unique = pd.read_csv('dataset_unsw.csv')

    file = pd.concat([file, data_unique], ignore_index=True)

    #hapus kolom yang tidak digunakan untuk proses klasifikasi
    file.drop(['id', 'attack_cat'], axis='columns', inplace=True)

    #standarisasi/normalisasi kolom numerik
    x = file.loc[:, numeric_columns].values
    normalized_data = StandardScaler().fit_transform(x)

    #reduksi dimensi data PCA
    pca = PCA(n_components=7)
    principal_components = pca.fit_transform(normalized_data)
    principal_df = pd.DataFrame(data=principal_components, columns=['Component 1', 'Component 2', 'Component 3', 'Component 4', 'Component 5', 'Component 6', 'Component 7'])

    #menggabungkan kembali data awal dengan hasil reduksi
    file_final = pd.concat([principal_df, file[['proto', 'service', 'state','label']]], axis=1)


    #hapus kolom yang tidak digunakan untuk proses klasifikasi
    file_final.drop('label', axis='columns', inplace=True)

    #transformasi data one-hot encoder
    file_final = pd.get_dummies(file_final, columns=['proto', 'service', 'state'], prefix="", prefix_sep="")
    
    file_final = file_final.iloc[:-165]

    #menjadikan file_final array
    file_final = np.array(file_final)

    #reshape file_final agar bisa diinput ke dalam model
    file_final = np.reshape(file_final, (file_final.shape[0], file_final.shape[1], 1))

    return file_final

@app.route("/", methods=["GET"])
@cross_origin()
def index() :
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
@cross_origin()
def hello_world():
    file = request.files["file"]
    data = preprocessing(file)
    model = tf.keras.models.load_model("ori_model_unsw.h5")
    result = model.predict(data)
    return jsonify(result.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0')