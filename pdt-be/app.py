from flask import Flask, jsonify, g, json, request
import psycopg2
from dotenv import load_dotenv
import os
import decimal
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv('.env')

AREA_RARE = 10000000000

def get_db():
    if 'db' not in g:
        connect_str = "dbname='%s' user='%s' " \
                      "host='%s' port='%s' password='%s'" \
                      % (os.getenv('DB_NAME'),
                         os.getenv('DB_LOGIN'),
                         os.getenv('DB_HOST'),
                         os.getenv('DB_PORT'),
                         os.getenv('DB_PASS'))
        g.db = psycopg2.connect(connect_str)
    return g.db


@app.route("/get_points")
def points():
    cursor = get_db().cursor()
    cursor.execute("""
                      SELECT json_build_object(
                      'type',       'Feature',
                      'geometry',   ST_AsGeoJSON(geom_slovakia)::json,
                      'properties', json_build_object(
                        'animal', binomial)) FROM occurences_slovakia LIMIT 10;
                  """)
    res = cursor.fetchall()
    res = [x[0] for x in res]
    return jsonify(res)


@app.route('/get_slovakia')
def slovakia():
    cursor = get_db().cursor()
    cursor.execute("""
                      SELECT json_build_object(
                      'type',       'Feature',
                      'geometry',   ST_AsGeoJSON(way)::json,
                      'properties', json_build_object(
                        'country', description)) FROM countries;
                  """)
    return jsonify(cursor.fetchall())



@app.route('/get_nearby')
def get_nearby():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius')
    cursor = get_db().cursor()
    cursor.execute("""
                      SELECT json_build_object(
                      'type',       'Feature',
                      'geometry',   ST_AsGeoJSON(ST_Intersection(ST_Buffer(ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s), geom_slovakia))::json,
                      'properties', json_build_object(
                        'name', binomial))
                      FROM occurences_slovakia WHERE ST_DWithin(ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, geom_slovakia::geography, %s) AND ST_Area(geom_slovakia::geography) < %s AND legend != 'Extinct';
                   """, (lng, lat, radius, lng, lat, radius, AREA_RARE))
    res = cursor.fetchall()
    res = [x[0] for x in res]
    return jsonify(res)


@app.route('/get_animals')
def get_animals():
    cursor = get_db().cursor()
    cursor.execute("SELECT DISTINCT binomial from occurences_slovakia WHERE ST_Area(geom_slovakia::geography) < %s", (AREA_RARE,))
    res = cursor.fetchall()
    res = [x[0] for x in res]
    return jsonify(res)


@app.route('/get_animal')
def get_animal_polygon_by_name():
    name = request.args.get('name')
    cursor = get_db().cursor()
    cursor.execute("""
                    SELECT json_build_object(
                      'type',       'Feature',
                      'geometry',   ST_AsGeoJSON(geom_slovakia)::json,
                      'properties', json_build_object(
                        'name', binomial))
                      FROM occurences_slovakia WHERE binomial = %s AND legend != 'Extinct';
                   """, (name,))
    res = cursor.fetchall()
    res = [x[0] for x in res]
    return jsonify(res)

@app.route('/get_heatmap')
def get_heatmap():
    cursor = get_db().cursor()
    cursor.execute("""
                        SELECT json_build_object(
                        'type',       'Feature',
                        'geometry',   ST_AsGeoJSON(points)::json,
                        'properties', json_build_object(
                          'count', count(CASE WHEN ST_Contains(geom_slovakia, points) THEN 1 END)))  
                        FROM(SELECT(ST_Dump(ST_GeneratePoints(way, 250))).geom as points FROM countries) a
                        CROSS JOIN
                        occurences_slovakia b GROUP BY a.points
                        """)
    res = cursor.fetchall()
    res = [x[0] for x in res]
    values = []
    for point in res:
        values.append(point['properties']['count'])
    min_val = min(values)
    max_val = max(values)
    max_val -= min_val
    for i in range(len(res)):
        res[i]['properties']['count'] -= min_val
        res[i]['properties']['count'] /= max_val

    return jsonify(res)
