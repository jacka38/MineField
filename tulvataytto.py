def tulvataytto(arr, arr2, x, y):
    """
    -ruutu, jossa miinat ja numerot on "arr" 
    -Piirretty peli-ikkuna on "arr2"

    Tulvatäyttö luokka, joka avaa tyhjät ruudut ja näyttää numeroruudut.
    """
    if (arr[y][x] == "x"):
        return

    luettelo = []
    luettelo.append([y, x])

    # Muuttujat selitetty selvyyden vuoksi
    yla = (y - 1, x)
    ala = (y + 1, x)
    vasen = (y, x - 1)
    oikea = (y, x + 1)

    while luettelo:
        arvo = luettelo.pop()

        y_1, x_1 = arvo

        for i in range(y_1 - 1, y_1 + 2):
            for j in range(x_1 - 1, x_1 + 2):
                if 0 <= i < len(arr) and 0 <= j < len(arr[0]) and arr[i][j] != "x":
                    if arr[i][j] == " ":
                        arr[i][j] = "0"
                        arr2[i][j] = "0"
                        luettelo.append([i, j])
                    else:
                        arr2[i][j] = arr[i][j]
