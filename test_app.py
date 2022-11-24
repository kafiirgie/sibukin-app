from kegiatan import Kegiatan
from kategori import Kategori
from model_app import Model
from view_app import App
from datetime import datetime

def test_insert_kategori():
    model = Model()

    list_kategori = model.get_all_kategori()
    found = False
    new_kategori = Kategori(202, 'Dummy Kategori')
    for data in list_kategori:
        if data[0] == 202:
            found = True
            break
    if not(found):
        model.insert_kategori(new_kategori)

    list_kategori = model.get_all_kategori()
    for data in list_kategori:
        if data[0] == 202:
            kategori = data
    
    assert kategori[0] == new_kategori.id and kategori[1] == new_kategori.nama

def test_insert_kegiatan():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)

    list_kegiatan = model.get_all_kegiatan()
    for data in list_kegiatan:
        if data[0] == 99:
            kegiatan = data
    # status tidak diperiksa karena dapat berubah2
    assert kegiatan[0] == new_kegiatan.id and kegiatan[1] == new_kegiatan.nama and kegiatan[2] == new_kegiatan.waktu and kegiatan[4] == new_kegiatan.kategori

def test_delete_kegiatan():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    model.remove_kegiatan(new_kegiatan)
    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    assert not found

def test_tandai_selesai_kegiatan():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    model.update_status(99, 'Done')
    list_kegiatan = model.get_all_kegiatan()
    for data in list_kegiatan:
        if data[0] == 99:
            kegiatan = data
    
    assert kegiatan[0] == new_kegiatan.id and kegiatan[3] == 'Done'

def test_filter_kegiatan_today():
    model = Model()
    date_now_string = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(100, 'Dummy Kegiatan', date_now_string, 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 100:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    list_kegiatan = model.get_kegiatan_filtered_today()
    value = True
    if len(list_kegiatan) != 0:
        for data in list_kegiatan:
            if data[2] != date_now_string:
                value = False
    assert value

def test_filter_kegiatan_status():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    list_kegiatan = model.get_kegiatan_filtered_status('On Going')
    value = True
    if len(list_kegiatan) != 0:
        for data in list_kegiatan:
            if data[3] != 'On Going':
                value = False
    assert value

def test_filter_kegiatan_kategori():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 202)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    list_kegiatan = model.get_kegiatan_filtered_kategori('Dummy Kategori')
    print(list_kegiatan)
    value = True
    if len(list_kegiatan) != 0:
        for data in list_kegiatan:
            if data[5] != 'Dummy Kategori':
                value = False
    assert value
