from pandas import read_excel

class Extract:

    def __init__(self, data_cache: bool = True):
        self.data_cache = data_cache
        self.data = None
        
    """
    def extract_data(self):
        file = 'https://www.undp.org/sites/g/files/zskgke326/files/2023-07/base_de_dados.xlsx'

        df = read_excel(file)

        return df

    """ 

    def extract_data(self):
        file = 'data/base_de_dados.xlsx'

        df = read_excel(file)

        return df

    def get_data(self):
        if self.data is not None:
            return self.data
        
        df = self.extract_data()

        self.data = df

        return df
