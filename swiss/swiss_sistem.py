from flask import Blueprint, render_template, request, redirect, flash
from flask_security import login_required
from flask_paginate import Pagination, get_page_parameter
from models import ChissePlayer
from app import csrf, db
from .forms import SelectForm, Nameturnir, Point
import datetime
from config import Configuration
from .tablemake import Table

swiss_sistem = Blueprint('swiss_sistem', __name__, template_folder='templates')
csrf.exempt(swiss_sistem)
table=Table() #экземпляр таблицы создаем объект таблицы

@swiss_sistem.route('/', methods=['GET', 'POST'])
# @login_required
@csrf.exempt
def swissistem():
    player = ChissePlayer.query.order_by(ChissePlayer.lastname)
    datta = ChissePlayer.query.order_by(ChissePlayer.datebirt).all()
    form = SelectForm()

    def yer():
        # выбираем года из базы
        return sorted(set([((g.datebirt.year), ((g.datebirt.year))) for g in datta]))

    def parsdatetime(strdatayear):
        # преобразуем в дату ('введенный год', первый месяц, первый день)
        return datetime.datetime(int(strdatayear), 1, 1)

    def pagin(players_chiss):
        # pagination
        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, total=players_chiss.count(),
                                bs_version=4)
        return pagination

    if request.method == 'POST':
        start_data = parsdatetime(request.form['widget_policy'])
        end_data = parsdatetime(request.form['end_data']).replace(day=31, month=12, hour=23, minute=59)
        players_chiss = ChissePlayer.query.filter(ChissePlayer.datebirt >= start_data,
                                                  ChissePlayer.datebirt <= end_data)
        pagination = pagin(players_chiss)
        pages = players_chiss.paginate(page=1, per_page=players_chiss.count())
        return render_template('swiss.html', pages=pages, pagination=pagination, p_none=True)

    form.widget_policy.choices = yer()
    form.end_data.choices = yer()
    pagination = pagin(player)
    pages = player.paginate(per_page=10)
    table.reset_players()

    return render_template('swiss.html', pages=pages, form=form, pagination=pagination)


@swiss_sistem.route('/table_party', methods=['GET', 'POST'])
# @login_required
@csrf.exempt
def table_party():

    if request.method == "POST":
        id_player = request.form.getlist('checks')
        id_arr = sorted(map(int, id_player))
        if len(id_arr)<=1:
            flash('Вы должны выбрать не менее двух игроков', 'warning')
            return redirect('/swiss_sistem/')

         # создаем турнирную таблицу

        if table.dict_gamers!={}:
            #в таблице есть данные не показывать таблицу,
            #вернуться в
            table.reset_players()
            return redirect('/swiss_sistem/')


        for id in id_arr:
            table.create_players(id, ChissePlayer.query.get(id).name,
                                 ChissePlayer.query.get(id).lastname)

        play_tab=table.table_game() #возращает таблицу с объектами[(obj1, obj3),...(objs),(objn)]

        form = Nameturnir()

        return render_template('tabl.html', play_tab=play_tab, form=form)
    return redirect('/')


@swiss_sistem.route('/turnir', methods=['GET', 'POST'])
# @login_required
@csrf.exempt
def turnir():

    if request.method == "POST":
        try:
            total={}
            nameturn = request.form['nameturnir']
            table.nameturnir = nameturn
        except:

            table.add_tur() # увеличиваем циферку турнира

             # [(id, point),(id, point),(id, point)]
            for i in request.form:
                if int(i):
                    id=int(i)
                    table.dict_gamers[id].win_points(float(request.form[i]), table.numbertur)

            print(table)

            for id in table.list_id_gamer:
                if id:
                    total[id] = table.dict_gamers[id].total_points

        #tur_table_all=table.tur_table_all()
        tur_table_all={}
        tur_table_all=table.tur_table_summ()

        play_tab=table.table_game() #возращает таблицу с объектами[(obj1, obj3),...(objs),(objn)]
        # проверяем окончание игры

        if len(play_tab)==1 and type(play_tab[0])==str:
            game_over=play_tab[0].upper()
            nambertur=table.numbertur

            return render_template('turnir.html', game_over=game_over, numbertur=nambertur, tur_table_all=tur_table_all)
        else:
            nambertur=table.numbertur+1

        return render_template('turnir.html', tur_table_all=tur_table_all, play_tab=play_tab, total=total, numbertur=nambertur)

    return render_template('turnir.html', play_tab=play_tab, total={})

@swiss_sistem.route('/turnir/end', methods=['GET', 'POST'])
# @login_required
@csrf.exempt
def save_summarytable():
    if request.method == "POST":
        table.berger_coefficient()
        table.buchholz_coefficient()
        tab = table
        tab.nan_tur() #вставляем '-' в турах которых не участвовал
        # import json
        # tablej=json.dumps(table.result())
        # print(tablej)

        # def fun(obj):
        #     d={}
        #     d.update(obj.__dict__)
        #     return d
        # import json
        # # for i in tab:
        # tab_json=json.dumps(tab, default=fun)
        # print(tab_json)
        # тута нужно сохранить усе у базу!!!!!!!!!!!!!!!!!!!
        return render_template ('summarytable.html', table=tab)