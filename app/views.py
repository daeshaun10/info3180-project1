"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from .forms import PropertyForm
from werkzeug.utils import secure_filename
from app.models import PropertyData
from app import db


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

## ---------------------------------------- property/create route ----------------------------------- ##

@app.route("/properties/create", methods=("GET", "POST"))
def propertyform():
    form = PropertyForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form["title"]
        desc = request.form["desc"]
        rooms = request.form["rooms"]
        bathrooms = request.form["bathrooms"]
        price = request.form["price"]
        propertytype = request.form["propertytype"]
        location = request.form["location"]

        ## fileupload
        f = form.upload.data
        filename = secure_filename(f.filename)
        img_url = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f.save(img_url)

        ##saving in db
        property = PropertyData(
            title=title,
            description=desc,
            rooms=rooms,
            bathrooms=bathrooms,
            price=price,
            type=propertytype,
            location=location,
            url=filename
        )

        db.session.add(property)
        db.session.commit()
      
        flash("property saved successfully!")
        return redirect(url_for("properties"))
    return render_template("propertyform.html", form=form)

## ----------------------------------------------------------------------------------------------- ##

## ---------------------------------------- properties route -------------------------------------- ##

@app.route("/properties/")
def properties():
    data = PropertyData.query.all()
    return render_template("properties.html", data=data)

## ------------------------------------------------------------------------------------------------- ##

## ---------------------------------------- single property route ----------------------------------- ##
@app.route("/properties/<propertyid>")
def property(propertyid):
    data = PropertyData.query.filter_by(id=propertyid).first()
    return render_template("property.html", data=data)

## ------------------------------------------------------------------------------------------------- ##

## --------------------------------------------- handling uploaded files -----------------------------##

@app.route("/uploads/<filename>")
def get_image(filename):
    print(filename)
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

## --------------------------------------------------------------------------------------------------- ##

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
