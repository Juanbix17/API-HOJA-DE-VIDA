from flask import Flask, request
from database import conectar_bd

app = Flask(__name__)

@app.route("/probar")
def probar_data():
    conec = conectar_bd()
    if conec.is_connected():
        conec.close()

        return {
            "mensaje": "conexion ok"
        }


@app.route("/")
def inicio():
    return "Api hoja de vida funcionando"


@app.route("/api/hojas-vida/<int:id>")
def obtener_hojasvidaid(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT * FROM HOJAS_VIDA WHERE id = %s"

    cursor.execute(sql, (id,))
    datos = cursor.fetchone()

    if not datos:
        cursor.close()
        conec.close()

        return {
            "mensaje": "Hoja de vida no encontrada"
        }, 404

    columnas = [columna[0] for columna in cursor.description]
    hoja_vida = dict(zip(columnas, datos))

    cursor.close()
    conec.close()

    return hoja_vida


@app.route("/api/hojas-vida")
def obtener_hojasvida():
    hojas_vida = [{
        "id": 1,
        "nombre": "Juan Perez",
        "edad": 20,
        "ciudad": "Bogota",
        "fotografia": "foto",
        "programa": "adso",
        "ficha": 243541,
        "jornada": "diurna"
    },
    {
        "id": 2,
        "nombre": "Pepe Rodriguez",
        "edad": 58,
        "ciudad": "Bogota",
        "fotografia": "foto",
        "programa": "adso",
        "ficha": 314122,
        "jornada": "diurna"
    }]

    return hojas_vida


@app.route("/api/registrohv", methods=["POST"])
def registrohvida():
    conec = conectar_bd()
    cursor = conec.cursor()

    datos = request.json

    sql_consulta = "SELECT id FROM HOJAS_VIDA WHERE correo = %s"

    cursor.execute(sql_consulta, (datos["correo"],))

    usuario_existente = cursor.fetchone()

    if usuario_existente:
        id_existente = usuario_existente[0]

        cursor.close()
        conec.close()

        return {
            "mensaje": "El usuario ya está registrado con este correo",
            "id": id_existente
        }

    sql = """INSERT INTO HOJAS_VIDA
    (nombre, edad, ciudad, correo, fotografia, programa, ficha, jornada)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

    valor = (
        datos["nombre"],
        datos["edad"],
        datos["ciudad"],
        datos["correo"],
        datos.get("fotografia"),
        datos["programa"],
        datos["ficha"],
        datos["jornada"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    id_generado = cursor.lastrowid

    cursor.close()
    conec.close()

    return {
        "mensaje": "Hoja de vida registrada con éxito",
        "id": id_generado
    }, 201


@app.route("/api/enlistar", methods=["GET"])
def listar_hojasvida():
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    sql = "SELECT * FROM HOJAS_VIDA"

    cursor.execute(sql)
    datos = cursor.fetchall()

    columnas = [columna[0] for columna in cursor.description]
    resultado = []

    for lista in datos:
        hoja_vida = dict(zip(columnas, lista))
        resultado.append(hoja_vida)

    cursor.close()
    conec.close()

    return {
        "hojas_vida": resultado
    }


@app.route("/api/eliminarhv/<int:id>", methods=["DELETE"])
def eliminar_hoja_vida(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql_consulta = "SELECT id FROM HOJAS_VIDA WHERE id = %s"

    cursor.execute(sql_consulta, (id,))
    hoja_vida = cursor.fetchone()

    if not hoja_vida:
        cursor.close()
        conec.close()

        return {
            "mensaje": "La hoja de vida no existe",
            "id": id
        }, 404

    sql = "DELETE FROM HOJAS_VIDA WHERE id = %s"

    cursor.execute(sql, (id,))
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Hoja de vida eliminada correctamente",
        "id": id
    }, 200
#hojas de vida fin

@app.route("/api/hojas-vida/<int:id>/estudios", methods=["GET"])
def listar_estudios(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT * FROM ESTUDIOS WHERE hoja_vida_id = %s"

    cursor.execute(sql, (id,))
    datos = cursor.fetchall()

    columnas = [columna[0] for columna in cursor.description]
    resultado = []

    for lista in datos:
        estudio = dict(zip(columnas, lista))
        resultado.append(estudio)

    cursor.close()
    conec.close()

    return {
        "estudios": resultado
    }


@app.route("/api/hojas-vida/<int:id>/estudios", methods=["POST"])
def registrar_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    datos = request.json

    sql = """INSERT INTO ESTUDIOS
    (hoja_vida_id, nivel, institucion, titulo, anio_graduacion)
    VALUES(%s, %s, %s, %s, %s)"""

    valores = (
        id,
        datos["nivel"],
        datos["institucion"],
        datos["titulo"],
        datos["anio_graduacion"]
    )

    cursor.execute(sql, valores)
    conec.commit()

    id_generado = cursor.lastrowid

    cursor.close()
    conec.close()

    return {
        "mensaje": "Estudio registrado correctamente",
        "id": id_generado
    }, 201


@app.route("/api/estudios/<int:id>", methods=["GET"])
def obtener_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT * FROM ESTUDIOS WHERE id = %s"

    cursor.execute(sql, (id,))
    datos = cursor.fetchone()

    if not datos:
        cursor.close()
        conec.close()

        return {
            "mensaje": "El estudio no existe"
        }, 404

    columnas = [columna[0] for columna in cursor.description]
    estudio = dict(zip(columnas, datos))

    cursor.close()
    conec.close()

    return estudio


@app.route("/api/estudios/<int:id>", methods=["PUT"])
def actualizar_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    datos = request.json

    sql = """UPDATE ESTUDIOS
    SET nivel = %s,
        institucion = %s,
        titulo = %s,
        anio_graduacion = %s
    WHERE id = %s"""

    valores = (
        datos["nivel"],
        datos["institucion"],
        datos["titulo"],
        datos["anio_graduacion"],
        id
    )

    cursor.execute(sql, valores)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Estudio actualizado correctamente",
        "id": id
    }


@app.route("/api/estudios/<int:id>", methods=["DELETE"])
def eliminar_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "DELETE FROM ESTUDIOS WHERE id = %s"

    cursor.execute(sql, (id,))
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Estudio eliminado correctamente",
        "id": id
    }
#ESTUDIOS FIN
@app.route("/api/hojas-vida/<int:id>/experiencias", methods=["GET"])
def listar_experiencias(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT * FROM EXPERIENCIAS WHERE hoja_vida_id = %s"

    cursor.execute(sql, (id,))
    datos = cursor.fetchall()

    columnas = [columna[0] for columna in cursor.description]
    resultado = []

    for lista in datos:
        experiencia = dict(zip(columnas, lista))
        resultado.append(experiencia)

    cursor.close()
    conec.close()

    return {
        "experiencias": resultado
    }

@app.route("/api/hojas-vida/<int:id>/experiencias", methods=["POST"])
def registrar_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    datos = request.json

    sql = """INSERT INTO EXPERIENCIAS
    (hoja_vida_id, empresa, cargo, tiempo, funciones)
    VALUES(%s, %s, %s, %s, %s)"""

    valores = (
        id,
        datos["empresa"],
        datos["cargo"],
        datos["tiempo"],
        datos["funciones"]
    )

    cursor.execute(sql, valores)
    conec.commit()

    id_generado = cursor.lastrowid

    cursor.close()
    conec.close()

    return {
        "mensaje": "Experiencia registrada correctamente",
        "id": id_generado
    }, 201

@app.route("/api/experiencias/<int:id>", methods=["GET"])
def obtener_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT * FROM EXPERIENCIAS WHERE id = %s"

    cursor.execute(sql, (id,))
    datos = cursor.fetchone()

    if not datos:
        cursor.close()
        conec.close()

        return {
            "mensaje": "La experiencia no existe"
        }, 404

    columnas = [columna[0] for columna in cursor.description]
    experiencia = dict(zip(columnas, datos))

    cursor.close()
    conec.close()

    return experiencia

@app.route("/api/experiencias/<int:id>", methods=["PUT"])
def actualizar_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    datos = request.json

    sql = """UPDATE EXPERIENCIAS
    SET empresa = %s,
        cargo = %s,
        tiempo = %s,
        funciones = %s
    WHERE id = %s"""

    valores = (
        datos["empresa"],
        datos["cargo"],
        datos["tiempo"],
        datos["funciones"],
        id
    )

    cursor.execute(sql, valores)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Experiencia actualizada correctamente",
        "id": id
    }

@app.route("/api/experiencias/<int:id>", methods=["DELETE"])
def eliminar_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "DELETE FROM EXPERIENCIAS WHERE id = %s"

    cursor.execute(sql, (id,))
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Experiencia eliminada correctamente",
        "id": id
    }
#EXOERIENCIAS FIN



if __name__ == "__main__":
    app.run(debug=True)
