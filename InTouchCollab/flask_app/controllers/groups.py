from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.group import Group
from flask_app.models.address import Address
from flask import flash

#**************************************
#   Create group
#**************************************
@app.route("/create_group", methods=["POST"])
def create_group():
    # if not Painting.validate_painting(request.form):
    #     print("redirecting to new_painting")
    #     return redirect("/paintings/new")
    data = {
        "name" : request.form['name'],
        "description" : request.form['description']
    }

    #returns the id
    group_id = Group.add_group(data)

    return redirect('/dashboard')

#**************************************
#   See group info
#**************************************
@app.route("/group/<int:group_id>")
def group_info(group_id):


    data = {
        "id" : group_id
    }

    group = Group.get_users_in_group(data)
    print('first user in group', group.users[0])
    print('address', group.users[0].address)
    # print(group.users[0].address.street1)
    return render_template("show_group.html", group=group)

#**************************************
#   Delete group
#**************************************
@app.route("/delete/<int:id>")
def delete_group(id):
    data = {
        "id" :id
    }
    Group.delete(data)
    return redirect("dashboard")
