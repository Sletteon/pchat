pchat
===================
 Egy nagyon egyszerű csetprogram működő kliens- és szerver szoftver.<hr>
<h3>Szerver:</h3>
<p>Indításkor egy socketet hoz létre a megadott porttal, valamint a szerver IP-címével. Ha hálózatok között (WAN) használjuk, akkor azt az IP-címet adjuk meg, amelyre IP-forwardeltünk. </p>
<p>Ha valaki csatlakozik a szerverre, a megfelelő paraméterek mellett, akkor egy menő üdvölő üzenet fogadja a felhasználót.</p>
<b>Használat:</b>

    python server.py <IP-cím> <port száma>

<h3>Kliens</h3>
<p>Indításnál csak a szerverhez csatlakozik, ezt a szerver üdvözlőüzenete jelzi. Szervernél megjelenik, hogy a felhasználó bekapcsolódott, amely ezt mindenkinek tudára adja.</p>
<p>Felhasználónevek helyett IP-címek vannak, hogy gördülékenyebb legyen a kommunikáció folyamata. :P</p>
<b>Használat:</b>

    python client.py <szerver IP-cím> <szerver port>
