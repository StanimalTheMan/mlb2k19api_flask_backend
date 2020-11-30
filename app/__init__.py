# app/__init__.py


from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

# local import
# from instance.config import app_config

# connect to db
def connect_to_db():
    db = os.environ.get('DATABASE_URL')
    

    try:
        return psycopg2.connect(db)
    except:
        print("Can't connect to database")

def create_app(config_name):
    app = Flask(__name__)
    
    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.route('/batting/player', methods=['GET'])
    def get_batter_data():
        con = connect_to_db()
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        SQL = 'select * from "Batting" inner join "Master" on "Batting"."playerID" = "Master"."playerID" and "Master"."nameLast" in (%s) and "Master"."nameFirst" in (%s);'
        try:
            cur.execute(SQL, (request.args.get('last'), request.args.get('first')))
        except:
            print("Error executing query")

        data = []
        for row in cur:
            # precautionary measures
            row['SF'] = 0 if row['SF'] is None else row['SF']
            row['H'] = 0 if row['H'] is None else row['H']
            row['AB'] = 0 if row['AB'] is None else row['AB']
            row['BB'] = 0 if row['BB'] is None else row['BB']
            row['HBP'] = 0 if row['HBP'] is None else row['HBP']

            data_entry = {
                'playerID': row['playerID'],
                'nameFirst': row['nameFirst'],
                'nameLast': row['nameLast'],
                'yearID': row['yearID'],
                'teamID': row['teamID'],
                'lgID': row['lgID'],
                'HR': row['HR'],
                'RBI': row['RBI'],
                'SB': row['SB'],
            }


            if row['AB'] == 0:
                data_entry['AVG'] = str(0.000)
            else:
                data_entry['AVG'] = str(round(row['H'] / row['AB'], 3))

            if row['AB'] + row['BB'] + row['HBP'] + row['SF'] == 0:
                data_entry['OBP'] = str(0.000)
            else:
                data_entry['OBP'] = str(round((row['H'] + row['BB'] + row['HBP']) / (row['AB'] + row['BB'] + row['HBP'] + row['SF']), 3))
                print(data_entry)
            data.append(data_entry)
        
        response = jsonify(data)
        con.close()

        return response

    @app.route('/pitching/player', methods=['GET'])
    def get_pitcher_data():
        con = connect_to_db()
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        SQL = 'select * from "Pitching" inner join "Master" on "Pitching"."playerID" = "Master"."playerID" and "Master"."nameLast" in (%s) and "Master"."nameFirst" in (%s);'
        try:
            cur.execute(SQL, (request.args.get('last'), request.args.get('first')))
        except:
            print("Error executing query")

        data = []
        for row in cur:
            # precautionary measures
            row['H'] = 0 if row['H'] is None else row['H']
            row['BB'] = 0 if row['BB'] is None else row['BB']
            row['IPouts'] = 0 if row['IPouts'] is None else row['IPouts']

            data_entry = {
                'playerID': row['playerID'],
                'nameFirst': row['nameFirst'],
                'nameLast': row['nameLast'],
                'yearID': row['yearID'],
                'teamID': row['teamID'],
                'lgID': row['lgID'],
                'W': row['W'],
                'L': row['L'],
                'SO': row['SO'],
                'ERA': str(round(row['ERA'], 2)),
            }

            if row['IPouts'] == 0:
                data_entry['WHIP'] = str(0.00)
            else:
                data_entry['WHIP'] = str(round((row['H'] + row['BB']) * 3 / row['IPouts'], 2))

            data.append(data_entry)
            
        response = jsonify(data)
        con.close()

        return response
            # PLAYERID	YEARID	TEAMID	LGID	W	L	SO	ERA	WHIP
    '''
    .then((pitcherData) => {
      // WHIP = round((H + BB)) * 3/IPouts, 2)
      pitcherData.forEach((pitcherDataEntry) => {
        pitcherDataEntry.ERA = String(pitcherDataEntry.ERA.toFixed(2));
        pitcherDataEntry.WHIP = String(
          (
            ((pitcherDataEntry.H + pitcherDataEntry.BB) * 3) /
            pitcherDataEntry.IPouts
          ).toFixed(2)
        );
      });

      res.send(pitcherData);
    });
});
    '''
    return app