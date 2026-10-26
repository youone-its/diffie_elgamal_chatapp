# Diffie-Hellman & ElGamal Encryption and Key Transfer Algorithm

Contoh sederhana buat bertukar kunci dan mengirim pesan terenkripsi antara Alice dan Budi.

### Made By:

|Nama|NRP|
| :---------------- | :------: |
| Evan Christian N | 5027241026 |
| Yuan Banny Albyan | 5027241027 |
| Rayka Dharma P | 5027241039 |

---

# Core Concept

## Key Generation

Program memakai bilangan prima `p = 467` dan generator `g = 2`. Setiap orang memilih kunci pribadi `x` secara acak dari `2` sampai `p - 2`, lalu menghitung kunci publik:

`y = g^x mod p`

## Key Exchange

Di contoh Diffie-Hellman pada API, Alice punya kunci pribadi `a` dan kunci publik `A = g^a mod p`. Budi punya `b` dan `B = g^b mod p`. Setelah bertukar kunci publik, keduanya menghitung:

`s = B^a mod p = A^b mod p`

Hasil `s` sama, sementara kunci pribadi tetap disimpan sendiri. Chat memakai kunci publik untuk ElGamal; hasil pertukaran `s` tidak dipakai oleh chat.

## Encryption

Saat chat, tiap byte pesan `b` diubah jadi `m = b + 1`. Untuk setiap `m`, program memilih angka acak `k` dari `2` sampai `p - 2`, lalu mengenkripsi dengan kunci publik penerima `y`:

`c1 = g^k mod p`  
`c2 = (m × y^k) mod p`

Pesan terenkripsi adalah pasangan `(c1, c2)`.

## Decryption

Penerima memakai kunci pribadi `x` untuk menghitung:

`s = c1^x mod p`  
`m = (c2 × s⁻¹) mod p`

`s⁻¹` adalah kebalikan `s` dalam modulo `p`. Untuk chat, byte asli didapat dari `b = m - 1`.

# Implementation

## Chat

Jalankan server dulu dengan `python Backend/UserAPI/API.py`. Lalu buka dua terminal lain: jalankan `python Frontend/Alice.py` dan `python Frontend/Budi.py`. Kalau Flask belum terpasang, jalankan `pip install -r requirements.txt`.

## API

`Backend/UserAPI/API.py` menyediakan layanan untuk kunci, pertukaran kunci, enkripsi, dekripsi, dan pengiriman pesan chat.

## Generator

`Backend/generator/` berisi fungsi untuk membuat kunci, mencari akar primitif, serta mengenkripsi dan mendekripsi pesan.

## Checker

`Backend/checker/` mengecek apakah `g` merupakan akar primitif dari `p`. Untuk setiap faktor prima `q` dari `p - 1`, syaratnya:

`g^((p - 1) / q) mod p ≠ 1`

Angka dalam contoh ini kecil agar mudah dipelajari, jadi jangan dipakai untuk mengamankan pesan sungguhan.
