import functools

listas = [
    {"vardas": "martynas"},
    {"vardas": "jonas"}
]


b = {"martynas": "jason", "jonas": "jablonskis"}
def funkcija(zodynas, b):



    id = zodynas["vardas"]
    temp_file = b[id]
    zodynas["pavarde"] = temp_file
    return zodynas


naujas_zodynas = map(functools.partial(funkcija, b=b), listas)
print(list(naujas_zodynas))
a = 1