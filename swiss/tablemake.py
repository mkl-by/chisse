# from test5 import Listinstanse
from operator import itemgetter
import math

class Gamer:
    def __init__(self, id, name, lastname):
        self.name = name
        self.lastname = lastname
        self.id = id
        self.point = {}  # очков в каждом туре, кеy-numbertur
        self.gamers = {}  # с кем играл в туре, key-numbertur
        self.total_points = self.total_point()  # всего очков за все туры


    def win_points(self, pointt, numbertur):
        '''словарь колличество очков в каждом туре'''
        self.point[numbertur] = pointt
        self.total_point()


    def pairs_of_players(self, idd, numbertur):
        '''словарь с кем играл в каждом туре'''
        self.gamers[numbertur] = idd

    def total_point(self):
        '''сумма выигранных очков со всех турaх'''
        if len(self.point):
            self.total_points = sum(self.point.values())
        else:
            return 0

    def __repr__(self):
        return '{0}.{1} {2}: point {3} - играл с {4} - очков={5}**\n'.format(
            self.id,
            self.lastname,
            self.name,
            self.point,
            self.gamers,
            self.total_points)


class Table:
    '''создание общей турнирной таблицы'''

    def __init__(self):
        self.numbertur = 0
        self.dict_gamers = {}
        self.list_id_gamer = []
        self.nameturnir=''
        self.number_of_tuors=0
        self.tur_table_all={}

    def add_tur(self):
        self.numbertur+=1

    def table_tur_id_id(self):
        """собираем все пары в единую таблицу"""
        pass
    # def number_of_tuors(self):
    #     """рекомендуемое колличество туров"""
    #     #n-число участников
    #     # log2(n)колличество кругов
    #     # m=(N*(log2N))/2
    #     N=len(self.dict_gamers)
    #     self.number_of_tuors=(N*math.log2(N))/2

    def create_players(self, id, name, lastname):
        '''создаем экземпляры игроков ложим в словарик по id'''
        self.dict_gamers[id] = Gamer(id, name, lastname)
        self.list_id_gamer.append(id)


    def reset_players(self):
        self.dict_gamers={}
        self.numbertur=0
        self.list_id_gamer=[]
        self.nameturnir=''

    def table_game(self):
        """Создает таблицу игроков вида:
         [(id, id), (1,2), ..., (id, None)-если игроков нечетное колличество]
         """
        if self.numbertur == 0:
            chet = len(self.list_id_gamer) % 2
            if chet == 1:
                self.list_id_gamer.append(None)
            # используем в начале игры для распределения пар игроков
            game_tb = list(zip(self.list_id_gamer,
                               self.list_id_gamer[len(self.list_id_gamer) // 2:]))
            # альтернатива атрибуту в классе
            # game_tb=list(zip(self.dict_gamers.keys(),
            #             list_id_gamer[len(listt)//2:]))
        else:
            list_tb = []
            game_t = {}
            for id in self.list_id_gamer:
                if id or id == 0:
                    game_t[id] = self.dict_gamers[id].total_points
                list_tuple = game_t.items()

                # cортируем по колличеству очков заработанных во всех турах
                # получаем game_tb=[(id, self.total_points), (3, 3), (6, 3), ...]
                # game_tb=sorted(list_tuple, key=lambda x: x[1], reverse=True)

            game_tb = sorted(list_tuple, key=itemgetter(1), reverse=True)

            # если в списке игроков оказался None, игроков нечетное колличество
            # ищем игрока который не будет играть
            # последний в списке, если у него отсутствует None
            if None in self.list_id_gamer:
                for i in reversed(range(len(game_tb))):
                    # если None есть у игрокa, добавляем в список
                    if None in self.dict_gamers[game_tb[i][0]].gamers.values():
                        continue
                    else:
                        list_tb.append((game_tb[i][0], None))
                        game_tb.pop(i)
                        break

            # собираем таблицу игроков вида [0,1]
            for i in range(len(game_tb)):
                if game_tb == []: break
                print(('*' * 30), '\n', game_tb)

                for j in range(len(game_tb)):
                    if j == 0: continue

                    print(game_tb[0], '--', game_tb[j], '-=-', j)
                    list_id_2 = self.dict_gamers[game_tb[j][0]].gamers.values()

                    print(game_tb[0][0], 'in', list_id_2, '=', (game_tb[0][0] in list_id_2))

                    if not (game_tb[0][0] in list_id_2):
                        print('совпало')
                        list_tb.append((game_tb[0][0], game_tb[j][0]))
                        print('j=', j, 'list_tb ', list_tb)

                        game_tb.pop(0)
                        game_tb.pop(j - 1)

                        break
            game_tb=list_tb

        print('турнирная таблица', game_tb)

        # создаем таблицу из объектов добавляем данные
        play_tb=[]
        for id in game_tb:

            self.dict_gamers[id[0]].pairs_of_players(id[1], self.numbertur+1) #добавляем данные в объекты

            if id[1]:
                self.dict_gamers[id[1]].pairs_of_players(id[0], self.numbertur+1) #если ноне
                play_tb.append((self.dict_gamers[id[0]],
                                self.dict_gamers[id[1]]))

            else:
                play_tb.append((self.dict_gamers[id[0]],
                                None))

        try:
            if play_tb[0][1]==None:
            #проверяем наличие None в начале списка
            #если да то удаляем и вставляем в конец
                play_tb.append(play_tb.pop(0))
        except IndexError:
            return [('игра окончена')]

        #Создаем таблицу общую за все туры
        if self.numbertur:
            self.tur_table_all[self.numbertur]=play_tb


        return play_tb

    def __repr__(self):
        return '{0}'.format(self.dict_gamers)





