from flask import Flask, abort, request, redirect, url_for
from google.appengine.api import users
from google.appengine.ext import ndb

app = Flask(__name__)

class Clue(ndb.Model):
	text = ndb.StringProperty()
	magicstring = ndb.StringProperty()

class Game(ndb.Model):
	name = ndb.StringProperty()
	clues = ndb.StructuredProperty(Clue, repeated=True)
	
@app.route('/edit')
def edit():
	if users.is_current_user_admin():
		output = "<html><body>"
		output = output + "<form action='/newgame' method=\"post\"> New game: <input type='text' name='newname'> <input type='submit' value='Add new game'></form>"
		output = output + "<br /> Select a game to edit!"
		games = Game.query(ancestor=game_list_key()).fetch()
		for game in games:
			output = output + "<br /><a href='/editgame/" + game.key.urlsafe() +"'>" + game.name + "</a>"
		return output + "</body></html>"
	else:
		abort(403)
		
def game_list_key():
    return ndb.Key('Game List', 'xmarksthespot_games')
		
@app.route('/newgame', methods=['POST'])
def newgame():
	if users.is_current_user_admin():
		newname = request.form['newname']
		newgame = Game(parent=game_list_key())
		newgame.name = newname
		newgame.put()
		return redirect(url_for('edit'))
	else:
		abort(403)
		

@app.route('/')
def homepage():
	user = users.get_current_user()
	output = "<html><body>"
	if user:
		output = output + user.nickname() + " <a href='" + users.create_logout_url("/") + "'>Sign out</a>"
		if users.is_current_user_admin():
			output = output + '<br /><a href="/edit">Go to edit page</a>'
	else:
		output = output + "<a href='" + users.create_login_url("/") + "'>Sign in</a>"
	return output + "</body></html>"


if __name__ == '__main__':
    app.run()
