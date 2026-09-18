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

# Ventas presencial
cantidad_ventas_por_canal = df.groupby("Canal")["ID_Venta"].count().get("Presencial", 0)
print(f"\nCantidad de ventas presencial: {cantidad_ventas_por_canal}")

# Ventas online
cantidad_ventas_online = df.groupby("Canal")["ID_Venta"].count().get("Online", 0)
print(f"\nCantidad de ventas online: {cantidad_ventas_online}")

#Total cantidad de ventas
total_cantidad_ventas = cantidad_ventas_por_canal + cantidad_ventas_online
print(f"\nTotal cantidad de ventas: {total_cantidad_ventas}")

#RTA
# Se observa que la cantidad de ventas presencial es mayor que la cantidad de ventas online, 
# lo que puede deberse a factores como la preferencia de los clientes por comprar en tiendas físicas,
# la disponibilidad de productos en línea y la confianza en el proceso de compra en línea.

#Importe promedio
importe_promedio_por_canal = df.groupby("Canal")["Importe_Final"].mean()
print("\nImporte promedio por canal:")
for canal, promedio in importe_promedio_por_canal.items():
    print(f"- {canal}: ${promedio:,.2f}")

#RTA
# Se observa que el importe promedio de las ventas online es mayor que el importe promedio de las ventas presencial.

#facturación total 
facturacion_total = df.groupby("Canal")["Importe_Final"].sum()

print("\nFacturación total por canal:")
for canal, total in facturacion_total.items():
    print(f"- {canal}: ${total:,.2f}")

print(f"Total facturación: ${facturacion_total.sum():,.2f}")

#RTA
# Se observa que la facturación total de las ventas online es mayor que la facturación total de las ventas presencial,
# lo que puede deberse a factores como la mayor cantidad de ventas online, la disponibilidad de productos exclusivos en línea
# y la comodidad de comprar desde casa.

#descuentos aplicados 
descuentos_aplicados = df.groupby("Canal")["Descuento_Porc"].mean()
print("\nDescuentos aplicados por canal:")
for canal, descuento in descuentos_aplicados.items():
    print(f"- {canal}: {descuento:.2%}")

print(f"Descuento promedio total: {descuentos_aplicados.mean():.2%}")
print(f"Total de descuentos aplicados: {descuentos_aplicados.sum():.2%}")
cantidad_descuentos_aplicados = df[df["Descuento_Porc"] > 0].shape[0]
print(f"Cantidad de descuentos aplicados: {cantidad_descuentos_aplicados}")

#RTA
# Se observa que el descuento promedio aplicado en las ventas online es mayor que el descuento promedio aplicado en las ventas presencial,
# lo que puede deberse a factores como la competencia en línea, la disponibilidad de cupones y promociones exclusivas para compras en línea, 
# y la estrategia de marketing de la empresa para incentivar las ventas online.

#costo de envío 
costo_envio_total = df.groupby("Canal")["Costo_Envio"].sum()
print("\nCosto de envío total por canal:")
for canal, costo in costo_envio_total.items():
    print(f"- {canal}: ${costo:,.2f}")

costo_envio_promedio = df.groupby("Canal")["Costo_Envio"].mean()
print("\nCosto de envío promedio por canal:")
for canal, costo in costo_envio_promedio.items():
    print(f"- {canal}: ${costo:,.2f}")

print(f"Total costo de envío: ${costo_envio_total.sum():,.2f}")
print(f"Promedio costo de envío: ${costo_envio_promedio.mean():,.2f}")

#RTA
# Se observa que el costo de envío promedio de las ventas online es mayor que el costo de envío promedio de las ventas presencial.
# Se puede deber a que las ventas online requieren envíos a domicilio, mientras que las ventas presencial no tienen este costo adicional o tal vez si dependiendo el producto.

#tipo de cliente 
tipo_cliente = df.groupby(["Canal", "Tipo_Cliente"]).size()
print("\nTipo de cliente por canal:")
for (canal, tipo), cantidad in tipo_cliente.items():
    print(f"{canal}, {tipo}: {cantidad}")

#RTA
# Se observa que el tipo de cliente más frecuente en las ventas en general es el cliente particular, en las ventas online
# hay una cierta cantidad de clientes de tipo Empresa pero aun asi no llega a superar al cliente particular.

#categorías más vendidas 

categorias_mas_vendidas = df.groupby("Canal")["Categoria"].value_counts()
print("\nCategorías más vendidas por canal:")
for (canal, categoria), cantidad in categorias_mas_vendidas.items():    
    print(f"{canal}, {categoria}: {cantidad}")

categoria_mas_venvida_por_canal = categorias_mas_vendidas.groupby(level=0).idxmax()
print("\nCategoría más vendida por canal:")
for canal, categoria in categoria_mas_venvida_por_canal.items():
    print(f"{canal}: {categoria[1]}")

#RTA
# Se observa que la categoría más vendida en las ventas presencial es la misma que en las ventas online.

"""
7. Análisis por vendedor
Analizar el desempeño de los distintos vendedores.
Pueden considerar:
•	cantidad de ventas
•	unidades vendidas
•	facturación
•	importe promedio por operación
•	calificación promedio de los clientes
No se busca solamente determinar quién posee el valor más alto, sino comparar los distintos comportamientos observados.
"""

# cantidad de ventas
cantidad_ventas = df.groupby("Vendedor")["Cantidad"].sum()
print("\nCantidad de ventas por vendedor:")
for vendedor, cantidad in cantidad_ventas.items():
    print(f"- {vendedor}: {cantidad}")

categoria_mas_vendida_por_vendedor = df.groupby("Vendedor")["Categoria"].value_counts().groupby(level=0).idxmax()
print("\nCategoría más vendida por vendedor:")
for vendedor, categoria in categoria_mas_vendida_por_vendedor.items():
    print(f"- {vendedor}: {categoria[1]}")

# unidades vendidas
productos_vendidos_por_vendedor = df.groupby(["Vendedor", "Producto"])["Cantidad"].sum()
print("\nUnidades vendidas por vendedor:")
for vendedor, productos in productos_vendidos_por_vendedor.groupby(level=0):
    print(f"{vendedor}:")
    for producto, unidades in productos.items():
        print(f"  - {producto[1]}: {unidades}")

vendedor_con_mas_unidades_vendidas = productos_vendidos_por_vendedor.groupby(level=0).sum().idxmax()
print(f"\nVendedor con más unidades vendidas:\n{vendedor_con_mas_unidades_vendidas} con {productos_vendidos_por_vendedor.groupby(level=0).sum().max()} unidades vendidas.")

# facturación
facturacion_por_vendedor = df.groupby("Vendedor")["Importe_Final"].sum()
print("\nFacturación por vendedor:")
for vendedor, facturacion in facturacion_por_vendedor.items():
    print(f"- {vendedor}: ${facturacion:,.2f}")

vendedor_con_facturacion_maxima = facturacion_por_vendedor.max()
print(f"\nVendedor con facturación máxima:\n{facturacion_por_vendedor.idxmax()} con facturación de ${vendedor_con_facturacion_maxima:,.2f}")

# importe promedio por operación
importe_promedio_por_vendedor = df.groupby("Vendedor")["Importe_Final"].mean()
print("\nImporte promedio por operación por vendedor:")
for vendedor, promedio in importe_promedio_por_vendedor.items():
    print(f"- {vendedor}: ${promedio:,.2f}")

mayor_importe_promedio = importe_promedio_por_vendedor.max()
print(f"\nVendedor con mayor importe promedio por operación:\n{importe_promedio_por_vendedor.idxmax()} con importe promedio de ${mayor_importe_promedio:,.2f}")

# calificación promedio de los clientes
calificacion_promedio_por_vendedor = df.groupby("Vendedor")["Calificacion"].mean()
print("\nCalificación promedio de los clientes por vendedor:")
for vendedor, calificacion in calificacion_promedio_por_vendedor.items():
    print(f"- {vendedor}: {calificacion:.0f}")

mayor_calificacion = calificacion_promedio_por_vendedor.max()
print(f"\nVendedor con mayor calificación promedio de los clientes:\n{calificacion_promedio_por_vendedor.idxmax()} con calificación promedio de {mayor_calificacion:.0f}")


"""
8. Productos y categorías
Realizar un análisis de las categorías y productos comercializados.
Pueden investigar:
•	categorías con mayor cantidad de unidades vendidas
•	categorías con mayor facturación
•	productos más frecuentes
•	marcas con mayor presencia
•	diferencias de precio entre categorías
"""

# categorías con mayor cantidad de unidades vendidas
categorias_vendidas = df.groupby("Categoria")["Cantidad"].sum()
categoria_maxima = categorias_vendidas.idxmax()
cantidad_categoria_maxima = categorias_vendidas.max()
print(f"\nCategoría con mayor cantidad de unidades vendidas:\n{categoria_maxima} con {cantidad_categoria_maxima} unidades vendidas.")

# categorías con mayor facturación
categorias_con_mayor_facturacion = df.groupby("Categoria")["Importe_Final"].sum().idxmax()
print(f"\nCategoría con mayor facturación:\n{categorias_con_mayor_facturacion} con ${df.groupby('Categoria')['Importe_Final'].sum().max():,.2f} en facturación.")

# productos más frecuentes
productos_mas_frecuentes = df.groupby("Producto")["Cantidad"].sum().idxmax()    
print(f"\nProducto más frecuente:\n{productos_mas_frecuentes} con {df.groupby('Producto')['Cantidad'].sum().max()} unidades vendidas.")

# marcas con mayor presencia
marcas_con_mayor_presencia = df.groupby("Marca")["Cantidad"].sum().idxmax()
print(f"\nMarca con mayor presencia:\n{marcas_con_mayor_presencia} con {df.groupby('Marca')['Cantidad'].sum().max()} unidades vendidas.")

# diferencias de precio entre categorías
diferencias_precio_entre_categorias = df.groupby("Categoria")["Precio_Unitario"].agg(["min", "max", "mean"])
print("\nDiferencias de precio entre categorías:")
for categoria, precios in diferencias_precio_entre_categorias.iterrows():
    print(f"- {categoria}: Mínimo: ${precios['min']:.2f}, Máximo: ${precios['max']:.2f}, Promedio: ${precios['mean']:.2f}")

"""
9. Visualización de datos
Construir al menos cuatro visualizaciones utilizando Matplotlib y/o Seaborn. Cada gráfico deberá responder a una pregunta concreta. 
Al menos una visualización deberá comparar grupos o categorías.
Cada gráfico deberá incluir: título, etiquetas en los ejes, leyenda cuando resulte necesaria,  escala adecuada.

Para cada visualización escribir brevemente:
•	¿Qué pregunta intenta responder?
•	¿Qué información permite observar?
"""