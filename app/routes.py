from flask import current_app as app
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask import jsonify
from app import db
from app.models import Request, RequestSchema, Provincias, Municipios
from app.forms import IndexForm, SearchBy
from app.search_algorithm import get_address
import folium

request_schema = RequestSchema()  # Create one task
requests_schema = RequestSchema(many=True)  # Create multiple tasks

# =============================================================================
# Services for Frontend
# =============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    post = IndexForm()
    post.municipio.choices = [(mun.CMUN, mun.NOMBRE)
                              for mun in Municipios.query.filter_by(CPRO='01').order_by('NOMBRE').all()]
    if request.method == 'POST':
        client_id = 1
        address = request.form['address']
        provincia = dict(post.provincia.choices).get(post.provincia.data)
        post.municipio.choices = [(mun.CMUN, mun.NOMBRE)
                                for mun in Municipios.query.filter_by(CPRO=post.provincia.data).all()]
        municipio = dict(post.municipio.choices).get(post.municipio.data)
        new_request = Request(client_id, provincia, municipio, address)
        db.session.add(new_request)
        db.session.commit()

        result = get_address(cpro=post.provincia.data,
                            cmun=post.municipio.data,
                            address=address)
        #result = {'status': 1, 'tvia': 'CALLE', 'nvia': 'BERROCAL'}
        
        '''new_request.completed_search(status=result['status'],
                                    tvia=result['tvia'],
                                    nvia=result['nvia'])
        db.session.commit()'''

        if result['status'] == -1:
            return redirect(url_for('address_options'))
        else:
            return redirect(url_for('result1'))

    return render_template('index.html', form=post)


@app.route('/municipios/<cpro>')
def list_mun(cpro):
    municipios = Municipios.query.filter_by(CPRO=cpro).order_by('NOMBRE').all()

    munArray = []
    for mun in municipios:
        munObj = {}
        munObj['CMUN'] = mun.CMUN
        munObj['NOMBRE'] = mun.NOMBRE
        munArray.append(munObj)

    return jsonify({'municipios': munArray})


@app.route('/search_client', methods=['GET', 'POST'])
def search_by_client():
    search = SearchBy()
    if request.method == 'GET':
        return render_template('search_by.html', table=None,
                               search=search, title='Search by Client')

    client_id = search.id.data
    client_request = Request.query.filter_by(client_id=int(client_id)).all()
    result = []
    for c in client_request:
        result.append(request_schema.dump(c))
    if len(result) < 1:
        flash('Id not found', 'danger')
    return render_template('search_by.html', table=result,
                           search=search, title='Search by Client')


@app.route('/search_request', methods=['GET', 'POST'])
def search_by_request():
    search = SearchBy()
    if request.method == 'GET':
        return render_template('search_by.html', table=None,
                               search=search, title='Search by Request')

    request_id = search.id.data
    req = Request.query.filter_by(request_id=int(request_id)).all()
    result = []
    for c in req:
        result.append(request_schema.dump(c))
    if len(result) < 1:
        flash('Id not found', 'danger')
    return render_template('search_by.html', table=result,
                           search=search, title='Search by Request')

@app.route('/map1')
def map_result1():
    coordinates = (36.7214175618618, -4.44599888204578)
    folium_map = folium.Map(location=coordinates, zoom_start=20)
    marker = folium.Marker(location=coordinates)
    marker.add_to(folium_map)
    #folium_map.save('app/templates/map.html')

    return folium_map._repr_html_()

@app.route('/map2')
def map_result2():
    coordinates = (36.6999032145525, -4.4752280869102)
    folium_map = folium.Map(location=coordinates, zoom_start=20)
    marker = folium.Marker(location=coordinates)
    marker.add_to(folium_map)
    #folium_map.save('app/templates/map.html')

    return folium_map._repr_html_()

@app.route('/select_options')
def address_options():
    flash('Calle no encontrada. Tiene las opciones más similares debajo.', 'warning')
    return render_template('address_options.html')

@app.route('/result1')
def result1():
    flash('Calle encontrada', 'success')
    return render_template('result1.html')

@app.route('/result2')
def result2():
    flash('Calle encontrada', 'success')
    return render_template('result2.html')
