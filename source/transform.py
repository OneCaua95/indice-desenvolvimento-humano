from extract import Extract

data = Extract()

class Transform:
    
    def __init__(self, data_cache: bool = True):
        self.data_cache = data_cache
        self.data = None

    def transform_data(self):
        if self.data is not None:
            return self.data
    
        df = data.get_data()
        
        columns = ["ANO", "AGREGACAO" ,"CODIGO", "NOME", "IDHM", "ESPVIDA", "IDHM_L", "IDHM_E", "IDHM_R", "GINI", "THEIL"]

        rename_columns = {
            'ANO':'Ano',
            'AGREGACAO':'Agregação',
            'CODIGO':'Código',
            'NOME':'Nome',
            'IDHM':'IDH Municipal',
            'ESPVIDA':'Expectativa de vida',
            'IDHM_L': 'IDHM Longevidade',
            'IDHM_E': 'IDHM Educação',
            'IDHM_R': 'IDHM Renda',
            'GINI': 'Índice Gini',
            'THEIL':'Índice Theil'
        }

        df = df[columns].rename(columns=rename_columns)

        self.data = df

        return df
    
    def get_data_by_country(self):
        df = self.transform_data()

        data_country = df[df['Agregação'] == "BRASIL"]

        data_country = data_country.drop(['Código','Nome'], axis=1)

        return data_country
    
    def get_data_by_state(self):
        df = self.transform_data()

        data_state = df[df['Agregação'] == 'UF']

        return data_state
    
    def get_data_by_metropolitan_region(self):
        df = self.transform_data()

        data_metropolitan = df[df['Agregação'] == 'RM_RIDE']

        return data_metropolitan
    




