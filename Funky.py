###################### concentración_final ######################################

import pandas as pd
import numpy as np

def concentración_final(archivo_csv, vol_inicial=10, vol_final=50):
    """
    Lee un archivo del Nanodrop, limpia los datos, remueve los blancos ('B') 
    y calcula la concentración final (C2) de las muestras diluidas.
    Además, registra los volúmenes utilizados para la dilución.
    """
    print(f"Procesando archivo: {archivo_csv}...")
    
    # 1. Leer el archivo
    df = pd.read_csv(archivo_csv)
    
    # 2. Filtrar columnas, quitar los blancos ('B') y crear una copia limpia
    df_clean = df.loc[df['Sample ID'] != 'B', ["Sample ID", "Nucleic Acid", "Unit"]].copy()
    
    # 3. Renombrar la columna
    df_clean = df_clean.rename(columns={'Nucleic Acid': 'C1'})
    
    # Validaciones de seguridad
    if vol_final <= 0:
        raise ValueError("El volumen final debe ser mayor a cero.")
    if vol_inicial > vol_final:
        raise ValueError("El volumen inicial no puede ser mayor al volumen final (el diluyente sería negativo).")
        
    # 4. Calcular la concentración final (C2)
    # C2 = (C1 * V1) / V2
    df_clean['C2_Final'] = (df_clean['C1'] * vol_inicial) / vol_final
    
    # 5. Agregar las columnas de registro
    df_clean['Vol_inicial'] = vol_inicial
    df_clean['Vol_final'] = vol_final
    df_clean['Vol_diluyente'] = vol_final - vol_inicial
    
    print("¡Procesamiento terminado! Tabla lista con todos los parámetros de la dilución.")
    
    # Devolvemos el DataFrame listo para usarse o exportarse
    return df_clean

###################### Volumen inicial ######################################

def volumen_inicial(archivo_csv, vol_final=50, concentración_final=10):
    """
    Lee un archivo del Nanodrop, limpia los datos y calcula:
    1. Vol_inicial (V1): Volumen de muestra pura.
    2. Vol_diluyente: Volumen de líquido para completar el vol_final.
    3. C2_objetivo: La concentración final deseada para tener el registro.
    """
    print(f"Procesando archivo: {archivo_csv}...")
    
    # 1. Leer el archivo
    df = pd.read_csv(archivo_csv)
    
    # 2. Filtrar columnas y quitar blancos
    df_clean = df.loc[df['Sample ID'] != 'B', ["Sample ID", "Nucleic Acid", "Unit"]].copy()
    
    # 3. Renombrar la columna de concentración inicial
    df_clean = df_clean.rename(columns={'Nucleic Acid': 'C1'})
    
    # Validación de seguridad
    if vol_final <= 0:
        raise ValueError("El volumen final debe ser mayor a cero.")
        
    # 4. Calcular el Volumen inicial (V1)
    df_clean['Vol_inicial'] = np.where(
        df_clean['C1'] > 0, 
        (concentración_final * vol_final) / df_clean['C1'], 
        0
    )
    
    # 5. Calcular el Volumen de Diluyente (lo que falta para completar)
    df_clean['Vol_diluyente'] = vol_final - df_clean['Vol_inicial']
    
    # Marcamos como nulos (NaN) los volúmenes de diluyente negativos
    # (muestras que ya están más diluidas que tu objetivo)
    df_clean.loc[df_clean['Vol_diluyente'] < 0, 'Vol_diluyente'] = np.nan
    
    # 6. Registrar la concentración final deseada (C2)
    # Esto asignará el mismo valor a todas las filas de esta nueva columna
    df_clean['C2'] = concentración_final
    
    print("¡Procesamiento terminado! Tabla lista con volúmenes y registro de concentración.")
    
    return df_clean

###################### Volumen final ######################################

def volumen_final(archivo_csv, vol_inicial=10, concentración_final=10):
    """
    Lee un archivo del Nanodrop, limpia los datos y calcula el 
    Volumen Final (V2) necesario para alcanzar una concentración deseada, 
    partiendo de un volumen inicial fijo.
    """
    print(f"Procesando archivo: {archivo_csv}...")
    
    # 1. Leer y limpiar el archivo
    df = pd.read_csv(archivo_csv)
    df_clean = df.loc[df['Sample ID'] != 'B', ["Sample ID", "Nucleic Acid", "Unit"]].copy()
    df_clean = df_clean.rename(columns={'Nucleic Acid': 'C1'})
    
    # Validaciones de seguridad
    if concentración_final <= 0:
        raise ValueError("La concentración final objetivo debe ser mayor a cero para evitar divisiones entre cero.")
    if vol_inicial <= 0:
        raise ValueError("El volumen inicial tomado debe ser mayor a cero.")
        
    # 2. Calcular el Volumen Final (V2)
    # V2 = (C1 * V1) / C2
    df_clean['Vol_final'] = (df_clean['C1'] * vol_inicial) / concentración_final
    
    # 3. Calcular el Volumen de Diluyente
    df_clean['Vol_diluyente'] = df_clean['Vol_final'] - vol_inicial
    
    # Seguridad: Si el volumen de diluyente es negativo, significa que 
    # tu muestra original (C1) es menos concentrada que tu objetivo (C2).
    # ¡No puedes concentrar una muestra agregando líquido!
    df_clean.loc[df_clean['Vol_diluyente'] < 0, 'Vol_diluyente'] = np.nan
    df_clean.loc[df_clean['Vol_diluyente'].isna(), 'Vol_final'] = np.nan # Invalida el vol_final también
    
    # 4. Registrar los parámetros fijos elegidos
    df_clean['Vol_inicial'] = vol_inicial
    df_clean['C2'] = concentración_final
    
    print("¡Procesamiento terminado! Tabla lista con volúmenes finales calculados.")
    
    return df_clean