# Datathon2024

- Luis Angel López
- Franco Mendoza
- Azahel Ramírez
- Sofía Badillo

## VivaAeorbus

**Modelo de optimización y predicción de venta a bordo**
*¿Cuántos productos se van a vender por vuelo?*

Modelo predictivo para optimizar el abastecimiento de productos y así reducir el desperdicio de productos perecederos y evitar la pérdida de ventas por poco invertario o productos faltantes.

Implicaciones
- Se incluye información de ventas, inventario, precios, etc.
- Por cada vuelo poder predicir la venta de productos a bordo
- ¿Cómo se puede mejorar los tiempos de recargas?

## Ideas
- Realizar una plataforma (streamlit) donde segun un vuelo, te mencione la predicción de ventas de productos a bordo.

- Un dashboard donde se muestre la información descriptiva de ventas, inventario, precios, etc.

- Mapa interactivo/estático sobre los lugares geográficos con su producto más vendido.


## Premios
1. Monederos electrónicos para vuelos VivaAerobus
2. Experiencia y Mercancía Viva
3. Experiencia y Mercancía Viva

## Datos 
- Vuelos 2023
- Ventas de 2023


## Notas
- Se usa la nube de GCP (la nube de Google), por lo que sería bueno usar plataformas de Google como Looker.

## Metedología

* Modelo de predicción de volumen de pasajeros *(incluyendo análisis de selección del modelo y medidas de ajuste- logloss, F1 score, accuracy, precision, etc)*.


* Modelo de prediccón de venta de productos (incluyendo análisis de selección del modelo y medidas de ajuste- logloss, F1 score, accuracy, precision, etc).

Modelo ML tradicional

*Plataforma Streamlit para realizar inferencias sobre el volumen pasajeros de un vuelo y venta de productos*

* Código de python, jupyter notebooks, colabs o repositorios necesarios para ejecutar el modelo. El modelo deberá estar proyectado para predecir un mes al futuro (por vuelo, día, hora, etc) .

* Principales insights encontrados en la data.

Dashboard en Looker Studio con análisis descriptivo de los datos históricos de ventas, inventario, precios, **ruta de los aviones.**

Productos más populares en ciertas horas.

Por ejemplo, tener un mapa donde se pueda interactuar con los destinos con su producto más vendido.

* 5 ejemplos de proyecciones de ventas entre el 1 de enero de 2024 y la fecha actual para comparar con la venta real.

Análisis de Serie de timempo (ARIMA, SARIMA, etc)

* **Plus: Plan abastecimiento optimizado (En qué momento del día y en qué estación hacer la recarga de productos y qué productos)**


## Dudas
- Valores nulos en los datos de datasets de vuelo

- ¿Realmente todos loa aviones tienen la misma capacidad de productos? Hay diferencias que necesitamos considerar entre las aeronaves

si salen vavciós

eliminar productos intangibles y combos/speciales

Se pueden hasta 24 sandwiches por vuelo (24 productos perecederos)