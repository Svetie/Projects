from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.painting import Painting
from flask import flash

#################################
#   New Painting
#################################
@app.route("/paintings/new")
def new_recipe():
    if not 'user_id' in session:
        flash("Please login!!!")
        return redirect('/')
    return render_template("new_painting.html")

#################################
#   Create painting
#################################
@app.route("/create_painting", methods=['POST'])
def create_pnting():
    print("inside create painting")

    if not Painting.validate_painting(request.form):
        print("redirecting to new_painting")
        return redirect("/paintings/new")

    data = {
        "user_id" : session['user_id'],
        "title" : request.form['title'],
        "description" : request.form['description'],
        "price" : request.form['price'],
    }
    painting = Painting.save_painting(data) #returns the id
    return redirect('/dashboard')

#################################
#   Edit painting
#################################
@app.route("/paintings/<int:id>/edit")
def edit_painting(id):
    # if in session
    if not "user_id" in session:
        flash("You have to login!")
        return redirect("/")
    data = {
        "id" : id
    }

    one_painting = Painting.get_painting_info(data)
    logged_user_id = session['user_id']

    if logged_user_id != one_painting.user_id:
        flash("You cannot access that page!")
        return redirect("/dashboard")

    return render_template("edit_painting.html", painting = one_painting, user_id = logged_user_id)

#******************************************
#   Update painting
#******************************************
@app.route("/update_painting/<int:id>", methods = ["POST"])
def update_painting(id):

    if not Painting.validate_painting(request.form):
        return redirect(f'/paintings/{id}/edit')

    data = {
        "id" : id,
        # "user_id" : session['user_id'],
        "title" : request.form['title'],
        "description" : request.form['description'],
        "price" : request.form['price'],
    }

    Painting.update_painting(data)
    return redirect("/dashboard")

#******************************************
#   Show the painting
#******************************************
@app.route("/paintings/<int:id>")
def show_a_painting(id):
    if not 'user_id' in session:
        flash("Please login!")
        return redirect('/')
    data = {
        "id" : id
    }

    one_painting= Painting.get_painting_info(data)
    return render_template("show_one.html", painting=one_painting)



#******************************************
#   Delete painting
#******************************************
@app.route("/delete/<int:id>")
def eliminame_painting(id):

    data = {
        "id" : id
    }

    Painting.delete_painting(data)
    return redirect("/dashboard")