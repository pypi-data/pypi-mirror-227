import requests
from bs4 import BeautifulSoup


def ekstrasi_data():
    """

    Tanggal: 15 Agustus 2023, 16:29:17 WIB
    Magnitudo: 2.6 skala richter
    Kedalaman: 6 km
    Lokasi: ls=6.82 LS - ls=107.13 BT
    Pusat Gempa : Pusat gempa berada di darat 1 km barat laut Kab. Cianjur
    Dirasakan : Dirasakan (Skala MMI): II Cugenang, II Kota Cianjur, II Karangtengah, II Warungkondang
    :return:
    """

    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        hasil = soup.find('span', {'class': 'waktu'})
        hasil = hasil.text.split(', ')
        tanggal = hasil[0]
        waktu = hasil[1]

        hasil = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        hasil = hasil.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        for res in hasil:
            print(i, res)
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan

        return hasil
    else:
        return None


def tampilkan_data(hasil):
    if hasil is None:
        print('Tidak bisa Menemukan data gempa terkini')
        return
    print('Gempa Terakhir Berdasarkan BMKG')
    print(f"Tanggal: {hasil['tanggal']}")
    print(f"Waktu: {hasil['waktu']}")
    print(f"Magnitudo: {hasil['magnitudo']}")
    print(f"kedalaman: {hasil['kedalaman']}")
    print(f"koordinat: LS={hasil['koordinat']['ls']}, BT={hasil['koordinat']['bt']}")
    print(f"lokasi: {hasil['lokasi']}")
    print(f"dirasakan: {hasil['dirasakan']}")


if __name__ == '__main__':
    result = data_gempa.ekstrasi_data()
    data_gempa.tampilkan_data(result)
