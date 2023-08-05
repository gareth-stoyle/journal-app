import bcrypt
import sqlite3

class DB:
    def register(self, username, password):
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            self.conn = sqlite3.connect('journal.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.IntegrityError:
            return "Username already exists. Please choose a different one."
        except Exception as e:
            return e

    def login(self, username, password):
        try:
            self.conn = sqlite3.connect('journal.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = self.cursor.fetchone()
            if result:
                hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return True
                else:
                    return False
            else:
                print("User not found.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def submit_journal_entry(self, entry, datestamp):
        try:
            self.conn = sqlite3.connect('journal.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('INSERT INTO journal_entries (date, entry) VALUES(?, ?);', (datestamp, entry))
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)
