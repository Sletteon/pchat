pchat
===================
 Egy nagyon egyszerű chatprogram működő kliens- és szerver szoftverrel.<hr>
<h3>Szerver:</h3>
<p>Indításkor egy socketet hoz létre a megadott porttal, valamint a szerver IP-címével. Mivel lokális IP-t kér le, ezért erre a címre érdemes IP-forwardelni, ha nem lokális hálózaton keresztül szeretnénk kapcsolatot létesíteni. </p>
<p>Ha valaki csatlakozik a szerverre, a megfelelő paraméterek mellett, akkor egy menő üdvölő üzenet fogadja a felhasználót.</p>
<h3>Kliens</h3>
<p>Indításnál csak a szerverhez csatlakozik, ezt a szerver üdvözlőüzenete jelzi. Szervernél megjelenik, hogy a felhasználó bekapcsolódott, amely ezt mindenkinek tudára adja.</p>
<p>Egy kliens lekapcsolódása esetén mindenkinek üzen, mielött eltávolítaná az illetőt az online lévő felhasználók listájából. </p>
<p>Felhasználónevek helyett IP-címek vannak, hogy gördülékenyebb legyen a kommunikáció folyamata. :P</p>
