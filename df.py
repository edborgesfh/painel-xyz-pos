import pandas as pd
import tabulate as tb

df_cursos = pd.read_excel('df_cursos.xlsx')

print(df_cursos['data final'])