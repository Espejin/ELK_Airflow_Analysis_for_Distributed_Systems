from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import pandas as pd
from sqlalchemy import create_engine
import time
import random
import mysql.connector

def exec_mysql_command(query):
    conn = mysql.connector.connect(
        host='192.168.96.5',  # Cambia esto si tu servidor MySQL está en otro host
        user='root',  # Nombre de usuario
        password='miclave',  # Contraseña
        database='mydatabase'  # Nombre de la base de datos
    )

    try:
        # Crear un cursor para ejecutar las consultas
        cursor = conn.cursor()

        # Ejecutar el query
        cursor.execute(query)

        # Si es un SELECT, obtener los resultados
        if query.strip().lower().startswith('select'):
            resultados = cursor.fetchall()
            for fila in resultados:
                print(fila)

            return resultados
        else:
            # Si es un INSERT, UPDATE, DELETE, commit los cambios
            conn.commit()
            print("Consulta ejecutada correctamente.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Cerrar el cursor
        cursor.close()
        conn.close()

def ges_ejecucion(tipo_ins):

    #Prepara ejecucion:
    if tipo_ins == 0:
        exec_mysql_command("UPDATE airflow_bar_execution SET execution = 1")

    elif tipo_ins == 1:
        exec_mysql_command("UPDATE airflow_bar_execution SET execution = 0")
    #Devuelve variable ejecucion
    else:
        res_q = exec_mysql_command("select execution FROM airflow_bar_execution")
        if res_q:  # Verifica si hay resultados
            var_exec = res_q[0][0]
            return var_exec
        else:
            print("No se encontraron resultados.")
            return None


def call_curl_website(site, port, possible_sections):

    ran_section = random.choice(possible_sections)
    command = ['curl', '-X', 'GET', site + ':' + str(port) + '/' + ran_section]
    result = subprocess.run(command, capture_output=True, text=True)

    print("Llamando a sección : " + ran_section)

    return ran_section, result



def requests_generator(**kwargs):

    lst_sections = ['index.html','skills.html','exp_edu.html','contact.html']
    lst_ports = [80,81]
    lst_prob = [0.7,0.3]
    site = 'http://192.168.96.4' # IP interna de docker

    ges_ejecucion(0)
    var_ejecucion = ges_ejecucion(2)

    print("Datos : " + str(var_ejecucion))
    while var_ejecucion == 1:
        rnd_port = random.choices(lst_ports, weights=lst_prob, k=1)[0]

        rn_sec, res = call_curl_website(site, rnd_port, lst_sections)
        print ("Consumiendo sitio - "  + site + ':' + str(rnd_port) + '/' + rn_sec)
        time.sleep(5)  # Espera 5 segundos
        var_ejecucion = ges_ejecucion(2)
        print(res.stdout)

with DAG(
    dag_id='requests_generator_base',
    start_date=datetime.now(),
    schedule_interval=None, 
    catchup=False,
    tags=['Proyecto Ing. Datos'],
) as dag:

    # Crear el PythonOperator
    request_task = PythonOperator(
        task_id='requests_generator_task',
        python_callable=requests_generator,
        provide_context=True,
    )

    
    request_task


