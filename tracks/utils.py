from datetime import date, datetime, timedelta
from re import findall, fullmatch
from typing import List, NamedTuple

from tracks import parameters

# Esta función es importante para el debug, ya que nos
# permite cambiar fácilmente la hora en toda la app.
def now():
    return datetime.now()#.replace(day=9, hour=9, minute=26, second=0, microsecond=0)

def firstWeekday(reference: datetime = None) -> date:
    if reference is None:
        reference = now()
    return reference.date() - timedelta(days = reference.weekday())

def firstMonthDay(month: int, year: int = None):
    if year is None:
        year = now().year
    return date(year, month, 1)

def getRegex():
    lastShift = len(parameters.Block) - 1
    return f"([{parameters.days['short']}](?:[0-{lastShift}],)*[0-{lastShift}])"

def verifyRegex(schedule: str) -> bool:
    return fullmatch(f'{getRegex()}+', schedule) is not None

class Shift(NamedTuple):
    date: date
    block: parameters.Block

    def __repr__(self) -> str:
        return f'{self.date.isoformat()} {self.block.name}'

    @property
    def checkin(self) -> datetime:
        return datetime.combine(self.date, self.block.start)

    @property
    def checkout(self) -> datetime:
        return datetime.combine(self.date, self.block.end)

# Retorna el horario del primo, ordenado desde el turno actual (desde el punto de
# referencia <reference>) o el más cercano, hasta el más lejano.
# NOTA: Debería retornar un objeto Block y un date
def parseSchedule(schedule: str, reference: datetime = None) -> List[Shift]:
    if reference is None:
        reference = now()
    shifts = []
    
    for daily in findall(getRegex(), schedule):
        for i in daily[1:].split(','):
            block = parameters.Block[int(i)]
            checkout = datetime.combine(firstWeekday(reference), block.end) + timedelta(days=parameters.days['short'].index(daily[0]))
            # Si el turno de esta semana ya terminó, entonces lo tiro para la
            # próxima semana
            if checkout < reference:
                checkout += timedelta(days=7)
            shifts.append(Shift(checkout.date(), block))
    
    shifts.sort(key=lambda s: datetime.combine(s.date, s.block.start))
    return shifts

# Esta función, dado <date: datetime> (Fecha y hora), retornará el bloque al que
# pertenece la hora proporcionada (Si esta está dentro de los límites del bloque)
# o el bloque más cercano. Es importante recalcar que encontrará el bloque más
# cercano dentro del día de la semana indicado. Por ejemplo; si nos encontramos
# el día Martes a las 23:00, nos retornaría el Martes 1-2 de la semana siguiente
# o un error (Véase el parámetro <strinctmode>).
# <strictmode: bool>: 
#   False: Se aproxima al bloque más cercano dentro del día de la semana indicado,
#    independiente de cuanto tiempo falte para ese bloque (Podrían ser desde
#    minutos, horas o incluso semanas).
#   True: Se aproxima al bloque más cercano dentro del día de la semana indicado
#    sólo si estamos dentro de los límites de la tolerancia; si falta mucho para
#    que comience el bloque o es demasiado tarde, lanzará un error.
def aproximateToBlock(date: datetime, strictmode = True) -> Shift:
    firstHour = date.date()
    if (weekday := firstHour.weekday()) > 4:
        if strictmode:
            raise Exception(f'<date> ({date}) is not a weekday, so is not close enough to any block')
        firstHour += timedelta(days=7 - weekday)
    
    for block in parameters.Block:
        checkin = datetime.combine(firstHour, block.start)
        checkout = datetime.combine(firstHour, block.end)

        if strictmode:
            # Aproxima al siguiente bloque más cercano sólo si estamos dentro del
            # tiempo de tolerancia
            nextblockCondition = checkin - parameters.beforeStartTolerance < date < checkin # <=
        else:
            # Aproxima directamente al bloque más cercano
            nextblockCondition = date < checkin

        if (checkin <= date <= checkout) or nextblockCondition:
            return Shift(firstHour, block)
            return {
                "block": block.name,
                "checkin": checkin,
                "checkout": checkout
            }
    if strictmode:
        raise Exception(f'<date> ({date}) is not close enough to any block')
    
    return Shift(firstHour + timedelta(days=7), parameters.Block[0])
    nextWeek = timedelta(days=7)
    return {
        "block": parameters.Block[0].name,
        "checkin": checkin + nextWeek,
        "checkout": checkout  + nextWeek
    }
