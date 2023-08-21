class User:
    def __init__(self, first_name, last_name, patronymic, organisation_name, personal_phone, work_phone):
        self.f_name = first_name
        self.l_name = last_name
        self.patronymic = patronymic
        self.org_name = organisation_name
        self.pers_phone = personal_phone
        self.work_phone = work_phone

    def __str__(self):
        return f'{self.f_name} {self.l_name} {self.patronymic} {self.org_name} {self.work_phone} {self.pers_phone}\n'


class User:
    def __init__(self, first_name: str, last_name: str, patronymic: str, organisation_name: str,
                 personal_phone: str, work_phone: str):
        """
        Represents a user in the phone book.

        Args:
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            patronymic (str): Patronymic of the user.
            organisation_name (str): Name of the organization.
            personal_phone (str): Personal phone number of the user.
            work_phone (str): Work phone number of the user.
        """
        self.f_name = first_name
        self.l_name = last_name
        self.patronymic = patronymic
        self.org_name = organisation_name
        self.pers_phone = personal_phone
        self.work_phone = work_phone

    def __str__(self):
        """
        Returns a formatted string representation of the user.

        Returns:
            str: Formatted user information.
        """
        return f'{self.f_name} {self.l_name} {self.patronymic} {self.org_name} {self.work_phone} {self.pers_phone}\n'


class PhoneBook:
    def __init__(self, file_name: str):
        """
        Represents a phone book.

        Args:
            file_name (str): Name of the file to store phone book data.
        """
        self.file_name = file_name
        self.paginate_value = 2

    def _read_file(self):
        """
        Read the content of the file.

        Returns:
            list: List of lines read from the file.
        """
        try:
            with open(self.file_name, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            return []

    def get_all_data(self, paginate: int = 1):
        """
        Get a list of user records from the phone book.

        Args:
            paginate (int): Page number to retrieve data from.

        Returns:
            list: List of user records.
        """
        records_list = []
        lines = self._read_file()
        for line in lines[paginate - 1: paginate + self.paginate_value - 1]:
            user_data = line.split()
            user_dict = {
                'f_name': user_data[0],
                'l_name': user_data[1],
                'patronymic': user_data[2],
                'org_name': user_data[3],
                'work_phone': user_data[4],
                'pers_phone': user_data[5]
            }
            records_list.append(user_dict)
        return records_list

    def add_user(self, user: User):
        """
        Add a user to the phone book.

        Args:
            user (User): User object to be added.

        Returns:
            bool: True if user was added successfully.
        """
        with open(self.file_name, 'a') as file:
            file.write(user.__str__())
        return True

    def edit_record(self, user: User, first_name: str, last_name: str, patronymic: str,
                    organisation_name: str, personal_phone: str, work_phone: str):
        """
        Edit a user record in the phone book.

        Args:
            user (User): User object to be edited.
            first_name (str): New first name.
            last_name (str): New last name.
            patronymic (str): New patronymic.
            organisation_name (str): New organization name.
            personal_phone (str): New personal phone number.
            work_phone (str): New work phone number.
        """
        new_data = User(first_name, last_name, patronymic, organisation_name, personal_phone, work_phone)
        lines = self._read_file()
        updated_lines = [line.replace(user.__str__(), new_data.__str__()) if user.__str__() in line else line for line in lines]
        with open(self.file_name, 'w') as file:
            file.writelines(updated_lines)

    def get_records(self, **kwargs):
        """
        Get a list of user records that match the specified criteria.

        Args:
            **kwargs: Keyword arguments representing search criteria.

        Returns:
            list: List of user records matching the criteria.
        """
        if not kwargs:
            return []

        user_list = []
        lines = self._read_file()
        for line in lines:
            user_data = line.split()
            user_dict = {
                'f_name': user_data[0],
                'l_name': user_data[1],
                'patronymic': user_data[2],
                'org_name': user_data[3],
                'work_phone': user_data[4],
                'pers_phone': user_data[5]
            }

            if all(user_dict.get(key) == value for key, value in kwargs.items()):
                user = User(*user_data)
                user_list.append(user)

        return user_list


def search_record(phonebook: PhoneBook, for_user=True):
    search_data = {}
    option = None
    records = []

    while True:
        print("Выберите поле, по которому хотите найти. \n\t1. Имя\n\t2. Фамилия\n\t3. Отчество \n\t4. "
              "Название организации \n\t5. Рабочий номер\n\t6. Личный номер "
              "\n\t7. Начать поиск")
        if for_user:
            print('\t8. Вернуться в главное меню ')
        else:
            print('\t8. Выбрать запись')

        option = int(input())
        if option == 7:
            if len(search_data) == 0:
                print('Введите хотя бы один параметр')
            else:
                records = phonebook.get_records(**search_data)

                for user in records:
                    print(f'Имя - {user.f_name}')
                    print(f'Фамилия - {user.l_name}')
                    print(f'Отчество - {user.patronymic}')
                    print(f'Организация - {user.org_name}')
                    print(f'Рабочий телефон - {user.work_phone}')
                    print(f'Личный телефон - {user.pers_phone}')
                    print()
        elif option == 8:
            if for_user:
                break
            else:
                return records
        else:
            option_name = None
            if option == 1:
                option_name = 'f_name'
            elif option == 2:
                option_name = 'l_name'
            elif option == 3:
                option_name = 'patronymic'
            elif option == 4:
                option_name = 'org_name'
            elif option == 5:
                option_name = 'work_phone'
            elif option == 6:
                option_name = 'pers_phone'

            if option_name:
                option_value = input(f'Введите значение параметра: ')
                search_data[option_name] = option_value


def edit_record(PB: PhoneBook):
    choose = int
    while choose != 2:
        print('Найдите запись, которую собираетесь изменить\n')

        records_list = search_record(PB, False)
        for ind, record in enumerate(records_list):
            print(f'{ind + 1} - {record}')

        record_number = int(input('Введите номер нужной вам записи'))
        record = records_list[record_number - 1]

        print('Создайте новую запись:\n')
        f_name = input('Введите имя:')
        l_name = input('Введите фамилию:')
        patronymic = input('Введите отчество:')
        org_name = input('Введите название организации:')
        work_phone = input('Введите рабочий телефон:')
        pers_phone = input('Введите личный телефон:')

        PB.edit_record(record, f_name, l_name, patronymic, org_name, work_phone, pers_phone)
        print('Запись заменена!\n')
        choose = int(input('\t1. Изменить еще одну запись\n\t2. Перейти в главное меню'))


def show_records():
    choose_page = 1
    paginate_value = 1

    while choose_page != 3:
        data = PB.get_all_data(paginate=paginate_value)
        for user in data:
            for key, value in user.items():
                print(f'{key} - {value}')
            print()
        print('Выберите действие: \n\t1. Показать предыдущую страницу \n\t2. Показать следующую страницу'
              '\n\t3. Перейти в главное меню ')
        choose_page = int(input())
        if choose_page == 1:
            paginate_value -= PB.paginate_value
        elif choose_page == 2:
            paginate_value += PB.paginate_value
        elif choose_page == 3:
            break


def add_record():
    choose = int
    while choose != 2:
        f_name = input('Введите имя:')
        l_name = input('Введите фамилию:')
        patronymic = input('Введите отчество:')
        org_name = input('Введите название организации:')
        work_phone = input('Введите рабочий телефон:')
        pers_phone = input('Введите личный телефон:')
        user = User(f_name, l_name, patronymic, org_name, work_phone, pers_phone)
        PB.add_user(user)

        choose = int(input('Выберите действие: \n\t1. Добавить еще одну запись \n\t2. Перейти в главное меню\n'))
        if choose == 2:
            break

if __name__ == '__main__':
    file_name = 'phonebook.txt'
    PB = PhoneBook(file_name=file_name)
    choose_action = int
    while choose_action != 5:
        print('Выберите действие: \n\t1. Показать все записи \n\t2. Найти запись '
              '\n\t3. Добавить запись \n\t4. Изменить запись \n\t5. Выход\n')
        try:
            choose_action = int(input())
        except ValueError:
            print('Введите число!')
        else:
            if choose_action == 1:
                show_records()

            elif choose_action == 2:
                search_record(PB)

            elif choose_action == 3:
                add_record()

            elif choose_action == 4:
                edit_record(PB)

            elif choose_action == 5:
                break


# # myanyo = User('Влад', 'Невгод', 'Юрьевич', 'БГУИР', '+375445453349', '-')
# # bim = User('Руслан', 'Муравейко', 'Олегович', 'БГУИР', '+375447209161', '-')
# # bin = User('Рус', 'Муравейко', 'Олегович', 'БГУИР', '+375447209161', '-')
# # myanyok = User('Влад', 'Муравейко', 'Олегович', 'БГУИР', '+375447209161', '-')
# # myanyoke = User('Влада', 'Муравейкофывфыв', 'Олеговичфывфы', 'БГУИРфывфыв', '+37544720916фывфыв1', '-фвыфыв')
# # myanyoke = User('Владааа', 'Вторая страница уже должна идти ёмаё', 'ДАда', 'Без шуток', '+37544720916фывфыв1', '-фвыфыв')
# pb = PhoneBook('phonebook.txt')
# # pb.add_user(myanyoke)
#
#
# # if pb.edit_record(myanyo, 'Влад', 'Невгод', 'Юргилевич', 'БГУИР', '+375445453349', '-') is False:
# #     print('гауняк, файл создай а потом изменяй что-то')
# # else:
# #     print('Вонь всё ок')
# page1 = pb.get_all_data(paginate=1)
# for user in page1:
#     for key, value in user.items():
#         print(f'{key} - {value}')
#     print()
