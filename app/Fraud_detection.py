import tensorflow as tf
import sys
import keras 
import pandas as pd 
import numpy as np
import pickle
import json
import warnings
warnings.filterwarnings('ignore')

class Fraud_detection():


    def __init__(self):
        # config = tf.ConfigProto(
        #     device_count={'GPU': 1},
        #     intra_op_parallelism_threads=1,
        #     allow_soft_placement=True
        # )
        # config.gpu_options.allow_growth = True
        # config.gpu_options.per_process_gpu_memory_fraction = 0.6
        # self.session = tf.Session(config=config)
        # keras.backend.set_session(self.session)

        self.combinaison_model=keras.models.load_model("./Models/cobinaison_model.h5")

        with open("./Models/LabelEncoders_dic.pickle","rb") as f:
            self.encoder_dic=pickle.load(f)

        with open("./Models/MinMaxScalers_dic.pickle","rb") as f:
            self.scaler_dic=pickle.load(f)

    def transformer_df(self, df):
        for c in df.columns :
            if (df[c].dtype =="object"):
                encoder = self.encoder_dic[c]
                df[c]=encoder.transform(df[c])
        return df

    def normaliser_all_columns(self, df):

        for c in df.columns :
            df[c]=self.scaler_dic[c].transform(df[c].values.reshape(-1,1))
        return df

    def reshape_x_data_3d(self, xtrain):
        return np.array(xtrain).reshape(xtrain.shape[0],xtrain.shape[1],1)

    def prepare_data(self, df):
        try :
            df.drop(['Transaction_date','Gender', 'Birth_date', 'City', 'Merchant_number', 
                    'Merchant_name', 'LIB_ACTIVITE', 'Churn_date','Account_creation_date',
                    'Ages_intervals'], axis=1, inplace=True)
        except:
            pass
        df = df[['Clinet_ID', 'Familial_status', 'Income_amount', 'Multicanal', 'Has_a_card', 'SEG', 
                'DNA_Year', 'DNA_Month', 'DNA_Day', 'Product_code', 'Account_number', 'Code_devise', 
                'Account_chapter', 'Start_of_month_amount', 'End_of_month_amount', 'Average_amount',
                'DATE_OUVERTURE_COMPTE_Year', 'DATE_OUVERTURE_COMPTE_Month', 'DATE_OUVERTURE_COMPTE_Day', 
                'DATE_FERMETURE_COMPTE_Year', 'DATE_FERMETURE_COMPTE_Month', 'DATE_FERMETURE_COMPTE_Day', 
                'Branche_code', 'Operation_code', 'Amount', 'DEV', 'Transaction_type', 'ORIGINE', 
                'Transaction_label', 'DCO_Year', 'DCO_Month', 'DCO_Day', 'Operation_category']]
        

        for c in df.columns: 
            if((c!="Familial_status")&(c!="Transaction_type")&(c!="ORIGINE")&(c!="Transaction_label")&
            (c!="Operation_category")&(c!="Has_a_card")&(c!="Multicanal")&(c!="Income_amount")):
                df[c]=df[c].astype(np.float64) # we will transform the int columns to float columns

        df=self.transformer_df(df)# we will change all categorical columns to numerical columns
        df=self.normaliser_all_columns(df)# we will make all values between 0 and 1

        return df

    def prediction(self, df ,thresh_min=1.5,tresh_max=3):
        df_reshaped = self.reshape_x_data_3d(df)


        # with self.session.as_default():
        #     with self.session.graph.as_default():
        y_pred=self.combinaison_model.predict([df,df_reshaped])

        y_dist=np.linalg.norm(df-y_pred,axis=-1)
        if((y_dist>= thresh_min)&(y_dist<= tresh_max)):
            p=0
        else:
            p=1     
        df["Prediction_Fraudulent"]=str(p)#     
        return df.to_dict(orient='records')[0]
        