import re
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

import pytils as pytils

from tools import ArrTools, StrTools
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
            strDate = init_date
            if StrTools.empty(strDate):
                self.init(EMPTY_DAY, EMPTY_MONTH, EMPTY_YEAR)
            else:
                splits = re.split('[./-]', strDate)
                if ArrTools.isAllEmpty(splits):
                    self.init(EMPTY_DAY, EMPTY_MONTH, EMPTY_YEAR)

                self.init(int(splits[0]), int(splits[1]), int(splits[2]))
        # elif type(init_date).__name__ in ('datetime', 'date'):
        elif isinstance(init_date, (datetime, date)):
            dtDate = init_date
            self.init(dtDate.day, dtDate.month, dtDate.year)
        elif isinstance(init_date, type(self)):
            rdDate = init_date
            self.init(rdDate.d.day, rdDate.d.month, rdDate.d.year)

    def init(self, day, month, year):
        if year < 100:
            if year > EPOCH:
                year += 1900
            else:
                year += 2000
        self.d = datetime(year, month, day)

    @staticmethod
    def emptyDate():
        """Пустая дата"""
        return RusDate("")

    @staticmethod
    def presentDate():
        """Текущая дата"""
        return RusDate(datetime.now())

    def forSql(self):
        return self.d

    def __str__(self) -> str:
        return self.toViewString()

    def __repr__(self) -> str:
        return self.toViewString()

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

    def toViewString(self, isFullYear: bool = True, delim: str = '/'):
        """Представлени даты типа 15/02/2020"""
        if self.empty():
            return "  " + delim + "  " + delim + "    " if isFullYear else "  " + delim + "  " + delim + "  "
        day = StrTools.padl(str(self.d.day), 2, '0')
        month = StrTools.padl(str(self.d.month), 2, '0')
        strYear = str(self.d.year)
        year = strYear if isFullYear else strYear[2:]
        return day + delim + month + delim + year

    def toDDMM(self, delim: str = ''):
        """Предсавление даты типа 1520"""
        if self.empty():
            return '  ' + delim + '  '
        day = StrTools.padl(str(self.d.day), 2, '0')
        month = StrTools.padl(str(self.d.month), 2, '0')
        return day + delim + month

    def toRusString(self):
        """Предсавление даты типа 15 февраля 2020 г."""
        return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=self.d) + " г."

    def begOfMonth(self):
        """Начало месяца"""
        d = RusDate.emptyDate()
        d.init(1, self.d.month, self.d.year)
        return d

    def endOfMonth(self):
        """Конец месяца"""
        d = datetime.now()
        next_month = d.replace(day=28, month=self.d.month, year=self.d.year) + timedelta(days=4)
        d = next_month - timedelta(days=next_month.day)
        return RusDate(d)

    def begOfWeek(self):
        """Начало недели"""
        d = datetime.now()
        d = d.replace(day=self.d.day, month=self.d.month, year=self.d.year)
        d = d - timedelta(days=d.isoweekday() % 7 - 1)
        return RusDate(d)

    def endOfWeek(self):
        """Конец недели"""
        d = datetime.now()
        d = d.replace(day=self.d.day, month=self.d.month, year=self.d.year)
        d = d + timedelta(days=6 - d.weekday())
        return RusDate(d)

    def dayOfWeek(self):
        """Номер дня недели"""
        return self.d.isoweekday()

    def dayOfWeekRus(self, isShort=True):
        """День недели по русски"""
        return pytils.dt.ru_strftime(u"%" + ('a' if isShort else 'A'), inflected=True, date=self.d)

    def monthRus(self, isShort=False, inflected=False):
        return pytils.dt.ru_strftime(u"%" + ('b' if isShort else 'B'), inflected=inflected, date=self.d)

    def begOfYear(self):
        """Начало года"""
        d = RusDate.emptyDate()
        d.init(1, 1, self.d.year)
        return d

    def endOfYear(self):
        """Конец года"""
        d = RusDate.emptyDate()
        d.init(31, 12, self.d.year)
        return d

    def addMonth(self, monthes):
        """Добавить месяц"""
        return RusDate(self.d + relativedelta(months=monthes))

    def addYear(self, years):
        """Добавить год"""
        return self.addMonth(years * 12)

    def getDay(self) -> int:
        """Возвращает день"""
        return self.d.day

    def getMonth(self) -> int:
        "Возвращает номер месяца"
        return self.d.month

    def getYear(self) -> int:
        "Возращает год"
        return self.d.year

    def isBetween(self, dateFrom, dateTo) -> bool:
        """true, если между датами"""
        return dateFrom <= self <= dateTo

    @staticmethod
    def getArrBetween(dateFrom, dateTo):
        """Возвращает массив дат между датами"""
        return [dateFrom + x for x in range((dateTo-dateFrom) + 1)]

    @staticmethod
    def max(*dates):
        """Максимальная дата из списка. Список может быть подан, как список или перечисление"""
        if not dates:
            raise NotFoundException()
        try:
            return ArrTools.last(sorted(*dates))
        except:
            return ArrTools.last(sorted(dates))

    @staticmethod
    def min(*dates):
        """Минимальная дата из списка. Список может быть подан, как список или перечисление"""
        if not dates:
            raise NotFoundException()
        try:
            return ArrTools.first(sorted(*dates))
        except:
            return ArrTools.first(sorted(dates))


if __name__ == '__main__':
    print(RusDate('15/04/20'))
    print(RusDate(RusDate('15/04/20')))
    print(RusDate.presentDate())
    print(RusDate.emptyDate())
    print(RusDate.emptyDate().empty())
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
    print(RusDate('12/02/19').begOfYear())
    print(RusDate('12/02/19').endOfYear())
    print(RusDate('12/02/19').begOfMonth())
    print(RusDate('12/02/19').endOfMonth())
    print(RusDate('12/02/19').begOfWeek())
    print(RusDate('12/02/19').endOfWeek())
    # print(RusDate.max({RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')}))
    # print(RusDate.max((RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020'))))
    # print(RusDate.max([RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')]))
    print(RusDate.max(RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')))
    # print(RusDate.min({RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')}))
    # print(RusDate.min((RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020'))))
    # print(RusDate.min([RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')]))
    print(RusDate.min(RusDate('20/04/2020'), RusDate('15/04/2020'), RusDate('11/04/2020'), RusDate('05/04/2020')))
    print(RusDate('12/02/19').toDDMM())
    print(RusDate('12/02/19').toRusString())
    print(RusDate('12/02/19').next())
    print(RusDate('12/02/19').prev())
    print(RusDate('31/01/19').addMonth(1))
    print(RusDate('31/01/19').addYear(10))
    rus_date = RusDate('31/01/19')
    print(rus_date.getDay(), rus_date.getMonth(), rus_date.getYear())
    print((RusDate.presentDate()).dayOfWeek())
    print(RusDate.presentDate().dayOfWeekRus(), RusDate.presentDate().dayOfWeekRus(False))
    print(RusDate.presentDate().isBetween(RusDate("17/04/20"), RusDate("17/04/20")))
    print(RusDate.getArrBetween(RusDate("17/04/20"), RusDate("20/04/20")))
