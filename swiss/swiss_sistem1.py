from flask import Blueprint, render_template, request, redirect
from flask_security import login_required
from flask_paginate import Pagination, get_page_parameter
from models import ChissePlayer
from app import csrf, db
from .forms import SelectForm, Nameturnir, Point
import datetime
from config import Configuration

swiss_sistem = Blueprint('swiss_sistem', __name__, template_folder='templates')
csrf.exempt(swiss_sistem)
# play_tab = []  # таблица игроков


def pair(listt):
    listpair = []
    for i in range(0, len(listt), 2):
        if i == len(listt) - len(listt) % 2:
            listpair.append((listt[i], (None, 0)))
            break
        listpair.append((listt[i], listt[i + 1]))
    return listpair


class TournamentTableDict:

    def __init__(self, play_tb=[], nametab=None):
        self.play_tb = play_tb  # таблица игроков, query запросы
        self.nametab = nametab  # название турнира
        self.numbertour = 0  # номер турнира
        self.turnirtabl = dict()  # турнирная таблица скелет
        self.numberofplayer = self.numbofplay()  # колличество игроков

    def __repr__(self):  # для разработчика
        return f'название турнира - {self.nametab}, номер тура - {self.numbertour}, играет - {self.numbofplay()} игроков, таблица игроков - {self.play_tb}'

    def get_id_totalpoint_previous_tour(self, id=None):
        #возвращаем колличество заработанных очков
        print(self.turnirtabl['tour' + str(self.numbertour - 1)])
        for c, i in enumerate(self.turnirtabl['tour'+str(self.numbertour-1)]):
            #для пары 1
            if i['pair' + str(c)]['playr1']['id'] == id:
                return float(i['pair' + str(c)]['playr1']['totalpoint'])
            #для пары 2
            if i['pair' + str(c)]['playr2']['id'] == id:
                return float(i['pair' + str(c)]['playr2']['totalpoint'])

    def get_typle_id_id_play_tb(self, ddd):
        # расчитывает турнирную таблицу для следующего тура play_tb
        # на вход принимает словарь ddd из очков полученных в предыдущем туре id, totalpoint
        ttt = self.turnirtabl.copy() #берем турнирную таблицу и из нее извлекаем, кто в каком
        # туре играл

        # вспомогательная таблица
        ktoskem = {}
        for j in range(len(ttt) - 1):
            j = j + 1
            # возвращаем колличество туров только делаем текущий тур
            for i in range(len(ttt['tour' + str(1)])):

                # получаем колличесство пар и проходим по ним
                if j == 1:
                    ktoskem.update({ttt['tour' + str(j)][i]['pair' + str(i)]['playr1']['id']: []})
                    ktoskem.update({ttt['tour' + str(j)][i]['pair' + str(i)]['playr2']['id']: []})
                try:
                    ktoskem[(ttt['tour' + str(j)][i]['pair' + str(i)]['playr1']['id'])].append(
                        ttt['tour' + str(j)][i]['pair' + str(i)]['playr2']['id'])
                    ktoskem[(ttt['tour' + str(j)][i]['pair' + str(i)]['playr2']['id'])].append(
                        ttt['tour' + str(j)][i]['pair' + str(i)]['playr1']['id'])
                except IndexError:
                    print('Игра окончена', ktoskem) #!!!!!!!!!!!!!!!

        # print('кто с кем=', ktoskem)
        listidplayer = []
        # должно быть ddd словарь с ключем=id и значением=заработанным очкам {3: 1, 7: 0.5, 6: 1, 9: 0, 1: 0}
        # словарь {'1': ['6'], '6': ['1'], '3': ['7'], '7': ['3'], '9': [None], None: ['9']} ключ=id и значением список с кем играл id
        # сортируем игроков по очкам
        from operator import itemgetter
        from collections import OrderedDict

        sorted_ddd = OrderedDict(
            sorted(ddd.items(), key=itemgetter(1)))  # OrderedDict([(9, 0), (1, 0), (7, 0.5), (3, 1), (6, 1)])
        # print('сортировка', sorted_ddd)

        if None in ktoskem.keys():
        # if ktoskem.keys():
            key_sort = (tuple(sorted_ddd.keys()))

            # print('key sorte', key_sort)
            min_point = min(ddd.values())
            for i in range(len(sorted_ddd)):
                if list(sorted_ddd.values())[i] == min_point:  # если количество заработанных очков минимально
                    if None in ktoskem.get(
                            str(key_sort[i])):  # проверяем давалось ли ему очко просто так ищем Ноне по значениям ключа
                        continue
                    listidplayer.append(
                        tuple((ChissePlayer.query.get(key_sort[i]), None), ))  # если не давались очки добавляем в таблицу не играющего чела
                    ddd.pop(key_sort[i])
                    # print('///', ddd,
                    #       listidplayer)  # получили новый список и словарь с которого необходимо составить играющих
                    break
            # собираем команду заново
            sorted_ddd = OrderedDict(reversed(sorted(ddd.items(), key=itemgetter(1))))
            key_sort = (tuple(sorted_ddd.keys()))
            # print('KEY', key_sort)
            ktoskem.pop(None)
            # print(ktoskem)
            for id in key_sort:
                if str(id) in ktoskem.keys():
                    for i in range(len(key_sort)):
                        try:
                            if (str(id) in ktoskem.get(str(key_sort[i]))) or id == key_sort[i]:
                                continue
                            else:
                                listidplayer.append(((ChissePlayer.query.get(id), ChissePlayer.query.get(key_sort[i]))))
                                # print(listidplayer)
                                try:
                                    ktoskem.pop(str(id))
                                    ktoskem.pop(str(key_sort[i]))
                                    break
                                except KeyError:
                                    pass
                        except TypeError:
                            continue
                else:
                    continue
        if len(listidplayer)!=0:
            N = listidplayer.pop(0)
            listidplayer.append(N) #ноне засунули взад
        # print(sorted_ddd, ' ', ddd, 'list disp id--', listidplayer)

        return listidplayer

    def numbofplay(self):
        # определение колличества играющих игроков
        def fun(iterobj):
            # находим None в таблице игроков и возвращаем  True or False если одному игроку не хватило пары
            if iterobj[1] == None or iterobj[0] == None:
                return True
            else:
                return False

        if not (True in list(map(fun, self.play_tb))):
            numbplayer = (len(self.play_tb) * 2)  # количество игроков в таблице
        else:
            numbplayer = (len(self.play_tb) * 2 - 1)

        return numbplayer

    def add_tur(self):
        if self.nametab == None:
            self.numbertour = 0
        else:
            self.numbertour += 1

# создаем объект
objturnir = TournamentTableDict()


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
    return render_template('swiss.html', pages=pages, form=form, pagination=pagination)


@swiss_sistem.route('/table_party', methods=['GET', 'POST'])
# @login_required
@csrf.exempt
def table_party():
    # tab-таблица игроков

    if request.method == "POST":
        play_tab = []
        tab = []
        id_player = request.form.getlist('checks')

        quantity = len(id_player) // 2
        id_arr = sorted(map(int, id_player))

        for i in range(quantity):
            p = (id_arr[i], id_arr[quantity + i])  # рассписываем пары
            tab.append(p)

        if len(id_player) % 2:
            # если нечетное колличество игроков
            tab.append((id_arr[-1], 'bye'))

        for i in tab:
            if i[1] != None:
                play_tab.append((ChissePlayer.query.get(i[0]), (ChissePlayer.query.get(i[1]))))
            else:
                play_tab.append((ChissePlayer.query.get(i[0]), None))

        form = Nameturnir()
        objturnir.play_tb = play_tab
        return render_template('tabl.html', play_tab=play_tab, form=form)

    return redirect('/')


@swiss_sistem.route('/turnir', methods=['GET', 'POST'])
# @login_required
@csrf.exempt
def turnir():

    # tab-таблица игроков
    if request.method == "POST":
        try:
            total={}
            nameturn = request.form['nameturnir']
            objturnir.nametab = nameturn
            objturnir.turnirtabl.update({'nameturnir': nameturn})
        except:
            objturnir.add_tur()  # увеличиваем циферку турнира

        # self.turnirtablskelet=[{'nameturnir': self.nametab},
        #                       {'tour'+str(self.numbertour):
        #                       {'pair':{'playr1': {'id':0, 'totalpoint':0, 'point': 0},
        #                                'playr2':{'id':0, 'totalpoint':0, 'point':0}}}}]
        # достали все идентификаторы игроков и введенные очки, объект ImmutableMultiDict
            print(objturnir.numbertour)
            listpoint = []  # [(id, point),(id, point),(id, point)]
            for j, i in enumerate(request.form):
                listpoint.append((i, request.form[i]))

            qte = dict()
            qqq = {'tour' + str(objturnir.numbertour): []}
            par = pair(listpoint)  # разбили на пары

            total={} #{id:totalpoint} для текущего тура

            for j, i in enumerate(par):
                if objturnir.numbertour == 1:
                    # таблица тура если номер тура первый количество очков присваиваем point
                    qte = ({'pair' + str(j):
                                {'playr1': {'id': i[0][0], 'totalpoint': float(i[0][1]), 'point': float(i[0][1])},
                                 'playr2': {'id': i[1][0], 'totalpoint': float(i[1][1]), 'point': float(i[1][1])}}})
                    qqq['tour' + str(objturnir.numbertour)].append(qte)

                    if i[1][0] == None:
                        total.update({int(i[0][0]): float(i[0][1])})
                    else:
                        total.update({int(i[0][0]): float(i[0][1]), int(i[1][0]): float(i[1][1])})

                elif objturnir.numbertour > 1:

                    totpoint1 = objturnir.get_id_totalpoint_previous_tour(i[0][0])
                    totpoint2 = objturnir.get_id_totalpoint_previous_tour(i[1][0])

                    qte = ({'pair' + str(j):
                                {'playr1': {'id': i[0][0], 'totalpoint': float(i[0][1])+totpoint1, 'point': float(i[0][1])},
                                 'playr2': {'id': i[1][0], 'totalpoint': float(i[1][1])+totpoint2, 'point': float(i[1][1])}}})
                    qqq['tour' + str(objturnir.numbertour)].append(qte)
                    #добавляем в таблицу наименование турнира`
                    if i[1][0]==None:
                        total.update({int(i[0][0]): totpoint1 + float(i[0][1])})
                    else:
                        total.update({int(i[0][0]): totpoint1+float(i[0][1]), int(i[1][0]): totpoint2+float(i[1][1])})

                    # получаем такую штуку где меняются туры и пары, потом их кидаем в общую турнирную таблицу
                    # {tour1:[pair0: pair1...], tour2: [pair0: pair1...]}
                    # 'tour1': [{'pair0': {'playr1': {'id': '3', 'totalpoint': '1', 'point': '1'},
                    #                      'playr2': {'id': '7', 'totalpoint': '1', 'point': '1'}}}, {
                    #               'pair1': {'playr1': {'id': '6', 'totalpoint': '1', 'point': '1'},
                    #                         'playr2': {'id': '9', 'totalpoint': '1', 'point': '1'}}}

            objturnir.turnirtabl.update(qqq) #добавляем в таблицу очередной тур

        # if objturnir.numbertour>=1:
        #     print(objturnir.turnirtabl['tour'+str(objturnir.numbertour)])
        # print('== ', objturnir.turnirtabl)
        # print(objturnir.numbertour)
        print('total=', total)
        # расчитываем пары для игры play_tab
        if objturnir.numbertour>=1:
            play_tab = objturnir.get_typle_id_id_play_tb(total)
        else:
            play_tab = objturnir.play_tb

        form = Point()
        print('play_tab', play_tab)
        return render_template('turnir.html', form=form, play_tab=play_tab, total=total)

    return render_template('turnir.html', play_tab=play_tab, total={})
