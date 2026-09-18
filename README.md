# Drone Mission Algorithm

İki drone'un dikdörtgen bir alanı paylaşarak **"çim biçme" (lawnmower / boustrophedon) deseniyle** taramasını sağlayan bir görev planlama projesi. Alan ortadan ikiye bölünür; her drone kendi yarısını zikzak çizerek tarar, sonra alanın merkezine gidip başlangıç noktasına döner (RTL).

Proje [DroneKit-Python](https://github.com/dronekit/dronekit-python) ve [pymavlink](https://github.com/ArduPilot/pymavlink) kullanır. ArduPilot SITL (simülasyon) ortamında çalışacak şekilde yazılmıştır.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| [algorithm.py](algorithm.py) | `algorithm1()`: dört köşe noktasından tarama rotasının waypoint listesini üretir. |
| [functions.py](functions.py) | `haversine()`: iki enlem/boylam çifti arasındaki mesafeyi **km** cinsinden hesaplar. |
| [missionForDrone1.py](missionForDrone1.py) | 1. drone: `127.0.0.1:14550` portuna bağlanır, **7 m** irtifada alanın alt yarısını tarar. |
| [missionForDrone2.py](missionForDrone2.py) | 2. drone: `127.0.0.1:14560` portuna bağlanır, **11 m** irtifada alanın üst yarısını tarar. |

## Algoritma

### Köşe noktaları

`algorithm1(a, b, c, d)` dikdörtgenin dört köşesini alır:

- **a**: drone'un başlangıç köşesi
- **b**: a'ya **komşu** köşe; tarama geçişleri a–b doğrultusunda yapılır (b, a'nın çaprazındaki köşe olamaz)
- **c**: a'ya komşu diğer köşe
- **d**: a'nın çaprazındaki köşe

```
   d ─────────────────── c
   │                     │
   │      Drone 2        │   ← 11 m
   │   (d–c arası, güneye)│
 e'│─ ─ ─ ─ ─ ⊕ ─ ─ ─ ─ ─│ f'   ⊕ = merkez (son waypoint)
   │      Drone 1        │   ← 7 m
   │   (b–a arası, kuzeye)│
   │                     │
   b ─────────────────── a
```

### Adımlar

1. **Orta noktalar:** `e` = b ile d'nin orta noktası, `f` = a ile c'nin orta noktası. `e–f` çizgisi alanı ikiye bölen orta çizgidir.
2. **Geçiş aralığının bulunması (ikiye bölme):** `b` ile `e` arasındaki mesafe, `haversine` ile ölçülerek 10 m'nin (`0.01` km) altına inene kadar tekrar tekrar ikiye bölünür. Bölme sayısı `counter`, geçiş sayısı ise `2^counter` olur.
3. **Zikzak rota:** Her adımda koordinat `(e − b) / 2^counter` kadar kaydırılır ve drone a-kenarı ile b-kenarı arasında gidip gelir:
   ```
   b → b+δ → a+δ → a+2δ → b+2δ → b+3δ → a+3δ → …
   ```
   Bu, orta çizgiye (`e–f`) ulaşılana kadar sürer.
4. **Son nokta:** Rotanın sonuna `e` ile `f`'nin orta noktası, yani **dikdörtgenin merkezi** eklenir.

Fonksiyon `LocationGlobalRelative` nesnelerinden oluşan bir liste döndürür; toplam uzunluk `2 · 2^counter + 1`'dir.

### İki drone ile kullanım

İki drone aynı fonksiyonu köşeleri farklı sırayla vererek kullanır:

| | Çağrı | Taranan bölge | İrtifa |
|---|---|---|---|
| Drone 1 | `algorithm1(a, b, c, d)` | a–b kenarından orta çizgiye (alt yarı) | 7 m |
| Drone 2 | `algorithm1(d, c, b, a)` | d–c kenarından orta çizgiye (üst yarı) | 11 m |

İki drone da tarama bitince merkeze gider. Farklı irtifalarda uçtukları için merkezde ve dönüşte çarpışmazlar.

**Örnek:** Kodda tanımlı koordinatlarla (~200 m × ~200 m) her drone için `counter = 5` olur: 32 geçiş, geçişler arası ~3,1 m, toplam **65 waypoint**.

## Görev akışı (`missionForDrone*.py`)

1. SITL'e bağlan ve drone'un arm edilebilir olmasını bekle.
2. `GUIDED` moda geç, motorları arm et, hedef irtifaya kalk (7 / 11 m) ve irtifanın %95'ine ulaşılmasını bekle.
3. Görev komutlarını oluştur:
   - Başlangıç köşesine iki kez `NAV_WAYPOINT` (ArduPilot 0. görev öğesini home olarak kullandığı için ilk öğe tekrarlanır),
   - `algorithm1()`'in döndürdüğü tüm waypoint'ler,
   - `NAV_RETURN_TO_LAUNCH`.
4. Komutları yükle ve `AUTO` moda geç.
5. Tüm waypoint'ler tamamlanana kadar `commands.next` değerini izle.
6. Drone inip disarm olana kadar bekle, görev listesini temizle ve bağlantıyı kapat.

## Kurulum

```bash
pip install dronekit pymavlink
```

> **Not:** `dronekit` 2.9.2, Python 3.10+ ile `collections.MutableMapping` hatası verir. Python 3.9 veya daha eski bir sürüm kullanın ya da `dronekit/__init__.py` içinde `collections.MutableMapping` ifadesini `collections.abc.MutableMapping` ile değiştirin.

## Çalıştırma

1. İki ayrı ArduCopter SITL örneği başlatın. Örneğin ArduPilot kaynak dizininde:
   ```bash
   sim_vehicle.py -v ArduCopter -I0 --out=127.0.0.1:14550
   sim_vehicle.py -v ArduCopter -I1 --out=127.0.0.1:14560
   ```
   Koddaki koordinatlar SITL'in varsayılan konumunun (CMAC, Canberra) yakınındadır.
2. Her drone için görev betiğini ayrı bir terminalde çalıştırın:
   ```bash
   python missionForDrone1.py
   python missionForDrone2.py
   ```

Farklı bir alanı taramak için her iki betikteki `lat1..lat4` / `lon1..lon4` değerlerini değiştirin.

## Bilinen notlar

- **Kod yorumları ile kod uyuşmuyor:** [algorithm.py](algorithm.py) içinde eşik değeri yorumda `0.001` km yazıyor, kodda ise `0.01` km (10 m) kullanılıyor. Ayrıca `e` noktası "c ve d arası", `f` noktası "a ve b arası" diye açıklanmış; kodda `e` b–d, `f` ise a–c orta noktasıdır.
- **Gerçek geçiş aralığı 10 m değil:** Mesafe, bölme işleminden *önce* ölçüldüğü için döngü bir kez fazla bölme yapar. Bu nedenle geçiş aralığı 10 m değil, 2,5–5 m arasında olur.
- **Sabit irtifa:** `algorithm1()` tüm noktaları 7 m irtifayla oluşturur. Drone 2'nin 11 m'de uçması, görev betiğinin `Command` içinde irtifayı ayrıca 11 olarak vermesi sayesindedir.
- **`RTL_ALT` birimi:** ArduCopter'da `RTL_ALT` **santimetre** cinsindendir. `7` / `11` değerleri 7 / 11 cm anlamına gelir. Drone'lar bundan yüksekte uçtukları için dönüşü mevcut irtifalarında yaparlar; irtifa ayrımı bu sayede korunur. Metre cinsinden bir dönüş irtifası istenirse değer `700` / `1100` olarak girilmelidir.
- Dikdörtgenin kenarlarının enlem/boylam eksenlerine paralel olduğu varsayılır. Alan dikdörtgen değilse orta noktalar ve geçişler beklendiği gibi olmaz.
