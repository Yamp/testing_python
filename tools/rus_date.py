import re
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

import pytils as pytils

from tools import arrtools, strtools
from tools.exceptions import NotFoundException

EMPTY_YEAR = 1900
EMPTY_MONTH = 1
EMPTY_DAY = 1
EPOCH = 60


@dataclass(order=True)
class RusDate:
    d: datetime

    def __init__(self, init_date) -> None:
        """
        Конструктор
        :param init_date: может быть строка '15/01/2000', datetime, date, RusDate
        """
        if isinstance(init_date, str):
            str_date = init_date
            if strtools.empty(str_date):
                self.init(EMPTY_DAY, EMPTY_MONTH, EMPTY_YEAR)
            else:
                splits = re.split('[./-]', str_date)
                if arrtools.is_all_empty(splits):
                    self.init(EMPTY_DAY, EMPTY_MONTH, EMPTY_YEAR)

                self.init(int(splits[0]), int(splits[1]), int(splits[2]))
        # elif type(init_date).__name__ in ('datetime', 'date'):
        elif isinstance(init_date, (datetime, date)):
            dt_date = init_date
            self.init(dt_date.day, dt_date.month, dt_date.year)
        elif isinstance(init_date, type(self)):
            rd_date = init_date
            self.init(rd_date.d.day, rd_date.d.month, rd_date.d.year)

    def init(self, day, month, year):
        if year < 100:
            if year > EPOCH:
                year += 1900
            else:
                year += 2000
        self.d = datetime(year, month, day)

    @staticmethod
    def empty_date():
        """Пустая дата"""
        return RusDate("")

    @staticmethod
    def present_date():
        """Текущая дата"""
        return RusDate(datetime.now())

    def for_sql(self, as_string: bool = False):
        if as_string:
            return "to_date('" + str(self.get_year()) \
                   + '-' + strtools.padl(str(self.get_month()), 2, '0') \
                   + '-' + strtools.padl(str(self.get_day()), 2, '0') + "', 'YYYY-MM-DD')"
        if self.empty():
            return None
        return self.d

    def __str__(self) -> str:
        return self.to_view()

    def __repr__(self) -> str:
        return self.to_view()

    def __add__(self, days):
        return RusDate(self.d + timedelta(days=days))

    def __sub__(self, p):
        if isinstance(p, int):
            days = p
            return RusDate(self.d - timedelta(days=days))
        elif type(p).__name__ == 'RusDate':
            rd = p
            delta = self.d - rd.d
            return delta.days

    def __hash__(self):
        return self.d.__hash__()

    def next(self):
        """Следующая дата"""
        return RusDate(self.d + timedelta(days=1))

    def prev(self):
        """Предыдущая дата"""
        return RusDate(self.d - timedelta(days=1))

    def empty(self) -> bool:
        """true, если дата пустая"""
        return self.d.day == EMPTY_DAY and self.d.month == EMPTY_MONTH and self.d.year == EMPTY_YEAR

    def to_view(self, is_fill_year: bool = True, delim: str = '/'):
        """Представлени даты типа 15/02/2020"""
        if self.empty():
            return "  " + delim + "  " + delim + "    " if is_fill_year else "  " + delim + "  " + delim + "  "
        day = strtools.padl(str(self.d.day), 2, '0')
        month = strtools.padl(str(self.d.month), 2, '0')
        str_year = str(self.d.year)
        year = str_year if is_fill_year else str_year[2:]
        return day + delim + month + delim + year

    def to_ddmm(self, delim: str = ''):
        """Предсавление даты типа 1520"""
        if self.empty():
            return '  ' + delim + '  '
        day = strtools.padl(str(self.d.day), 2, '0')
        month = strtools.padl(str(self.d.month), 2, '0')
        return day + delim + month

    def to_rus_str(self):
        """Предсавление даты типа 15 февраля 2020 г."""
        return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.d) + " г."

    def beg_month(self):
        """Начало месяца"""
        d = RusDate.empty_date()
        d.init(1, self.d.month, self.d.year)
        return d

    def end_month(self):
        """Конец месяца"""
        d = datetime.now()
        next_month = d.replace(day=28, month=self.d.month, year=self.d.year) + timedelta(days=4)
        d = next_month - timedelta(days=next_month.day)
        return RusDate(d)

    def beg_week(self):
        """Начало недели"""
        d = datetime.now()
        d = d.replace(day=self.d.day, month=self.d.month, year=self.d.year)
        d = d - timedelta(days=d.isoweekday() % 7 - 1)
        return RusDate(d)

    def end_week(self):
        """Конец недели"""
        d = datetime.now()
        d = d.replace(day=self.d.day, month=self.d.month, year=self.d.year)
        d = d + timedelta(days=6 - d.weekday())
        return RusDate(d)

    def day_week(self) -> int:
        """Номер дня недели"""
        return self.d.isoweekday()

    def day_week_rus(self, is_short=True) -> str:
        """День недели по русски"""
        return pytils.dt.ru_strftime(u"%" + ('a' if is_short else 'A'), inflected=True, date=self.d)

    def month_rus(self, is_short=False, inflected=False) -> str:
        return pytils.dt.ru_strftime(u"%" + ('b' if is_short else 'B'), inflected=inflected, date=self.d)

    def beg_year(self):
        """Начало года"""
        d = RusDate.empty_date()
        d.init(1, 1, self.d.year)
        return d

    def end_year(self):
        """Конец года"""
        d = RusDate.empty_date()
        d.init(31, 12, self.d.year)
        return d

    def add_month(self, monthes):
        """Добавить месяц"""
        return RusDate(self.d + relativedelta(months=monthes))

    def add_year(self, years):
        """Добавить год"""
        return self.add_month(years * 12)

    def get_day(self) -> int:
        """Возвращает день"""
        return self.d.day

    def get_month(self) -> int:
        "Возвращает номер месяца"
        return self.d.month

    def get_year(self) -> int:
        "Возращает год"
        return self.d.year

    def is_between(self, date_from, date_to) -> bool:
        """true, если между датами"""
        return date_from <= self <= date_to

    @staticmethod
    def get_arr_between(date_from, date_to):
        """Возвращает массив дат между датами"""
        return [date_from + x for x in range((date_to - date_from) + 1)]

    @staticmethod
    def max(*dates):
        """Максимальная дата из списка. Список может быть подан, как список или перечисление"""
        if not dates:
            raise NotFoundException()
        try:
            return arrtools.last(sorted(*dates))
        except:
            return arrtools.last(sorted(dates))

    @staticmethod
    def min(*dates):
        """Минимальная дата из списка. Список может быть подан, как список или перечисление"""
        if not dates:
            raise NotFoundException()
        try:
            return arrtools.first(sorted(*dates))
        except:
            return arrtools.first(sorted(dates))


if __name__ == '__main__':
    print(RusDate('15/04/20'))
    print(RusDate(RusDate('15/04/20')))
    print(RusDate.present_date())
    print(RusDate.empty_date())
    print(RusDate.empty_date().empty())
    print(RusDate(datetime.now()) + 5)
    print(RusDate(datetime.now()) - 5)
    print(RusDate(datetime.now()) - RusDate('10/04/20'))
    print(RusDate('15/04/2020') == RusDate('15/04/2020'))
    print(RusDate('15/04/2020') != RusDate('15/04/2020'))
    print(RusDate('15/04/2020') > RusDate('14/04/2020'))
    print(RusDate('15/04/2020') < RusDate('14/04/2020'))
    print(RusDate('15/04/2020') <= RusDate('14/04/2020'))
    print(RusDate('15/04/2020') >= RusDate('14/04/2020'))
    l = [RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020'),
         RusDate('05/04/2020')]
    print(sorted(l))
    s = {RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020'),
         RusDate('05/04/2020')}
    print(sorted(s))
    print(RusDate('12/02/19').beg_year())
    print(RusDate('12/02/19').end_year())
    print(RusDate('12/02/19').beg_month())
    print(RusDate('12/02/19').end_month())
    print(RusDate('12/02/19').beg_week())
    print(RusDate('12/02/19').end_week())
    # print(RusDate.max({RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')}))
    # print(RusDate.max((RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020'))))
    # print(RusDate.max([RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')]))
    print(RusDate.max(RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')))
    # print(RusDate.min({RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')}))
    # print(RusDate.min((RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020'))))
    # print(RusDate.min([RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')]))
    print(RusDate.min(RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')))
    print(RusDate('12/02/19').to_ddmm())
    print(RusDate('12/02/19').to_rus_str())
    print(RusDate('12/02/19').next())
    print(RusDate('12/02/19').prev())
    print(RusDate('31/01/19').add_month(1))
    print(RusDate('31/01/19').add_year(10))
    rus_date = RusDate('31/01/19')
    print(rus_date.get_day(), rus_date.get_month(), rus_date.get_year())
    print((RusDate.present_date()).day_week())
    print(RusDate.present_date().day_week_rus(), RusDate.present_date().day_week_rus(False))
    print(RusDate.present_date().is_between(RusDate("17/04/20"), RusDate("17/04/20")))
    print(RusDate.get_arr_between(RusDate("17/04/20"), RusDate("20/04/20")))
