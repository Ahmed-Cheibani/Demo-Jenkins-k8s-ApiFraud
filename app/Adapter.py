import pandas as pd
import json


class Adapter():


    def read_data_andparse_to_df(self, request):
        transaction=request.get_json()
        return pd.DataFrame(transaction, index=[0])


    def read_data_andparse_to_dfs(self, request):
        transactions=request.get_json()
        trx = []
        for data in transactions['transactions']:
            trx.append(pd.DataFrame(data, index=[0]))
        return trx
        