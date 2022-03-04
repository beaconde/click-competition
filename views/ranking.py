import flask_praetorian
import sqlalchemy
from flask import jsonify
from flask_restx import Resource, Namespace

from model import db, Player, PlayerSchema


# namespace declaration
api_ranking = Namespace("Ranking", "Ranking management")


@api_ranking.route("/players")
class RankingPlayersController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT id, name, clicks \
                                 FROM player \
                                 ORDER BY clicks desc')
        result = db.session.execute(query).fetchall()
        return PlayerSchema(many=True).dump(result)


@api_ranking.route("/players/<player_id>")
class RankingPlayerController(Resource):
    @flask_praetorian.auth_required
    def get(self, player_id):
        player = Player.query.get_or_404(player_id)
        return player.clicks


@api_ranking.route("/teams")
class RankingTeamsController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT team.name, sum(player.clicks) as clicks \
                                 FROM teams_players \
                                 INNER JOIN team on teams_players.team_id = team.id \
                                 INNER JOIN player on teams_players.player_id = player.id \
                                 GROUP BY teams_players.team_id \
                                 ORDER BY clicks desc')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/teams/<team_id>")
class RankingTeamController(Resource):
    @flask_praetorian.auth_required
    def get(self, team_id):
        query = sqlalchemy.text('SELECT team.name, sum(player.clicks) as clicks \
                                 FROM teams_players \
                                 INNER JOIN team on teams_players.team_id = team.id \
                                 INNER JOIN player on teams_players.player_id = player.id \
                                 WHERE teams_players.team_id = ' + team_id + '\
                                 GROUP BY teams_players.team_id')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/countries")
class RankingCountriesController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT country.name, sum(player.clicks) as clicks \
                                 FROM country \
                                 INNER JOIN region on region.country_id = country.id \
                                 INNER JOIN locality on locality.region_id = region.id \
                                 INNER JOIN player on player.locality_id = locality.id \
                                 GROUP BY country.name \
                                 ORDER BY clicks desc')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/countries/<country_id>")
class RankingCountryController(Resource):
    @flask_praetorian.auth_required
    def get(self, country_id):
        query = sqlalchemy.text('SELECT country.name, sum(player.clicks) as clicks \
                                 FROM country \
                                 INNER JOIN region on region.country_id = country.id \
                                 INNER JOIN locality on locality.region_id = region.id \
                                 INNER JOIN player on player.locality_id = locality.id \
                                 WHERE country.id = ' + country_id + '\
                                 GROUP BY country.name')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/regions")
class RankingRegionsController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT region.name, sum(player.clicks) as clicks \
                                 FROM region \
                                 INNER JOIN locality on locality.region_id = region.id \
                                 INNER JOIN player on player.locality_id = locality.id \
                                 GROUP BY region.name \
                                 ORDER BY clicks desc')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/regions/<region_id>")
class RankingRegionController(Resource):
    @flask_praetorian.auth_required
    def get(self, region_id):
        query = sqlalchemy.text('SELECT region.name, sum(player.clicks) as clicks \
                                 FROM region \
                                 INNER JOIN locality on locality.region_id = region.id \
                                 INNER JOIN player on player.locality_id = locality.id \
                                 WHERE region.id = ' + region_id + '\
                                 GROUP BY region.name')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/localities")
class RankingLocalitiesController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        query = sqlalchemy.text('SELECT locality.name, sum(player.clicks) as clicks \
                                 FROM locality \
                                 INNER JOIN player on locality.id = player.locality_id \
                                 GROUP BY locality.name \
                                 ORDER BY clicks desc')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})


@api_ranking.route("/localities/<locality_id>")
class RankingLocalityController(Resource):
    @flask_praetorian.auth_required
    def get(self, locality_id):
        query = sqlalchemy.text('SELECT locality.name, sum(player.clicks) as clicks \
                                 FROM locality \
                                 INNER JOIN player on locality.id = player.locality_id \
                                 WHERE locality.id = ' + locality_id + ' \
                                 GROUP BY locality.name')
        result = db.session.execute(query)
        return jsonify({res['name']: res['clicks'] for res in result})
