# B1. Magic bytes: tipul real, nu extensia

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

# B2. strings: textul citibil dintr-un binar

def b2_strings():
    import re
    date = open("probe/ascuns.png", "rb").read()
    for m in re.findall(rb"[ -~]{4,}", date):
        print(m.decode())

# B3. Metadate EXIF si GPS din poza

def b3_exif():
    from PIL import Image
    from PIL.ExifTags import TAGS
    exif = Image.open("probe/foto.jpg")._getexif() or {}
    for id, val in exif.items():
        print(TAGS.get(id, id), "=", val)
    if 34853 in exif:
        gps = exif[34853]
        lat = float(gps[2][0] + gps[2][1]/60 + gps[2][2]/3600), gps[1]
        lon = float(gps[4][0] + gps[4][1]/60 + gps[4][2]/3600), gps[3]
        print("GPS:", lat, lon)

# B4. File carving: scoti fisierul ascuns

def b4_carving():
    import zipfile
    date = open("probe/ascuns.png", "rb").read()
    i = date.find(b"PK\x03\x04")
    if i != -1:
        open("gasit.zip","wb").write(date[i:])
        print("arhiva extrasa de la octetul", i)
        with zipfile.ZipFile("gasit.zip") as z:
            z.extractall("gasit")

def main():
    print(tip_real("probe/foto.jpg"))
    b2_strings()
    b3_exif()
    b4_carving()

if __name__ == "__main__":
    main()
