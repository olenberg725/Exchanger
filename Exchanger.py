import sqlite3
# Создание базы дaнных exchanger.db
db_exchanger = sqlite3.connect('exchanger.db')
print('Подключились к базе данных')
cur = db_exchanger.cursor()
# Создание таблицы users_balance и заполнение данными тестового пользователя (10000, 1000, 1000)
cur.executescript("""CREATE TABLE IF NOT EXISTS users_balance(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Balance_RUB FLOAT NOT NULL,
    Balance_USD FLOAT NOT NULL,
    Balance_EUR FLOAT NOT NULL);

    INSERT INTO users_balance(Balance_RUB, Balance_USD, Balance_EUR)
    VALUES (10000, 1000, 1000);
""")
db_exchanger.commit()

try:
    print('Таблица users_balance создана')
    print('Тестовый пользователь создан')
    print('Добро пожаловать в наш обменный пункт, курс валют следующий:\n'
    '1 USD = 70 RUB\n'
    '1 EUR = 80 RUB\n'
    '1 USD = 0,87 EUR\n'
    '1 EUR = 1,15 USD\n')

    list_cash = [1, 2, 3]

    cash = int(input('Введите какую валюту желаете получить:\n'
                    '1. RUB\n'
                    '2. USD\n'
                    '3. EUR\n'
                 'Введите номер валюты:\n'))

    amount = float(input('Какая сумма Вас интересует?\n'))

    cash_in_return = int(input('Какую валюту готовы предложить взамен?\n'
                            '1. RUB\n'
                            '2. USD\n'
                            '3. EUR\n'
                           'Введите номер валюты:\n'))

    def database_query():
        # Запрос содержимого таблицы с балансом
        cur.execute("""SELECT Balance_RUB, Balance_USD, Balance_EUR FROM users_balance""")
        query = cur.fetchone()
        result = []
        for i in range(len(query)):
            result.append(query[i])
        # Возвращаем содержимое в виде списка
        return result

    def rate(cash, cash_in_return):
        # Выбор коэффициента, соответствующего обмену валют
        if cash == 2 and cash_in_return == 1:
            return 70
        elif cash == 3 and cash_in_return == 1:
            return 80
        elif cash == 2 and cash_in_return == 3:
            return 0.87
        elif cash == 1 and cash_in_return == 2:
            return 1/70
        elif cash == 3 and cash_in_return == 2:
            return 1.15
        else:
            return 1/80


    def database_update(lists):
        # Внесение изменений в БД после совершения обмена
        checklist = tuple(lists)
        cur.execute("""UPDATE users_balance SET Balance_RUB = (?), Balance_USD = (?), Balance_EUR = (?);""", checklist)
        db_exchanger.commit()
        # Вывод баланса после совершения обмена
        print(database_query())

    def lack_of_funds(amount, value, k):
        if value < amount * k:
            return (f'Обмен не возможен. На вашем счете недостаточно средств. Попробуйте выбрать сумму поменьше.')
        else:
            return amount * k

    def transaction(cash, cash_in_return, amount, k):
        list_of_cash = database_query()
        first = list_of_cash[cash - 1]
        second = list_of_cash[cash_in_return - 1]
        print(list_of_cash)
        difference = lack_of_funds(amount, second, k)
        if type(difference) != str:
            first += amount
            second -= difference
            list_of_cash[cash - 1] = '{:6.2f}'.format(first)
            list_of_cash[cash_in_return - 1] = '{:6.2f}'.format(second)
            database_update(list_of_cash)
            return f'Обмен валют выполнен.'
        else:
            return difference


    if cash in list_cash and cash_in_return in list_cash:
        if amoumt > 0:
            if cash == cash_in_return:
                print('Невозможно производить обмен двух одинаковых валют')
            else:
                k = rate(cash, cash_in_return)
                print(transaction(cash, cash_in_return, amount, k))
        else:
            print('Невозможно обменять отрицательную или равную нулю сумму')
    else:
        print('Обмен валют невозможен')

except:
    print('Для выбора валюты вводите ее номер\n'
          'RUS - 1\n'
          'USD - 2\n'
          'EUR - 3\n')

# cur.execute("""DROP TABLE users_balance""")
# db_exchanger.commit()