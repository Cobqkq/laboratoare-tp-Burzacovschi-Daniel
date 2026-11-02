# B5. Ascunzi un mesaj prin LSB

def b5_ascunde():
    from PIL import Image
    img = Image.open("probe/foto.jpg").convert("RGB")
    px = list(img.getdata())
    mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj)
    px_nou = []
    i = 0
    for (r, g, b) in px:
        if i < len(biti):
            r = (r & ~1) | int(biti[i]); i += 1
        if i < len(biti):
            g = (g & ~1) | int(biti[i]); i += 1
        if i < len(biti):
            b = (b & ~1) | int(biti[i]); i += 1
        px_nou.append((r, g, b))
    img.putdata(px_nou)
    img.save("stego.png")

# B6. Dezvalui mesajul inapoi

def b6_dezvaluie():
    from PIL import Image
    px = list(Image.open("stego.png").convert("RGB").getdata())
    biti = ""
    for (r, g, b) in px:
        biti += str(r & 1) + str(g & 1) + str(b & 1)
    octeti = []
    for i in range(0, len(biti), 8):
        octet = biti[i:i+8]
        if len(octet) < 8:
            break
        valoare = int(octet, 2)
        if valoare == 0:
            break
        octeti.append(valoare)
    print("".join(chr(o) for o in octeti))

def main():
    b5_ascunde()      # dupa ce scrii B5, aici se creeaza stego.png
    b6_dezvaluie()    # are nevoie de stego.png, deci ruleaza dupa B5

if __name__ == "__main__":
    main()
