from transform import Transform
import folium as fl
import glob
import re

data = Transform()

class Analysis:
    
    def get_analysis_state_and_region(self, data, year, column):
        df = data
        df = df[df['Ano'] == year]

        df_std = round(df[column].std(), 3)
        df_min = df[column].min()
        df_mean = round(df[column].mean(), 3)
        df_max = df[column].max()

        worst_value = df.loc[df[column].idxmin(), 'Nome']
        best_value = df.loc[df[column].idxmax(), 'Nome']

        return df, df_min, df_mean, df_max, df_std, worst_value, best_value
    
    def get_analysis_by_country(self, column):
        df = data.get_data_by_country()

        df_std = round(df[column].std(), 3)
        df_min = df[column].min()
        df_mean = round(df[column].mean(), 3)
        df_max = df[column].max()
        
        worst_value = df.loc[df[column].idxmin(), 'Ano']
        best_value = df.loc[df[column].idxmax(), 'Ano']

        return df, df_min, df_mean, df_max, df_std, worst_value, best_value

    def get_state_and_region_by_year(self, data, year):
        df = data
        df = df[df['Ano'] == year]

        return df
    
    def get_analysis_by_state(self, year, column):
        df = data.get_data_by_state()

        result = self.get_analysis_state_and_region(df, year, column)

        return result
    
    def get_analysis_by_region(self, year, column):
        df = data.get_data_by_metropolitan_region()

        result = self.get_analysis_state_and_region(df, year, column)

        return result
    
    def get_state_heatmap(self, year, column):
        df, *_ = self.get_analysis_by_state(year, column)
        geojson_path = glob.glob("assets/br_states.json")[0]

        estado_sigla = {
            "Rondônia": "RO", "Acre": "AC", "Amazonas": "AM", "Roraima": "RR",
            "Pará": "PA", "Amapá": "AP", "Tocantins": "TO", "Maranhão": "MA",
            "Piauí": "PI", "Ceará": "CE", "Rio Grande do Norte": "RN",
            "Paraíba": "PB", "Pernambuco": "PE", "Alagoas": "AL", "Sergipe": "SE",
            "Bahia": "BA", "Minas Gerais": "MG", "Espírito Santo": "ES",
            "Rio de Janeiro": "RJ", "São Paulo": "SP", "Paraná": "PR",
            "Santa Catarina": "SC", "Rio Grande do Sul": "RS", "Mato Grosso do Sul": "MS",
            "Mato Grosso": "MT", "Goiás": "GO", "Distrito Federal": "DF"
        }

        df['Sigla'] = df['Nome'].map(estado_sigla)
        
        if df['Sigla'].isnull().any():
            missing_states = df[df['Sigla'].isnull()]['Nome'].unique()
            print(f"Estados sem correspondência: {missing_states}")
            return None
        
        if df[column].isnull().any():
            print(f"Valores NaN encontrados na coluna {column}")
            return None

        br_map = fl.Map(location=[-15.7801, -47.9292], zoom_start=4)

        choropleth = fl.Choropleth(
            geo_data=geojson_path,
            data=df,
            columns=["Sigla", column],
            key_on="feature.properties.SIGLA",  # Chave para o arquivo GeoJSON do IBGE
            nan_fill_color="white",
            fill_color='YlOrRd',
            legend_name=f'{column} por Estado'
        )
        
        choropleth.add_to(br_map)

        return br_map
    
    def extract_region_sigla(self, nome):
        match = re.search(r'\((\w{2})\)', nome)  # Busca uma sigla entre parênteses, como "(AM)"

        return match.group(1) if match else None
   

    def get_region_heatmap(self, year, column):
        df, *_ = self.get_analysis_by_region(year, column)
        geojson_path = glob.glob("assets/br_states.json")[0]

        df['Sigla'] = df['Nome'].apply(self.extract_region_sigla)
        
        if df['Sigla'].isnull().any():
            missing_states = df[df['Sigla'].isnull()]['Nome'].unique()
            print(f"Estados sem correspondência: {missing_states}")
            return None
        
        if df[column].isnull().any():
            print(f"Valores NaN encontrados na coluna {column}")
            return None

        rm_map = fl.Map(location=[-15.7801, -47.9292], zoom_start=4)

        choropleth = fl.Choropleth(
            geo_data=geojson_path,
            data=df,
            columns=["Sigla", column],
            key_on="feature.properties.SIGLA",  # Chave para o arquivo GeoJSON do IBGE
            nan_fill_color="white",
            fill_color='YlOrRd',
            legend_name=f'{column} por Estado'
        )
        
        choropleth.add_to(rm_map)

        return rm_map
   