import psycopg2
from psycopg2.extensions import AsIs
import configparser
from random import randint


class UserRecords:
    def __init__(self, host_, port_, dbname_, user_, password_):
        self.connection = psycopg2.connect(host=host_, port=port_, dbname=dbname_, user=user_, password=password_)

    def create_structure(self):  # Create DB structure. Warning, all existing data will be removed!
        with self.connection.cursor() as my_cur:
            my_cur.execute('DROP TABLE IF EXISTS phones;')
            my_cur.execute('DROP TABLE IF EXISTS emails;')
            my_cur.execute('DROP TABLE IF EXISTS users;')
            self.connection.commit()
            my_cur.execute('''
            CREATE TABLE IF NOT EXISTS users ( 
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            surname VARCHAR(20)
            );''')
            my_cur.execute('''
            CREATE TABLE IF NOT EXISTS phones (
            phone_id SERIAL PRIMARY KEY,
            phone_no VARCHAR(20),
            user_id int,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
            );''')
            my_cur.execute('''
            CREATE TABLE IF NOT EXISTS emails (
            email_id SERIAL PRIMARY KEY,
            email VARCHAR(50),
            user_id int,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
            );''')
            self.connection.commit()

    def load_data(self, table_name, file_name):  # Read data from CSV files into clean tables.
        with self.connection.cursor() as my_cur:
            my_cur.execute("""
            COPY %s FROM %s DELIMITER ';' CSV HEADER;
            """, (AsIs(table_name), file_name))
            self.connection.commit()

    def input_record(self):  # User input. Returns entered user_id if correct, -1 otherwise.
        user_id = input('Enter UserID: ')
        if not user_id.isdecimal():
            print('Wrong ID, only decimal numbers allowed.')
            return -1
        user_id = int(user_id)
        with self.connection.cursor() as my_cur:
            my_cur.execute("SELECT COUNT(user_id) FROM users WHERE user_id = %s;", (user_id,))
            records_ = my_cur.fetchone()[0]
            if records_ == 0:
                print(f'UserID {user_id} not found.')
                return -1
        return user_id

    def create(self, user_details):  # Create new record
        with self.connection.cursor() as my_cur:
            my_cur.execute("SELECT max(user_id) FROM users;")
            user_id = my_cur.fetchone()
            user_id = user_id[0]
            user_id += 1
            my_cur.execute("SELECT max(email_id) FROM emails;")
            email_id = my_cur.fetchone()
            email_id = email_id[0]
            email_id += 1
            my_cur.execute("SELECT max(phone_id) FROM phones;")
            phone_id = my_cur.fetchone()
            phone_id = phone_id[0]
            phone_id += 1
            my_cur.execute("""
            INSERT INTO %s (user_id, name, surname) VALUES (%s, %s, %s);
            """, (AsIs('users'), user_id, user_details[0], user_details[1]))
            self.connection.commit()
            my_cur.execute("""
            INSERT INTO %s (email_id, email, user_id) VALUES (%s, %s, %s);
            """, (AsIs('emails'), email_id, user_details[2], user_id))
            self.connection.commit()
            for phone_no in user_details[3]:
                my_cur.execute("""
                INSERT INTO %s (phone_id, phone_no, user_id) VALUES (%s, %s, %s);
                """, (AsIs('phones'), phone_id, phone_no, user_id))
                phone_id += 1
            self.connection.commit()
            print(f'New record added:')
            self.print_user_details(user_id)

    def print_user_details(self, user_id):  # Print all user data using ID
        with self.connection.cursor() as my_cur:
            my_cur.execute("""
            SELECT name, surname FROM users WHERE user_id = %s;
            """, (user_id,))
            record_ = my_cur.fetchone()
            print(f'{user_id}. {record_[0]} {record_[1]}', end=' ')
            my_cur.execute("""
            SELECT email FROM emails
            WHERE user_id = %s;""", (user_id,))
            emails_ = my_cur.fetchall()
            print(f'E-mails:', end=' ')
            [print(f'{email_[0]}', end=' ') for email_ in emails_]
            print(f'Phones:', end=' ')
            my_cur.execute("""
            SELECT phone_no FROM phones
            WHERE user_id = %s;""", (user_id,))
            phones_ = my_cur.fetchall()
            [print(phone_[0], end=' ') for phone_ in phones_]
            print(f'\n', end='')

    def get_list(self):  # Get all users data
        with self.connection.cursor() as my_cur:
            my_cur.execute("""
            SELECT user_id FROM users;
            """)
            records_ = my_cur.fetchall()
            [self.print_user_details(record_[0]) for record_ in records_]

    def add_phone(self, user_id):  # Add new phone number to the existing user
        # user_id = self.input_record()
        if user_id == -1:
            return
        with self.connection.cursor() as my_cur:
            phone_ = randint(1000000, 9999999)
            my_cur.execute("SELECT max(phone_id) FROM phones;")
            phone_id = my_cur.fetchone()
            phone_id = phone_id[0]
            phone_id += 1
            my_cur.execute("""INSERT INTO phones (phone_id, phone_no, user_id)
            VALUES (%s, %s, %s);""", (phone_id, phone_, user_id))
            self.connection.commit()
            print(f'Phone number {phone_} was added to UserID {user_id}')

    def change(self, user_id):  # Update existing record. New data will be generated automatically.
        # user_id = self.input_record()
        if user_id == -1:
            return
        with self.connection.cursor() as my_cur:
            print('Choose info to change:\n1. Name, surname and e-mail\n2. Phone\n')
            choice_ = input('Enter option: ')
            user_details = get_new_identity()
            if choice_ == '1':
                my_cur.execute("""
                UPDATE users SET name = %s, surname = %s WHERE user_id = %s;
                """, (user_details[0], user_details[1], user_id))
                my_cur.execute("""
                UPDATE emails SET email = %s WHERE user_id = %s;
                """, (user_details[2], user_id))
            elif choice_ == '2':
                my_cur.execute("SELECT count(phone_no) FROM phones WHERE user_id = %s;", (user_id,))
                phones_ = my_cur.fetchone()[0]
                if phones_ != 0:
                    my_cur.execute("SELECT phone_id FROM phones WHERE user_id = %s;", (user_id,))
                    phone_ids_ = my_cur.fetchall()
                    phone_ids_ = [(phone_id_[0]) for phone_id_ in phone_ids_]
                    user_details[3] = []
                    for index, phone_id_ in enumerate(phone_ids_):
                        user_details[3].append(randint(1000000, 9999999))
                        my_cur.execute("UPDATE phones SET phone_no = %s WHERE phone_id = %s;",
                       (user_details[3][index], phone_id_))
            else:
                print('Wrong input.')
                return
            self.connection.commit()
            print('Record updated.')
            self.print_user_details(user_id)

    def delete_phone(self, user_id):  # Delete existing phone number
        # user_id = self.input_record()
        if user_id == -1:
            return
        with self.connection.cursor() as my_cur:
            my_cur.execute('SELECT COUNT(phone_no) FROM phones WHERE user_id = %s;', (user_id,))
            phones_ = my_cur.fetchone()[0]
            if phones_ == 0:
                print(f'UserID {user_id} has no phone numbers.')
                return
            my_cur.execute('SELECT phone_no FROM phones WHERE user_id = %s', (user_id,))
            phones_ = my_cur.fetchall()
            phones_ = [phone_[0] for phone_ in phones_]
            [print(f'{index}. {phone_}') for index, phone_ in enumerate(phones_)]
            phones_q_ = len(phones_)
            print(f'{phones_q_}. All')
            choice_ = input('Enter phone you wish to delete: ')
            if not choice_.isdecimal():
                print('Wrong input')
                return
            choice_ = int(choice_)
            if choice_ > phones_q_:
                print('Wrong input')
                return
            elif choice_ == phones_q_:
                my_cur.execute('DELETE FROM phones WHERE user_id = %s;', (user_id,))
                print(f'All phones from UserID {user_id} deleted.')
                self.connection.commit()
                return
            else:
                my_cur.execute('DELETE FROM phones WHERE user_id = %s AND phone_no = %s;', (user_id, phones_[choice_]))
                self.connection.commit()
                print(f'Phone {phones_[choice_]} from UserID {user_id} deleted.')

    def delete(self):  # Delete existing record
        with self.connection.cursor() as my_cur:
            my_cur.execute('SELECT user_id, name, surname FROM users;')
            records_ = my_cur.fetchall()
            [print(f'{record_[0]}. {record_[1]} {record_[2]}') for record_ in records_]
            user_id = self.input_record()
            if user_id == -1:
                return
            my_cur.execute('DELETE FROM phones WHERE user_id = %s;', (user_id,))
            my_cur.execute('DELETE FROM emails WHERE user_id = %s;', (user_id,))
            my_cur.execute('DELETE FROM users WHERE user_id = %s;', (user_id,))
            self.connection.commit()
            print(f'Record UserID {user_id} was deleted.')

    def find(self):  # Find existing user by parameters
        with self.connection.cursor() as my_cur:
            print('Search by:\n1. Name\n2. Surname\n3. E-mail\n4. Phone\n')
            choice_ = input('Enter option: ')
            if choice_ == '1':
                choice_ = input('Enter name: ')
                my_cur.execute('''SELECT COUNT(name), user_id FROM users WHERE name = %s
                               GROUP BY user_id;''', (choice_,))
                user_details_ = my_cur.fetchone()
                if not user_details_:
                    print(f'User {choice_} not found.')
                    return
                self.print_user_details(user_details_[1])
            elif choice_ == '2':
                choice_ = input('Enter surname: ')
                my_cur.execute('''SELECT COUNT(name), user_id FROM users WHERE surname = %s
                GROUP BY user_id;''', (choice_,))
                user_details_ = my_cur.fetchone()
                if not user_details_:
                    print(f'User {choice_} not found.')
                    return
                self.print_user_details(user_details_[1])
            elif choice_ == '3':
                choice_ = input('Enter e-mail: ')
                my_cur.execute('''SELECT COUNT(email), user_id FROM emails WHERE email = %s
                               GROUP BY user_id;''', (choice_,))
                user_details_ = my_cur.fetchone()
                if not user_details_:
                    print(f'User with e-mail {choice_} not found.')
                    return
                self.print_user_details(user_details_[1])
            elif choice_ == '4':
                choice_ = input('Enter phone: ')
                my_cur.execute('''SELECT COUNT(phone_no), user_id FROM phones WHERE phone_no = %s
                               GROUP BY user_id;''', (choice_,))
                user_details_ = my_cur.fetchone()
                if not user_details_:
                    print(f'User with phone number {choice_} not found.')
                    return
                self.print_user_details(user_details_[1])
            else:
                print('Wrong input.')
            return


def read_config(path, section, parameter):  # Reading configs
    config = configparser.ConfigParser()
    config.read(path)
    c_value = config.get(section, parameter)
    return c_value


def get_new_identity():  # Generate user data
    names = ['John', 'Peter', 'Tanya', 'Elena', 'Bill', 'Phil', 'Andrew', 'Alex', 'Joanna', 'Ivanna', 'Iren',
             'Sam', 'Bruce', 'Kylie', 'Daniel', 'Linda', 'Mary', 'Chris', 'Christina', 'Penny']
    name_ = names[randint(0, len(names) - 1)]
    surnames = ['Johnson', 'Curtis', 'Willis', 'Smith', 'Ripley', 'Morgan', 'Jefferson', 'McCallan', 'Andersson',
                'Peterson', 'Jackson', 'Jones', 'Sanders', 'Nixon', 'Callahan', 'Richards', 'Newman', 'Hatfield',
                'Newman', 'Burton']
    surname_ = surnames[randint(0, len(surnames) - 1)]

    phone_ = [randint(1000000, 9999999) for index in range(0, randint(0, 2))]
    mail_ = f'{name_}.{surname_}@fakeidentity.com'
    return [name_, surname_, mail_, phone_]


if __name__ != '__main__':
    exit()
host = read_config('config.ini', 'Main', 'IP')
port = read_config('config.ini', 'Main', 'Port')
db_name = read_config('config.ini', 'Credentials', 'DBName')
user_name = read_config('config.ini', 'Credentials', 'UserName')
password = read_config('config.ini', 'Credentials', 'Password')
path_to_csv = read_config('config.ini', 'Main', 'DataPath')

my_record = UserRecords(host, port, db_name, user_name, password)
my_record.create_structure()
my_record.load_data('users', f'{path_to_csv}users.csv')
my_record.load_data('emails', f'{path_to_csv}emails.csv')
my_record.load_data('phones', f'{path_to_csv}phones.csv')

while True:
    print('-' * 20)
    print('1. Add record\n2. Add phone number\n3. Change record')
    print('4. Delete phone\n5. Delete record\n6. Find record\n7. List records\n0. Exit')
    print('-' * 20)
    choice = input('Enter option: ')
    if choice == '0':
        print('Goodbye!')
        my_record.connection.close()
        exit()
    elif choice == '1':
        my_record.create(get_new_identity())
    elif choice == '2':
        my_record.add_phone(my_record.input_record())
    elif choice == '3':
        my_record.change(my_record.input_record())
    elif choice == '4':
        my_record.delete_phone(my_record.input_record())
    elif choice == '5':
        my_record.delete()
    elif choice == '6':
        my_record.find()
    elif choice == '7':
        my_record.get_list()