from kegiatan import Kegiatan
from kategori import Kategori
from model_app import Model
from datetime import datetime
import pytest
    
# Unit testing untuk fitur tambah kategori
def test_insert_kategori():
    # SETUP PRE CONDITION
    #### Menghapus kategori dengan id 999 jika sudah ada dalam database
    model = Model()
    list_kategori = model.get_all_kategori()
    for data in list_kategori:
        if data[0] == 999:
            model.delete_kategori_by_id(data[0])
            break
    
    # IMPLEMENTATION
    #### Menambahkan kategori
    new_kategori = Kategori(999, 'Dummy Kategori')
    model.insert_kategori(new_kategori)

    # CHECK POST CONDITION
    #### Memeriksa apakah data kategori yang dimasukan ada dalam database
    kategori = ('None', 'None')
    list_kategori = model.get_all_kategori()
    for data in list_kategori:
        if data[0] == 999:
            kategori = data
    
    assert kategori[0] == new_kategori.id and kategori[1] == new_kategori.nama

# Unit testing untuk fitur tambah kegiatan
def test_insert_kegiatan():
    # SETUP PRE CONDITION
    #### Menghapus kegiatan dengan id 999 jika sudah ada dalam database
    model = Model()
    list_kegiatan = model.get_all_kegiatan()
    for data in list_kegiatan:
        if data[0] == 999:
            model.delete_kegiatan_by_id(999)
            break
    
    # IMPLEMENTATION
    #### Menambahkan kegiatan
    new_kegiatan = Kegiatan(999, 'Dummy Kegiatan', '2025-12-12', 'On Going', 999)
    model.insert_kegiatan(new_kegiatan)

    # CHECK POST CONDITION
    #### Memeriksa apakah data kegiatan yang dimasukan ada dalam database
    kegiatan = ('None','None','None','None','None')
    list_kegiatan = model.get_all_kegiatan()
    for data in list_kegiatan:
        if data[0] == 999:
            kegiatan = data
    
    assert kegiatan[0] == new_kegiatan.id and kegiatan[1] == new_kegiatan.nama and kegiatan[2] == new_kegiatan.waktu and kegiatan[4] == new_kegiatan.kategori

# Unit testing untuk fitur tandai selesai kegiatan (ubah status)
def test_tandai_selesai_kegiatan():
    # SETUP PRE CONDITION
    #### Memastikan kegiatan dengan id 999 ada dalam database
    model = Model()
    list_kegiatan = model.get_all_kegiatan()
    new_kegiatan = Kegiatan(999, 'Dummy Kegiatan', '2025-12-12', 'On Going', 999)
    for data in list_kegiatan:
        if data[0] == 999:
            model.delete_kegiatan_by_id(999)
            break
    model.insert_kegiatan(new_kegiatan)
    
    # IMPLEMENTATION
    #### Mengubah status kegiatan dengan id 999 dari 'On Going' menjadi 'Done'
    model.update_status(999, 'Done')
    
    # CHECK POST CONDITION
    #### Memeriksa apakah kegiatan dengan id 999 memiliki status 'Done'
    kegiatan = ('None','None','None','None','None')
    list_kegiatan = model.get_all_kegiatan()
    for data in list_kegiatan:
        if data[0] == 999:
            kegiatan = data
    
    assert kegiatan[0] == new_kegiatan.id and kegiatan[3] == 'Done'

# Unit testing untuk fitur hapus kegiatan
def test_delete_kegiatan():
    # SETUP PRE CONDITION
    #### Memastikan kegiatan dengan id 999 ada dalam database
    model = Model()
    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(999, 'Dummy Kegiatan', '2025-12-12', 'On Going', 999)
    for data in list_kegiatan:
        if data[0] == 999:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    # IMPLEMENTATION
    #### Menghapus data kegiatan dengan id 999 dari database
    model.delete_kegiatan(new_kegiatan)

    # CHECK POST CONDITION
    #### Memeriksa apakah data kegiatan yang dimasukan tidak ada dalam database
    list_kegiatan = model.get_all_kegiatan()
    found = False
    for data in list_kegiatan:
        if data[0] == 999:
            found = True
            break
    
    assert not found

# Unit testing untuk fitur filter berdasarkan waktu
def test_filter_kegiatan_today():
    # SETUP PRE CONDITION
    #### Memastikan kegiatan dengan id 999 dan batas_waktu hari ini ada dalam database
    model = Model()
    list_kegiatan = model.get_all_kegiatan()
    date_now_string = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'
    new_kegiatan = Kegiatan(999, 'Dummy Kegiatan', date_now_string, 'On Going', 999)
    for data in list_kegiatan:
        if data[0] == 999:
            model.delete_kegiatan_by_id(999)
            break
    model.insert_kegiatan(new_kegiatan)
    
    # IMPLEMENTATION
    #### Menyimpan kegiatan yang sudah difilter berdasarkan waktu hari ini
    list_kegiatan = model.get_kegiatan_filtered_today()
    
    # CHECK POST CONDITION
    #### Memeriksa apakah ada data kegiatan yang tidak memenuhi syarat filter
    check_is_today_date = True
    for data in list_kegiatan:
        if (data[2] != date_now_string):
            check_is_today_date = False
    
    assert check_is_today_date

# Unit testing untuk fitur filter berdasarkan status
def test_filter_kegiatan_status():
    # SETUP PRE CONDITION
    #### Memastikan kegiatan dengan id 999 dan status 'On Going' ada dalam database
    model = Model()
    list_kegiatan = model.get_all_kegiatan()
    new_kegiatan = Kegiatan(999, 'Dummy Kegiatan', '2025-12-12', 'On Going', 999)
    for data in list_kegiatan:
        if data[0] == 999:
            model.delete_kegiatan_by_id(999)
            break
    model.insert_kegiatan(new_kegiatan)
    
    # IMPLEMENTATION
    #### Menyimpan kegiatan yang sudah difilter berdasarkan status 'On Going'
    list_kegiatan = model.get_kegiatan_filtered_status('On Going')
    
    # CHECK POST CONDITION
    #### Memeriksa apakah ada data kegiatan yang tidak memenuhi syarat filter
    check_is_status_ongoing = True
    for data in list_kegiatan:
        if (data[3] != 'On Going'):
            check_is_status_ongoing = False
    
    assert check_is_status_ongoing

# Unit testing untuk fitur filter berdasarkan kategori
def test_filter_kegiatan_kategori():
    # SETUP PRE CONDITION
    #### Memastikan kegiatan dengan id 999 dan kategori 'Dummy Kategori' ada dalam database
    model = Model()
    list_kegiatan = model.get_all_kegiatan()
    new_kegiatan = Kegiatan(999, 'Dummy Kegiatan', '2025-12-12', 'On Going', 999)
    for data in list_kegiatan:
        if data[0] == 999:
            model.delete_kegiatan_by_id(999)
            break
    model.insert_kegiatan(new_kegiatan)
    
    # IMPLEMENTATION
    #### Menyimpan kegiatan yang sudah difilter berdasarkan kategori 'Dummy Kategori'
    list_kegiatan = model.get_kegiatan_filtered_kategori('Dummy Kategori')
    
    # CHECK POST CONDITION
    #### Memeriksa apakah ada data kegiatan yang tidak memenuhi syarat filter
    check_is_cateogry_dummy = True
    for data in list_kegiatan:
        if (data[5] != 'Dummy Kategori'):
            check_is_cateogry_dummy = False
    assert check_is_cateogry_dummy

