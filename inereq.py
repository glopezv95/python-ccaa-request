import bs4
import requests
from io import StringIO
import pandas as pd
import rapidfuzz

class CCAA:
    
    DEFAULT_COLUMN_NAMES: list[str] = ['id_ccaa', 'ccaa', 'id_prov', 'prov']
    
    def __init__(
        self,
        url: str = 'https://ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm'
        ) -> None:
        
        self.url: str = url
        self.status_code: int | None = None
        self.error_message: str | None = None
        self.soup: bs4.BeautifulSoup | None = None
        self.html_table: bs4.element.Tag | None = None
        
        self.pd_table: pd.DataFrame | None = None
        
        self.fetch_data()
        
    def __str__(self):
        
        print(f'\nClase {self.__class__.__name__} {type(self)}\n')
        
        print(f'Información del request')
        print('----------')
        print(f'URL del request: {self.url}')
        print(f'Status HTTP: {self.status_code}')
        print(f'Error en el request GET: {self.error_message}\n')
        
        print(f'Información de la tabla')
        print('----------')
        print(f'Columnas ({len(self.pd_table.columns)}): {self.pd_table.columns.values}')
        print(f'Número de filas: {len(self.pd_table)}\n')

        return f'{self.pd_table.head()}\n'
        
    def fetch_data(
        self,
        to_pd: bool = True,
        custom_column_names: list[str] | None = None
        ) -> None:
        
        try:
            
            response: requests.Response = requests.get(self.url)
            self.status_code = response.status_code
            
            if self.status_code == 200:
                
                self.soup = bs4.BeautifulSoup(response.content, 'html.parser')
                self.html_table = self.soup.select('table')[0]
                
                if to_pd:
                
                    self.pd_table = pd.read_html(StringIO(str(self.html_table)))[0]
                    self._clean_pd_table(custom_column_names = custom_column_names)
            
            else:
                
                self.error_message = f'Error en el GET request HTTP: {self.status_code}. \
                    Compruebe que el parámetro CCAA.url está definido como una ruta válida'
                
        except requests.RequestException as e:
            self.error_message = f'Error en el request: {e}'
            
    def _clean_pd_table(
        self,
        custom_column_names: list[str]
        ) -> None:
        
        if custom_column_names is not None and len(self.pd_table.columns) == len(self.custom_column_names):
            self.pd_table.columns = self.custom_column_names
        
        else:
            self.pd_table.columns = self.DEFAULT_COLUMN_NAMES
        
        mask: pd.DataFrame = self.pd_table.apply(lambda row: row.astype(str).str.lower().str.contains('ciudad').any(), axis = 1)
        self.pd_table = self.pd_table[~mask]
        
        float_id_cols: list[str] = [col for col in self.pd_table.columns if self.pd_table[col].astype(str).str.contains('.0').any()]
        self.pd_table[float_id_cols] = self.pd_table[float_id_cols].apply(
            lambda col: col.astype(str).str.replace('.0', '').str.zfill(2))
        
        self.pd_table = self.pd_table.astype(str)
    
    def normalise_values(
        self,
        ref_column_name: str,
        dirty_values: list[str],
        sim_threshold: int = 85
        ) -> list[str]:
        
        reference_list = self.pd_table[ref_column_name].unique().tolist()
        cleaned_values: list[str] = []
        
        for index, value in enumerate(dirty_values):
            
            best_match, score = rapidfuzz.process.extractOne(value, reference_list)
            
            if score >= sim_threshold:
                cleaned_values.append(best_match)
                
            else:
                
                print(f'No se encontró un valor de reemplazo adecuado para el item {index} de la lista ({value}).\n\
                    Pruebe a modificar el valor de similitud {sim_threshold} o eliminar caracteres especiales')
                cleaned_values.append(value)
                
        return cleaned_values