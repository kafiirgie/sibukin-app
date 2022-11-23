from kegiatan import Kegiatan
from kategori import Kategori
from model_app import Model
from view_app import App

def test_insert_kategori():
    model = Model()

    list_kategori = model.get_all_kategori()
    found = False
    new_kategori = Kategori(998, 'ASDFGHJKL;')
    for data in list_kategori:
        if data[0] == 998:
            found = True
            break
    if not(found):
        model.insert_kategori(new_kategori)

    list_kategori = model.get_all_kategori()
    for data in list_kategori:
        if data[0] == 998:
            kategori = data
    
    assert kategori[0] == new_kategori.id and kategori[1] == new_kategori.nama

def test_insert_kegiatan():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 998)
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
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 998)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    if not(found):
        model.insert_kegiatan(new_kegiatan)
    
    model.remove_kegiatan(new_kegiatan)
    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 998)
    for data in list_kegiatan:
        if data[0] == 99:
            found = True
            break
    assert not found

def test_tandai_selesai_kegiatan():
    model = Model()

    list_kegiatan = model.get_all_kegiatan()
    found = False
    new_kegiatan = Kegiatan(99, 'Dummy Kegiatan', '2025-12-12', 'On Going', 998)
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