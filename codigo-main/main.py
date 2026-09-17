""""
1. Importación y reconocimiento del archivoImportar la hoja Ventas utilizando Pandas.Realizar una primera 
exploración utilizando algunas de las herramientas trabajadas:

df.head()
df.shape
df.columns
df.dtypes
df.info()
df.describe()

A partir de esta exploración, responder:
•¿Cuántos registros contiene el archivo?
•¿Cuántas variables posee?
•¿Qué variables son numéricas?
•¿Qué variables son categóricas?
•¿Qué información representa cada fila?
Pueden consultartambién la hoja Diccionariopara conocer el significado de las variables.
"""
import pandas as pd

print("Importación y reconocimiento del archivo")

df = pd.read_excel("ventas_electrodomesticos_integrador.xlsx", sheet_name="Ventas")

print("Exploración inicial del DataFrame")
print(df.head())
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
print(df.describe())


#¿Cuántos registros contiene el archivo?
contar_registros = df.shape[0]
print(f"El archivo contiene {contar_registros} registros.")

#¿Cuántas variables posee?
cantidad_variables = df.shape[1]
print(f"El archivo posee {cantidad_variables} variables.")

#¿Qué variables son numéricas?
variables_numericas = df.select_dtypes(include=['number']).columns.tolist()
print(f"Las variables numéricas son: {variables_numericas}")

#¿Qué variables son categóricas?
variables_categoricas = df.select_dtypes(include=['object', 'string']).columns.tolist()
print(f"Las variables categóricas son: {variables_categoricas}")

#¿Qué información representa cada fila?
print("Cada fila representa un registro de venta de electrodomésticos, incluyendo información sobre el producto, la fecha de venta, " \
"el precio, la cantidad vendida y otros detalles relevantes.")

"""
2. Calidad y preparación de los datos 
Analizar la calidad del conjunto de datos. Deberán identificar, cuando corresponda: 
• valores faltantes 
• registros duplicados 
• posibles inconsistencias 
• tipos de datos que requieran alguna modificación 
• columnas que puedan ser útiles para realizar nuevos cálculos 
No es necesario modificar todos los datos. Deberán decidir qué operaciones son pertinentes y 
justificar brevemente las decisiones tomadas. 
"""
# Cantidad valores faltantes
valores_faltantes = df.isnull().sum()
print("\nValores faltantes por columna:")
print(valores_faltantes)

# Cantidad de valores duplicados
valores_duplicados = df.duplicated().sum()
print(f"\nNúmero de registros duplicados: {valores_duplicados}")

# Posibles inconsistencias
print("\nValores únicos de variables categóricas:")

columnas_categoricas = df.select_dtypes(include=["object", "string"]).columns

for columna in columnas_categoricas:
    print(f"\n{columna}:")
    print(df[columna].value_counts(dropna=False))

# Tipos de datos
print("\nTipos de datos:")
print(df.dtypes)

# Resumen estadístico para detectar valores sospechosos
print("\nResumen de variables numéricas:")
print(df.describe())


# Deberán decidir qué operaciones son pertinentes y 
# justificar brevemente las decisiones tomadas. 

# RTA
# - No se eliminaron registros, ya que no se encontraron filas duplicadas.

# - Se mantuvieron los valores faltantes de Medio_Pago y Calificacion, ya que no
#   contamos con información suficiente para determinar sus valores reales.

# - Los valores faltantes de Descuento_Porc se reemplazaron por 0, considerando
#   que representan operaciones en las que no se registró un descuento.

# - No se modificaron las variables de categoría, ya que no se encontraron
#   inconsistencias evidentes en sus valores.

# - Los tipos de datos se consideraron adecuados para los análisis posteriores.

"""
3. Crear nuevas variables 
A partir de las columnas existentes, crear al menos dos nuevas variables que resulten útiles 
para el análisis.  También podrían calcular el importe luego del descuento. 
A partir de estas variables pueden surgir otros cálculos o clasificaciones. Deberán explicar qué 
variables crearon y para qué pueden resultar útiles. 
"""

# Importe original de la venta antes de aplicar descuentos.
df["Importe_Bruto"] = df["Cantidad"] * df["Precio_Unitario"]

# Importe descontado sobre el valor bruto de la venta.
df["Importe_Descuento"] = (
    df["Importe_Bruto"] * df["Descuento_Porc"]
)

# Importe final luego de aplicar el descuento y sumar el costo de envío.
df["Importe_Final"] = (
    df["Importe_Bruto"]
    - df["Importe_Descuento"]
    + df["Costo_Envio"]
)

print(
    df[
        [
            "ID_Venta",
            "Cantidad",
            "Precio_Unitario",
            "Descuento_Porc",
            "Costo_Envio",
            "Importe_Bruto",
            "Importe_Descuento",
            "Importe_Final"
        ]
    ].head()
)
# Deberán explicar qué variables crearon y para qué pueden resultar útiles. 
# RTA: 
# Importe_Bruto: Representa el valor total de la venta antes de aplicar cualquier descuento.
# Importe_Descuento: Representa el monto del descuento aplicado a la venta.
# Importe_Final: Representa el valor final de la venta después de aplicar el descuento y 
# sumar el costo de envío.

"""
4. Análisis exploratorio 
Realizar un análisis general de las ventas utilizando las herramientas estadísticas trabajadas 
durante el curso. 
Pueden analizar variables como: 
• cantidad de productos vendidos 
• precio unitario 
• descuentos 
• costos de envío 
• calificaciones 
• importes de venta
"""

#cantidad de productos vendidos 
cantidad_productos_vendidos = df["Cantidad"].sum()
print(f"\nCantidad total de productos vendidos: {cantidad_productos_vendidos}")

#facturacion total
facturacion_total = df["Importe_Final"].sum()
print(f"Facturación total: {facturacion_total:.2f}")

#precio unitario 
precio_unitario_promedio = df["Precio_Unitario"].mean()
print(f"Precio unitario promedio: {precio_unitario_promedio:.2f}")

#descuentos 
descuentos_promedio = df["Descuento_Porc"].mean()
print(f"Descuento promedio: {descuentos_promedio:.2%}")

#costos de envío 
costos_envio_promedio = df["Costo_Envio"].mean()
print(f"Costo de envío promedio: {costos_envio_promedio:.2f}")

#calificaciones 
calificaciones_promedio = df["Calificacion"].mean()
print(f"Calificación promedio: {calificaciones_promedio:.2f}")

#importes de venta
importes_venta_promedio = df["Importe_Final"].mean()
print(f"Importe de venta promedio: {importes_venta_promedio:.2f}")

#venta maxima y minima
venta_maxima = df["Importe_Final"].max()
venta_minima = df["Importe_Final"].min()
print(f"Venta máxima: {venta_maxima:.2f}")
print(f"Venta mínima: {venta_minima:.2f}")

#rangos quantiles de las ventas
quantiles = df["Importe_Final"].quantile([0.25, 0.5, 0.75])
print(f"Quantiles de las ventas: \n{quantiles}")

#desviación estándar de las ventas
desviacion_estandar = df["Importe_Final"].std()
print(f"Desviación estándar de las ventas: {desviacion_estandar:.2f}")

#obtener limites superior e inferior de las ventas
q1 = df["Importe_Final"].quantile(0.25)
q3 = df["Importe_Final"].quantile(0.75)
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr
print(f"Límite inferior de las ventas: {limite_inferior:.2f}")
print(f"Límite superior de las ventas: {limite_superior:.2f}")

ventas_atipicas = df[
    (df["Importe_Final"] < limite_inferior) |
    (df["Importe_Final"] > limite_superior)
]

print("\nPosibles ventas atípicas:")
print(ventas_atipicas[["ID_Venta", "Importe_Final"]])


"""
5. Análisis por sucursal 
Analizar las ventas realizadas en las distintas sucursales. 
Pueden trabajar con preguntas como: 
• ¿Qué sucursal registra mayor cantidad de operaciones? 
• ¿Cuál presenta mayor facturación? 
• ¿Qué categorías se venden más en cada sucursal? 
• ¿Existen diferencias en el importe promedio de las ventas?
"""


#¿Qué sucursal registra mayor cantidad de operaciones?
sucursal_con_mas_operaciones = df.groupby("Sucursal")["ID_Venta"].count().idxmax()
print(f"La sucursal con más operaciones es: {sucursal_con_mas_operaciones}")

#¿Cuál presenta mayor facturación? 
sucursal_con_mayor_facturacion = df.groupby("Sucursal")["Importe_Final"].sum().idxmax()
print(f"La sucursal con mayor facturación es: {sucursal_con_mayor_facturacion}")

#¿Qué categorías se venden más en cada sucursal? 
# categorias_por_sucursal = df.groupby("Sucursal")["Categoria"].value_counts().groupby(level=0).idxmax()
# print("\nCategorías más vendidas por sucursal:")

# for sucursal, categoria in categorias_por_sucursal.items():
#     print(f"{sucursal}: {categoria[1]}")


conteo_categorias = df.groupby("Sucursal")["Categoria"].value_counts()

maximos = conteo_categorias.groupby(level=0).transform("max")

categorias_por_sucursal = conteo_categorias[conteo_categorias == maximos]

print("\nCategorías más vendidas por sucursal:")

for (sucursal, categoria), cantidad in categorias_por_sucursal.items():
    print(f"{sucursal}: {categoria} ({cantidad} ventas)")

#¿Existen diferencias en el importe promedio de las ventas?
diferencias_ventas = df.groupby("Sucursal")["Importe_Final"].mean()

print("\nImporte promedio de las ventas por sucursal:")

for sucursal, promedio in diferencias_ventas.items():
    print(f"{sucursal}: ${promedio:.2f}")

#RTA 
# Si existen diferencias en el importe promedio de las ventas entre las sucursales, 
# lo que puede deberse a factores como la ubicación, el tipo de clientes, la competencia y 
# las estrategias de marketing implementadas por cada sucursal.

"""
6. Canal online y presencial 
Comparar las ventas realizadas mediante los canales: Online y Presencial 
Analizar al menos dos aspectos. 
• cantidad de ventas 
• importe promedio 
• facturación total 
• descuentos aplicados 
• costo de envío 
• tipo de cliente 
• categorías más vendidas 
Escribir una breve interpretación de las diferencias observadas. 
"""
#cantidad de ventas 
cantidad_ventas_por_canal = df.groupby("Canal")["ID_Venta"].count()
print(f"\nCantidad de ventas por canal: {cantidad_ventas_por_canal}")
cantidad_ventas_online = df.groupby("Canal")["ID_Venta"].count().get("Online", 0)
print(f"\nCantidad de ventas online: {cantidad_ventas_online}")

#importe promedio 
importe_promedio_por_canal = df.groupby("Canal")["Importe_Final"].mean()
print(f"\nImporte promedio por canal: {importe_promedio_por_canal}")

for canal, promedio in importe_promedio_por_canal.items():
    print(f"{canal}: ${promedio:.2f}")

#facturación total 

#descuentos aplicados 

#costo de envío 

#tipo de cliente 

#categorías más vendidas 


