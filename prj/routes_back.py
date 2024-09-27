import os
import psycopg2
from flask import Flask, render_template,request, url_for, redirect
from prj import app
from prj.frm_data import EditForm,CariForm

def get_db_connection():
    conn=psycopg2.connect(host='localhost',
                          database='moocs',
                          user='postgres',
                          password='postgres123')
    return conn

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/tampil_data", methods=["GET","POST"])
def tampil_data():
    conn = get_db_connection()
    cur = conn.cursor()
    form_cari=CariForm()

    wherenya_1=""

    if request.method=="POST":
       details=request.form
       yname=details["wname"]

       if len(yname)>0:
          wherenya_1=" where name like '%"+yname+"%'"
       else:
          wherenya_1=""

    cur.execute("""select gid,osm_id,name,operatorty,addrcity,addrfull,amenity,source,ST_X(geom),ST_Y(geom) 
                   from hotosm_idn """+wherenya_1+""" order by amenity""")
    dataku = cur.fetchall()

    # Data Peta
    cur.execute("select gid,name,amenity,ST_X(geom),ST_Y(geom) from hotosm_idn "+ wherenya_1)
    datapeta = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("tampil_data.html", dataku=dataku,datapeta=datapeta,form_cari=form_cari)

@app.route("/edit_data/<id>",methods=["GET","POST"])
def edit_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    form=EditForm()
    cur.execute("select gid,osm_id,operatorty,name,addrcity,addrfull,amenity,source,geom from hotosm_idn where gid ='"+ id +"'")
    hasilnya=cur.fetchall()
    for rows in hasilnya:
        xgid=rows[0]
        xosm_id = rows[1]
        xoperatorty = rows[2]
        xname=rows[3]
        xaddrcity=rows[4]
        xaddrfull=rows[5]
        xamenity=rows[6]
        xsource = rows[7]
        xgeom = rows[8]

    if request.method=="POST":
       details=request.form
       xgid=id
       xosm_id=details["zosm_id"]
       xoperatorty = details["zoperatorty"]
       xname = details["zname"]
       xaddrcity = details["zaddrcity"]
       xaddrfull = details["zaddrfull"]
       xamenity = details["zamenity"]
       xgeom = details["zgeom"]
       xsource = details["zsource"]

       cur.execute("update hotosm_idn set osm_id=%s,name=%s,addrcity=%s,addrfull=%s,source=%s,operatorty=%s,amenity=%s,geom=%s where gid=%s",
                   ((xosm_id,xname,xaddrcity,xaddrfull,xsource,xoperatorty,xamenity,xgeom,xgid)))
       cur.connection.commit()
       cur.close()
       return render_template("info/sukses_edit.html")
    else:
       form.zosm_id.data = xosm_id
       form.zname.data=xname
       form.zoperatorty.data=xoperatorty
       form.zaddrcity.data=xaddrcity
       form.zaddrfull.data=xaddrfull
       form.zamenity.data=xamenity
       form.zsource.data=xsource
       form.zgeom.data=xgeom
    return render_template("edit_data.html",form=form)

@app.route("/hapus_data/<id>",methods=["GET","POST"])
def hapus_data(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("delete from hotosm_idn where gid='"+id+"'")
    cur.connection.commit()
    cur.close()
    return render_template("info/sukses_hapus_data.html")

@app.route("/entry_data",methods=["GET","POST"])
def entry_data():
    conn = get_db_connection()
    cur = conn.cursor()
    form=EditForm()

    if request.method=="POST":
        details=request.form
        xosm_id = details["zosm_id"]
        xname = details["zname"]
        xaddrcity = details["zaddrcity"]
        xoperatorty = details["zoperatorty"]
        xaddrfull = details["zaddrfull"]
        xsource = details["zsource"]
        xamenity = details["zamenity"]

        cur.execute("insert into hotosm_idn (osm_id,name,addrcity,operatorty,addrfull,source,amenity) values (%s,%s,%s,%s,%s,%s,%s)",((xosm_id,xname,xaddrcity,xoperatorty,xaddrfull,xsource,xamenity)))
        cur.connection.commit()
        cur.close()
        return render_template("info/sukses_entry.html")

    return render_template("entry_data.html",form=form)