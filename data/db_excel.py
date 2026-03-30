import pandas as pd
import sys

sys.path.insert(0, "C:\\Users\\PC\\Data\\Documents\\git\\search-interface\\config")
from microrreductor_config import microrreductor

# data = [100, 102, 104]
# data2 = {"Name": ["SpongeBob", "Patrick", "Squidward"], "Age": [30, 35, 50]}

# series = pd.Series(data, index=["a", "b", "c"])

# print(series.loc["a"])
# print(series.iloc[1])

# df = pd.DataFrame(data2, index=["Employee1", "Employee2", "Employee3"])

# # Add a new column
# df["Job"] = ["Cook", "N/A", "Cashier"]

# # Add a new row
# new_row = pd.DataFrame(
#     [{"Name": "Sandy", "Age": 28, "Job": "Engineer"}], index=["Employee4"]
# )
# df = pd.concat([df, new_row])

excel_file_path = (
    "C:/Users/PC/Data/Documents/Chamba/WESMOTOR/Reportes/Stock/Microrreductores.xlsx"
)

df = pd.read_excel(excel_file_path, sheet_name="Microrreductores")
# print(
#     df[
#         [
#             "Código",
#             "Stock Total",
#             "Marca",
#             "Conexión",
#             "Potencia",
#         ]
#     ]
# )
features = df.columns.tolist()
print(features)
