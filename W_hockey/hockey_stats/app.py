from flask import Flask, render_template
import data_display as dd
import dash_plot as dp


app = Flask(__name__)

@app.route('/')
def skater():
    con = dd.connect_sql()
    nwhl_skate = {}
    cwhl_skate = {}
    all_skate = {}
    table = [['nwhl_stats', 'NWHL'], ['cwhl_stats', 'CWHL']]
    for year in range(2015, 2019):
        nwhl_skate[year] = dd.get_table_html(dd.get_table_list(con, table[0][0], table[0][1], year))
        cwhl_skate[year] = dd.get_table_html(dd.get_table_list(con, table[1][0], table[1][1], year))
        all_skate[year] = dd.get_all_html(dd.get_all_table_list(con, year, table[0][0], table[1][0]))
    return render_template("layout.html", title2='Skaters Regular Season', nwhl=nwhl_skate, cwhl=cwhl_skate, all=all_skate)

@app.route('/playoffs')
def playoffs():
    con = dd.connect_sql()
    nwhl_p = {}
    cwhl_p = {}
    all_p = {}
    table = [['nwhl_playoffs', 'NWHL'], ['cwhl_playoffs', 'CWHL']]
    for year in range(2015, 2019):
        nwhl_p[year] = dd.get_table_html(dd.get_table_list(con, table[0][0], table[0][1], year))
        cwhl_p[year] = dd.get_table_html(dd.get_table_list(con, table[1][0], table[1][1], year))
        all_p[year] = dd.get_all_html(dd.get_all_table_list(con, year, table[0][0], table[1][0]))
    return render_template("layout.html", title2='Skaters Playoffs', nwhl=nwhl_p, cwhl=cwhl_p, all=all_p)

@app.route('/goalies')
def goalies():
    con = dd.connect_sql()
    nwhl_g = {}
    cwhl_g = {}
    all_g = {}
    table = [['nwhl_goalies', 'NWHL'], ['cwhl_goalies', 'CWHL']]
    for year in range(2015, 2019):
        nwhl_g[year] = dd.get_goalie_html(dd.get_goalie_table(con, table[0][0], table[0][1], year))
        cwhl_g[year] = dd.get_goalie_html(dd.get_goalie_table(con, table[1][0], table[1][1], year))
        #all_p[year] = dd.get_all_html(dd.get_all_table_list(con, year, table[0][0], table[1][0]))
    return render_template("layout.html", title2='Goalie Stats', nwhl=nwhl_g, cwhl=cwhl_g, all=all_g)

@app.route('/goalie_playoffs')
def goalies_p():
    con = dd.connect_sql()
    nwhl_gp = {}
    cwhl_gp = {}
    all_gp = {}
    table = [['nwhl_playoffs_g', 'NWHL'], ['cwhl_playoffs_g', 'CWHL']]
    for year in range(2015, 2019):
        nwhl_gp[year] = dd.get_goalie_html(dd.get_goalie_table(con, table[0][0], table[0][1], year))
        cwhl_gp[year] = dd.get_goalie_html(dd.get_goalie_table(con, table[1][0], table[1][1], year))
        #all_p[year] = dd.get_all_html(dd.get_all_table_list(con, year, table[0][0], table[1][0]))
    return render_template("layout.html", title2='Goalie Playoff Stats', nwhl=nwhl_gp, cwhl=cwhl_gp, all=all_gp)

@app.route('/hometown')
def map():
    #dp.map()
    return render_template("map.html", title2='Hometowns')


if __name__ =='__main__':
    app.run()