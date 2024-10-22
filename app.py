from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesaria para manejar sesiones

# Ruta principal para el registro
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        date = request.form['date']
        name = request.form['name']
        lastname = request.form['lastname']
        turn = request.form['turn']
        seminars = request.form.getlist('seminars')

        # Crear un nuevo registro
        new_registration = {
            'date': date,
            'name': name,
            'lastname': lastname,
            'turn': turn,
            'seminars': ', '.join(seminars)
        }

        # Si no existe la lista de registros en la sesión, se crea
        if 'registrations' not in session:
            session['registrations'] = []  # Crear la lista de registros si no existe

        # Añadir el nuevo registro a la lista existente
        registrations = session['registrations']  # Obtener la lista de registros actual
        registrations.append(new_registration)  # Añadir el nuevo registro
        session['registrations'] = registrations  # Guardar la lista actualizada en la sesión

        # Redirigir a la página de listado
        return redirect(url_for('listado'))

    return render_template('registro.html')

# Ruta para ver la lista de inscritos
@app.route('/listado')
def listado():
    registrations = session.get('registrations', [])  # Obtener los registros de la sesión
    return render_template('listado.html', registrations=registrations)

# Ruta para eliminar un registro
# Ruta para eliminar un registro
@app.route('/eliminar/<int:index>')
def eliminar(index):
    # Verificar si hay registros en la sesión
    if 'registrations' in session:
        registrations = session['registrations']
        
        # Asegurarse de que el índice es válido
        if 0 <= index < len(registrations):
            registrations.pop(index)  # Eliminar el registro en la posición index
            session['registrations'] = registrations  # Actualizar la sesión con la lista modificada
        else:
            return "Índice fuera de rango", 400  # Manejar error de índice inválido
    return redirect(url_for('listado'))


# Ruta para editar un registro (opcional)
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    if 'registrations' not in session:
        return redirect(url_for('listado'))
    
    if request.method == 'POST':
        # Obtener los nuevos datos del formulario
        session['registrations'][index]['date'] = request.form['date']
        session['registrations'][index]['name'] = request.form['name']
        session['registrations'][index]['lastname'] = request.form['lastname']
        session['registrations'][index]['turn'] = request.form['turn']
        session['registrations'][index]['seminars'] = ', '.join(request.form.getlist('seminars'))

        return redirect(url_for('listado'))
    
    registration = session['registrations'][index]
    return render_template('editar.html', registration=registration, index=index)

if __name__ == '__main__':
    app.run(debug=True)
