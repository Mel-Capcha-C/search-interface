import xlwings as xw

wb = xw.Book(
    r"C:\Users\PC\Data\Documents\Chamba\WESMOTOR\Reportes\Stock\Stock Categoria v08_20_Marzo_2026.xlsx"
)
sheet = wb.sheets["Microrreductores"]
print(sheet["A1"].value)
