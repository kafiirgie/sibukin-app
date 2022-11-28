import sqlite3

class Model():
    def __init__(self):
        pass
    
    # Membuat tabel kegiatan dan tabel kategori pada file sibukin.db
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
                              FOREIGN KEY (id_kategori) REFERENCES kategori(id_kategori))""")
            self.c.execute("""CREATE TABLE IF NOT EXISTS kategori (
                              id_kategori integer,
                              nama_kategori text,
                              PRIMARY KEY (id_kategori))""")
        self.conn.close()

    # Menambahkan kegiatan baru ke dalam database
    def insert_kegiatan(self, kegiatan):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""INSERT INTO kegiatan VALUES (
                               '{kegiatan.id}',
                               '{kegiatan.nama}',
                               '{kegiatan.waktu}',
                               '{kegiatan.status}',
                               '{kegiatan.kategori}')""")
        self.conn.close()    

    # Menambahkan kategori baru ke dalam database
    def insert_kategori(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""INSERT INTO kategori VALUES (
                            '{kategori.id}',
                            '{kategori.nama}')""")
        self.conn.close()

    # Melakukan return semua data kegiatan dari database (kategori masih berupa id)
    def get_all_kegiatan(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kegiatan")
        return self.c.fetchall()

    # Melakukan return semua data kegiatan yang sudah mencakup nama kategori dari database
    def get_all_kegiatan_with_nama_kategori(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("""SELECT * FROM kegiatan
                          LEFT OUTER JOIN kategori
                          USING(id_kategori)""")
        return self.c.fetchall()
    
    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan waktu hari ini
    def get_kegiatan_filtered_today(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("""SELECT * FROM kegiatan
                          LEFT OUTER JOIN kategori
                          USING(id_kategori)
                          WHERE batas_waktu = Date('now')""")
        return self.c.fetchall()
    
    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan status tertentu
    def get_kegiatan_filtered_status(self, status):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT * FROM kegiatan
                           LEFT OUTER JOIN kategori
                           USING(id_kategori)
                           WHERE status = '{status}'""")
        return self.c.fetchall()
    
    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan kategori tertentu
    def get_kegiatan_filtered_kategori(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        print(kategori)
        self.c.execute(f"""SELECT * FROM kegiatan
                           LEFT OUTER JOIN kategori
                           USING(id_kategori)
                           WHERE nama_kategori = '{kategori}'""")
        return self.c.fetchall()
    
    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan status dan kategori tertentu
    def get_kegiatan_filtered_status_kategori(self, status, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT * FROM kegiatan
                           LEFT OUTER JOIN kategori
                           USING(id_kategori)
                           WHERE status = '{status}'
                           AND nama_kategori = '{kategori}'""")
        return self.c.fetchall()

    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan waktu hari ini dan status tertentu
    def get_kegiatan_filtered_status_today(self, status):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT * FROM kegiatan
                           LEFT OUTER JOIN kategori
                           USING(id_kategori)
                           WHERE batas_waktu = Date('now')
                           AND status = '{status}'""")
        return self.c.fetchall()

    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan waktu hari ini dan kategori tertentu
    def get_kegiatan_filtered_kategori_today(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT * FROM kegiatan
                           LEFT OUTER JOIN kategori
                           USING(id_kategori)
                           WHERE batas_waktu = Date('now')
                           AND nama_kategori = '{kategori}'""")
        return self.c.fetchall()
    
    # Melakukan return data kegiatan yang memenuhi kondisi filter berdasarkan waktu hari ini, status dan kategori tertentu
    def get_kegiatan_filtered_status_kategori_today(self, status, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT * FROM kegiatan
                           LEFT OUTER JOIN kategori
                           USING(id_kategori)
                           WHERE batas_waktu = Date('now')
                           AND status = '{status}'
                           AND nama_kategori = '{kategori}'""")
        return self.c.fetchall()

    # Melakukan return semua data kategori dari database
    def get_all_kategori(self):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM kategori")
        return self.c.fetchall()

    # Melakukan return data kegiatan berdasarkan input id_kegiatan
    def get_kegiatan_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT * FROM kegiatan
                           WHERE id_kegiatan = '{id}'""")
        return self.c.fetchone()

    # Melakukan return data kategori berdasarkan input id_kegiatan
    def get_kategori_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        self.c.execute(f"""SELECT nama_kategori FROM kategori
                           WHERE id_kategori = '{id}'""")
        return self.c.fetchone()

    # Mengubah status data kegiatan tertentu menjadi new_status
    def update_status(self, id, new_status):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""UPDATE kegiatan
                               SET status = '{new_status}'
                               WHERE id_kegiatan = '{id}'""")
        self.conn.close()

    # Menghapus data kegiatan tertentu dari database
    def delete_kegiatan(self, kegiatan):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""DELETE from kegiatan
                               WHERE id_kegiatan = '{kegiatan.id}'""")
        self.conn.close()
    
    # Menghapus data kegiatan tertentu dari database melalui id_kegiatan
    def delete_kegiatan_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""DELETE from kegiatan
                               WHERE id_kegiatan = '{id}'""")
        self.conn.close()
    
    # Menghapus data kategori tertentu dari database
    def delete_kategori(self, kategori):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""DELETE from kategori
                               WHERE id_kategori = '{kategori.id}'""")
        self.conn.close()
    
    # Menghapus data kategori tertentu dari database melalui id_kategori
    def delete_kategori_by_id(self, id):
        self.conn = sqlite3.connect('sibukin.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute(f"""DELETE from kategori
                               WHERE id_kategori = '{id}'""")
        self.conn.close()
