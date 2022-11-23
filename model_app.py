import sqlite3
from kegiatan import Kegiatan
from kategori import Kategori

class Model():
    def __init__(self):
        pass

    def create_table(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS kegiatan (
                        id_kegiatan integer,
                        nama_kegiatan text,
                        batas_waktu text,
                        status text,
                        id_kategori integer,
                        PRIMARY KEY (id_kegiatan),
                        FOREIGN KEY (id_kategori) REFERENCES kategori(id_kategori)
                        )"""
                    )
            self.c.execute("""CREATE TABLE IF NOT EXISTS kategori (
                        id_kategori integer,
                        nama_kategori text,
                        PRIMARY KEY (id_kategori)
                        )"""
                    )
        self.conn.close()

    def insert_kegiatan(self, kegiatan):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("""INSERT INTO kegiatan VALUES
                        (:id_kegiatan, :nama_kegiatan, :batas_waktu, :status, :id_kategori)""",
                        {'id_kegiatan': kegiatan.id, 'nama_kegiatan': kegiatan.nama, 'batas_waktu': kegiatan.waktu, 'status': kegiatan.status, 'id_kategori': kegiatan.kategori}
                    )
        self.conn.close()    

    def insert_kategori(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("""INSERT INTO kategori VALUES
                        (:id_kategori, :nama_kategori)""",
                        {'id_kategori': kategori.id, 'nama_kategori': kategori.nama}
                    )
        self.conn.close()

    def get_all_kegiatan(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan")
        return self.c.fetchall()

    def get_all_kegiatan_with_nama_kategori(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori)")
        return self.c.fetchall()
    
    def get_kegiatan_filtered_today(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE batas_waktu = Date('now')")
        return self.c.fetchall()
    
    def get_kegiatan_filtered_status(self, status):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        # self.c.execute(f"SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE status = '{status}'")
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE status = :status", {'status': status})
        return self.c.fetchall()
    
    def get_kegiatan_filtered_kategori(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        print(kategori)
        self.c.execute(f"SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE nama_kategori = '{kategori}'")
        # self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE nama_kategori = :nama_kategori", {'nama_kategori':kategori})
        return self.c.fetchall()
    
    def get_kegiatan_filtered_status_kategori(self, status, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE status = :status AND nama_kategori = :nama_kategori", {'status':status,'nama_kategori':kategori})
        return self.c.fetchall()

    def get_kegiatan_filtered_status_today(self, status):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE batas_waktu = Date('now') AND status = :status", {'status':status})
        return self.c.fetchall()

    def get_kegiatan_filtered_kategori_today(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE batas_waktu = Date('now') nama_kategori = :nama_kategori", {'nama_kategori':kategori})
        return self.c.fetchall()
    
    def get_kegiatan_filtered_status_kategori_today(self, status, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan INNER JOIN kategori USING(id_kategori) WHERE batas_waktu = Date('now') AND status = :status AND nama_kategori = :nama_kategori", {'status':status,'nama_kategori':kategori})
        return self.c.fetchall()

    def get_all_kategori(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kategori")
        return self.c.fetchall()

    def get_kegiatan_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan WHERE id_kegiatan=:id_kegiatan", {'id_kegiatan': id})
        return self.c.fetchone()

    def get_kategori_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT nama_kategori FROM kategori WHERE id_kategori=:id_kategori", {'id_kategori': id})
        return self.c.fetchone()

    def update_status(self, id, new_status):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("""UPDATE kegiatan SET status = :status
                        WHERE id_kegiatan = :id_kegiatan""",
                    {'id_kegiatan': id, 'status': new_status})
        self.conn.close()

    def remove_kegiatan(self, kegiatan):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("DELETE from kegiatan WHERE id_kegiatan = :id_kegiatan",
                    {'id_kegiatan': kegiatan.id})
        self.conn.close()
    
    def remove_kegiatan_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("DELETE from kegiatan WHERE id_kegiatan = :id_kegiatan",
                    {'id_kegiatan': id})
        self.conn.close()
