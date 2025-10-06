from datetime import datetime

inputdata = "continue"

base = []
goods = dict()
allgoods = []
categories = []
fund = 0
maxfund = 10**12
username = ""
boughts = []


# Открытие файла, режим открытия, ошибка при невозможности открытия
def open_file(filename, error, mode="r"):
    try:
        return open(filename, mode)
    except:
        print(error)
        return None


# считывание профилей из файла
def make_base():
    global base
    file = open_file("../profiles.txt",
                     "Созданные пользователи не найдены.")
    if file is not None:
        for i in file:
            base.append(i.strip())
        file.close()
        return False
    return True


# считывание товаров из файла
def read_goods():
    global categories, goods
    file = open_file("../goods.txt",
                     "Товары и категории не найдены.")
    if file is not None:
        category = ""
        for i in file:
            if i[0] == "-":
                category, upprice = i[1:].strip().split()
                upprice = int(upprice)
                categories.append([category, upprice])
                goods[category] = []
            else:
                good, price = i.strip().split()
                price = int(price)
                allgoods.append(good)
                goods[category].append([good, price])
            goods[category].sort(key=lambda x: x[1])
        categories.sort(key=lambda x: x[0])
        file.close()
        return False
    return True


# запись профилей в файл
def save_base():
    global base
    file = open_file("../profiles.txt", "Невозможно сохранить базу пользователей.", 'w')
    if file is not None:
        for i in base:
            file.write(i + "\n")
        file.close()
        return False
    return True


# запись товаров в файл
def save_goods():
    global base
    file = open_file("../goods.txt", "Невозможно сохранить категории и товары.", 'w')
    if file is not None:
        for i in categories:
            file.write(f"-{i[0]} {i[1]}\n")
            for j in goods[i[0]]:
                file.write(f"{j[0]} {j[1]}\n")
        file.close()
        return False
    return True


# сохранение информации о пользователе
def save_info():
    global username, fund
    if username != "":
        file = open_file(username + ".txt", "Невозможно сохранить статистику пользователя.", 'w')
        if file is not None:
            file.write(str(fund) + "\n")
            for i in boughts:
                file.write(f"{i[0]} {i[1]} {i[2]} {str(i[3])}\n")
            file.close()
            return False
        return True
    return False


# остановка программы
def stop():
    raise StopIteration


# проверяемый вход: вывод на экран, список с возможными ответами и ошибка при не соответствии,
# список ответов не удовлетворяющих условию
def check_input(output, keystoexit, error, keystorestart=None):
    uinput = ""
    flag = True if keystorestart is None else False
    if keystorestart is None:
        restart = [""]
    else:
        restart = keystorestart + [""]

    while ((uinput not in keystoexit or uinput in restart) and flag
           or not flag and uinput not in keystoexit and uinput in restart):
        uinput = input(output).lower().replace('\"', '')

        if uinput == "выход":
            stop()
        if ((uinput not in keystoexit or uinput in restart) and flag
                or (not flag and uinput not in keystoexit and uinput in restart)):
            print(error)
        print()
    return uinput


# проверяемый вход на определённый тип данных
def check_type_input(output, indata, errorsfortypes, types):
    # uinput = ""

    while True:
        uinput = input(output).lower()

        if uinput == "выход":
            stop()
        if uinput == "назад":
            return uinput

        for i in range(len(types)):
            try:
                if types[i] == indata:
                    uinput = indata(uinput)
                    return uinput
                types[i](uinput)
            except:
                print(errorsfortypes[i])
                break
        print()
    # return uinput


def num_less_than(output, upborder, sup="Число должно", indata=int, errorsfortypes=None, types=None):
    if types is None:
        types = [float, indata]
    if errorsfortypes is None:
        errorsfortypes = ["Нужно ввести число.", "Нужно ввести целое число."]
    num = -1

    while num <= 0 or num > upborder:
        num = check_type_input(output, indata, errorsfortypes, types)
        if num == "назад":
            return num
        if 0 < num < upborder:
            return num
        elif num > upborder:
            print(f'{sup} быть меньше {upborder}.')
        elif num <= 0:
            print(f"{sup} быть больше нуля.")
    return num


# вход в программу
def start():
    logIn = ""
    entry = None
    while True:
        if entry is None and logIn not in ["войти", "создать"]:
            logIn = check_input("Вы хотите \"войти\" в профиль или \"создать\" новый: ",
                                ["войти", "создать"],
                                "Некорректный ввод, попробуйте выбрать ответ из представленных в кавычках.")

        if logIn == "войти":
            logIn, entry = log_in()
        elif logIn == "создать":
            logIn, entry = create()
        if entry:
            return logIn


# создание профиля
def create():
    global base
    locUsername = check_input("Введите имя пользователя или команду \"войти\", чтобы войти в профиль: ",
                           ["войти"],
                           "Введённое имя уже занято."
                           "\nВозможно вы уже зарегистрировались, тогда попробуйте войти в профиль",
                           keystorestart=base)
    if locUsername == "войти":
        return locUsername, None
    base.append(locUsername)
    print(f"Добро пожаловать в систему, {locUsername}!")
    return locUsername, True


# вход в профиль
def log_in():
    global base
    unbase = base + ["создать"]
    locUsername = check_input("Введите имя пользователя или команду \"создать\", чтобы создать новый профиль: ",
                           unbase,
                           "Имя пользователя не найдено, возможно его нет в базе."
                           "\nПроверьте введённое имя пользователя на ошибки или попробуйте создать нового "
                           "пользователя.")
    if locUsername == "создать":
        return locUsername, None
    print(f"Добро пожаловать в систему, {locUsername}!")
    return locUsername, True


# основная часть программы
def main():
    global username

    print("Запуск сервиса...")
    print("Загрузка данных...")
    # errors = False
    locErrors = make_base()
    locErrors = read_goods() if not locErrors else True
    if not locErrors:
        print("Загрузка данных прошла успешно.")
    print("Сервис запущен")
    print()

    print("Добрый день, пользователь, для продолжения работы необходимо войти в профиль"
          " или создать новый.\nДля выхода из системы необходимо написать \"выход\".\n")

    username = start()

    info_about_user(username)
    actions()
    # stop()


# составление информации о пользователе
def info_about_user(locUsername):
    global fund, maxfund
    fund = -1
    try:
        file = open(locUsername + ".txt")
        fund = int(file.readline())
        for i in file:
            try:
                name, cost, category, data = i.strip().split()
                cost = int(cost)
                data = datetime(*list(map(int, data.split("-")))).date()
                boughts.append([name, cost, category, data])
            except:
                break
        print(f"Ваш бюджет {fund}")
        boughts.sort(key=lambda x: x[1])
    except:
        fund = num_less_than("Введите ваш бюджет: ", maxfund, "Бюджет должен")
        print(f"Ваш бюджет {fund}")
    print()


# действия для пользователя
def actions():
    global fund
    while True:
        action = check_input(f"Ваш бюджет составляет {fund}.\n"
                             "Выберите действие, которое хотите совершить. (достаточно ввести номер действия)"
                             "\nДействия:"
                             "\n1. просмотреть товары"
                             "\n2. купить товар"
                             "\n3. удалить данные о покупке"
                             "\n4. просмотреть покупки"
                             "\n5. добавить товар"
                             "\n6. удалить товар"
                             "\n7. изменить бюджет\n" + "Для выхода из системы необходимо написать \"выход\".\n",
                             ["просмотреть товары", "купить товар",
                              "удалить данные о покупке", "просмотреть покупки",
                              "добавить товар", "удалить товар", "изменить бюджет",
                              "1", "2", "3", "4", "5", "6", "7"],
                             "Введенная строка не является возможным действием.")

        if action == "просмотреть товары" or action == "1":
            present_goods()
        if action == "купить товар" or action == "2":
            buy_goods()
        if action == "удалить данные о покупке" or action == "3":
            delete_bought()
        if action == "просмотреть покупки" or action == "4":
            view_bougths()
        if action == "добавить товар" or action == "5":
            add_good()
        if action == "удалить товар" or action == "6":
            delete_good()
        if action == "изменить бюджет" or action == "7":
            vary_fund()
        print()


# Просмотр всех товаров
def present_goods():
    global categories, goods
    for i in categories:
        if goods[i[0]]:
            print(f"{i[0]}:")
            for j in range(len(goods[i[0]])):
                print(f"{j + 1}. {goods[i[0]][j][0]} - стоимость {goods[i[0]][j][1]}.")


# Купить товар
def buy_goods():
    global categories, goods, fund, boughts
    locBase = [i[0] for i in categories if goods[i[0]]]
    numbase = [str(i + 1) for i in range(len(categories)) if goods[categories[i][0]]]
    if categories:
        while True:
            category = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                                   "Категории товаров:\n" +
                                   "\n".join([(f"{i + 1}. " + categories[i][0])
                                              for i in range(len(categories)) if goods[categories[i][0]]]) +
                                   "\nВыберите категорию товаров: ",
                                   locBase + numbase + ["назад"],
                                   "Введённой категории не существует.")

            if category == "назад":
                return
            if category in numbase:
                category = locBase[int(category) - 1]
            gbase, gnumbase = [i[0] for i in goods[category]], [str(i + 1) for i in range(len(goods[category]))]

            good = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                               f"Товары:\n" + "\n".join([f"{i + 1}. " +
                                                         goods[category][i][0] + " - " +
                                                         str(goods[category][i][1]) for i in
                                                         range(len(goods[category]))]) +
                               f"\nВыберите товар из категории {category}: ",  # выбор товара из категории
                               gbase + gnumbase + ["назад"],
                               "Выбранного товара не существует.")

            if good == "назад":
                return
            if good in gnumbase:
                good = gbase[int(good) - 1]

            for i in goods[category]:  # проверка на возможность покупки
                if i[0] == good and i[1] <= fund:
                    fund -= i[1]
                    boughts = place_in_array(boughts, good, i[1], [category, datetime.now().date()])

                    print(f"Товар - {i[0]} - куплен. Осталось средств: {fund}.")
                    return
                elif i[0] == good and i[1] > fund:
                    print(f"Недостаточно средств для покупки товара. Осталось средств: {fund}")
                    exit = check_input("Вы хотите выйти из покупки товара? Введите \"да\" или \"нет\": ",
                                       ["да", "нет"],
                                       "Подразумевается ответ \"да\" или \"нет\".")
                    if exit == "да":
                        return


def place_in_array(array, good, price, addit=None):
    if addit is None:
        addit = []
    length = len(array)

    for i in range(length):
        if price < array[i][1]:
            array.insert(i, [good, price] + addit)
            return array
    array.append([good, price] + addit)
    return array


def delete_bought():  # удаление записей о покупке
    global boughts
    numbase = [str(i + 1) for i in range(len(boughts))]
    if boughts:
        good = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                           "Совершённые покупки:\n" + '\n'.join([f'{i + 1}. Товар {boughts[i][0]} куплен '
                                                                 f'{f"{boughts[i][3].day}.{boughts[i][3].month}.{boughts[i][3].year}"}'
                                                                 f' за {boughts[i][1]}' for i in range(len(boughts))]) +
                           "\nВыберите намер покупки, данные о которой вы хотите стереть (стоимость товара не "
                           "вернётся в бюджет): ",
                           # выбор товара для возврата
                           numbase + ["назад"],
                           "Выбранного номера покупки нет.")

        if good == "назад":
            return
        if good in numbase:
            good = int(good) - 1
            print(f"Запись о покупке {boughts[good][0]} за {boughts.pop(good)[1]} удалена.")
    else:
        print("Вы ещё не совершали покупок.")


def view_bougths():  # Просмотр покупок
    global boughts
    locBase = []
    catbase = []
    for i in range(len(boughts)):
        sup = f"{boughts[i][3].day}.{boughts[i][3].month}.{boughts[i][3].year}"
        if sup not in locBase:
            locBase.append(sup)
        if boughts[i][2] not in catbase:
            catbase.append(boughts[i][2])
    catbase.sort()
    locBase.sort(key=lambda x: [int(x.split(".")[0]), int(x.split(".")[1]), int(x.split(".")[2])])
    dbase = [str(i + 1) for i in range(len(locBase))]
    cbase = [str(i + 1) for i in range(len(catbase))]

    sorttype = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                           "Вас интересуют:\n"
                           "1. \"все\" покупки\n"
                           "2. \"дата\" совершения покупок\n"
                           "3. \"категория\" покупок\n"
                           "Выберите критерий вывода покупок: ",
                           ["все", "дата", "категория", "назад", "1", "2", "3"],
                           "Невозможно вывести покупки по введённому критерию. ")
    if sorttype == "назад":
        return
    if sorttype in ["1", "2", "3"]:
        sorttype = ["все", "дата", "категория"][int(sorttype) - 1]
    if sorttype in ["все", "дата", "категория"]:
        crease = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                             "Вывести покупки:\n"
                             "1. \"по возрастанию\" цены\n"
                             "2. \"по убыванию\" цены\n"
                             "Выберите способ сортировки покупок: ",
                             ["по возрастанию", "по убыванию", "назад", "1", "2"],
                             "Покупки возможно сортировать только \"по возрастанию\" или \"по убыванию\".")
        if crease == "назад":
            return
        if crease in ["1", "2"]:
            crease = ["по возрастанию", "по убыванию"][int(crease) - 1]

        direct = 1 if crease == "по возрастанию" else -1
        if sorttype == "все":
            for i in boughts[::direct]:
                print(f"Товар - {i[0]} - куплен за {i[1]}.")
            return

        if sorttype == "дата":
            date = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +  # фиксим
                               "Даты покупок:\n" + "\n".join([f"{i}. " + locBase[int(i) - 1] for i in dbase]) +
                               "\nВыберите порядковый номер даты, за которую вы хотите просмотреть покупки: ",
                               dbase + ["назад"],
                               "Даты с таким номером не существует.")

            if date == "назад":
                return
            if date in dbase:
                date = locBase[int(date) - 1]

            for i in boughts[::direct]:
                if f"{i[3].day}.{i[3].month}.{i[3].year}" == date:
                    print(f"Товар - {i[0]} - куплен за {i[1]}.")
            return

        if sorttype == "категория":
            category = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                                   "Категории покупок:\n" + "\n".join([f"{i}. {catbase[int(i) - 1]}" for i in cbase]) +
                                   "\nВведите категорию покупок: ",
                                   catbase + cbase + ["назад"],
                                   "Введённой категории покупок нет.")
            if category == "назад":
                return
            if category in cbase:
                category = catbase[int(category) - 1]

            for i in boughts[::direct]:
                if i[2] == category:
                    print(f"Товар - {i[0]} - куплен за {i[1]}.")
            return


# Добавить товар
def add_good():
    global goods, categories, maxfund, allgoods
    unbase = [i[0] for i in categories]
    numbase = [str(i + 1) for i in range(len(unbase))]
    upcost = 0
    created = False

    while True:  # выбор или создание категории
        categoryname = input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                             "Введите категорию, в которую хотите добавить товар.\n"
                             "Категории:\n" + "\n".join([f"{i}. {unbase[int(i) - 1]}" for i in numbase]) + "\n"
                             "Создайте новую или выберите из списка категорий: ").lower()
        if categoryname == "выход":
            stop()
        if categoryname == "назад":
            return
        if categoryname in numbase:
            categoryname = unbase[int(categoryname) - 1]
        if categoryname in unbase:
            if upcost == 0:
                upcost = categories[unbase.index(categoryname)][1]
            break
        print()

        if categoryname not in unbase:  # создание категории
            new = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                              f"Вы хотите создать категорию {categoryname}? Введите \"да\" или \"нет\": ",
                              ["да", "нет"] + ["назад"],
                              "Подразумевается ответ \"да\" или \"нет\".")
            if new == "назад":
                return
            if new == "да":
                print()
                upcost = num_less_than("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                                       "Укажите максимальную стоимость товаров в категории: ", maxfund,
                                       "Стоимость должна")
                created = True
                if upcost == "назад":
                    return
                break
            # else:
            #     continue
    print()

    # создание товара
    goodname = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                           "Введенный товар должен отсутствовать во всех категориях. Введите название товара: ",
                           ["назад"],
                           "Данный товар уже существует.",
                           keystorestart=allgoods)

    if goodname == "назад":
        return

    print()
    cost = num_less_than("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                         "Введите стоимость товара: ", upcost, "Стоимость товара должна")

    if cost == "назад":
        return

    if created:
        categories.append([categoryname, upcost])
        goods[categoryname] = []
    goods[categoryname] = place_in_array(goods[categoryname], goodname, cost)
    allgoods.append(goodname)

    print(f"Товар - {goodname} - успешно добвален в категорию - {categoryname}.")


def delete_good():  # удаление товара
    global categories, goods
    unbase = [i[0] for i in categories]
    numbase = [str(i + 1) for i in range(len(unbase))]
    category = check_input(
        "Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +  # выбор категории для покупки товара
        "Категории товаров:\n" + "\n".join([(f"{i}. " + unbase[int(i) - 1] + "") for i in numbase]) +
        "\nВыберите категорию товаров: ",
        unbase + numbase + ["назад"],
        "Введённой категории не существует.")
    if category == "назад":
        return
    if category in numbase:
        category = unbase[int(category) - 1]

    gbase = [(i[0], i[1]) for i in goods[category]]
    gnumbase = [str(i + 1) for i in range(len(gbase))]

    good = check_input("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +  # выбор товара из категории
                       f"Товары:\n" + "\n".join(
                        [f"{i}. " + gbase[int(i) - 1][0] + " - " + str(gbase[int(i) - 1][1]) for i in gnumbase]) +
                       f"\nВыберите товар из категории {category}: ",
                       [i[0] for i in gbase] + gnumbase + ["назад"],
                       "Выбранного товара не существует.")

    if good == "назад":
        return
    if good in gnumbase:
        good = gbase[int(good) - 1][0]

    new_goods = []
    for i in goods[category]:
        if i[0] != good:
            new_goods.append(i)
    goods[category] = new_goods[::]
    print(f"Товар - {good} - удалён.")


def vary_fund():  # изменить бюджет
    global fund, maxfund
    print(f"Ваш бюджет составлял {fund}.")
    cur = num_less_than("Если вы хотите вернуться к выбору действий, введите \"назад\".\n" +
                        "Введите новый бюджет: ", maxfund, "Бюджет должен")
    if cur == "назад":
        return
    fund = cur


if __name__ == '__main__':
    try:
        main()
    except StopIteration:
        print()
        print("Сохранение данных...")
        # errors = False
        errors = save_base()
        errors = save_goods() if not errors else True or save_goods()
        errors = save_info() if not errors else True or save_info()
        if not errors:
            print("Данные успешно сохранены.")
        print()

        print("Спасибо за использование сервиса")