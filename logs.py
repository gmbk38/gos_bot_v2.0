from datetime import datetime
import pandas as pd

class User_log():
    def __init__(self):
        self.id = None
        self.name = None


    def user_record(self):

        data = pd.read_excel('./users/users.xlsx', header= None).rename(columns={0 : 'id', 1 : 'name'})

        if data.shape[0] == 0:
            data = pd.DataFrame(columns=['id', 'name'])

        if data[data['id'] == self.id].shape[0] == 0:
            data.loc[data.shape[0]] = [self.id, self.name] 
            data.to_excel('./users/users.xlsx', columns= None, index= None, header= None, engine='xlsxwriter')
        else:
            pass