# 1. Create Table
```sql
-- 1. Membuat Tabel Master Dokter
CREATE TABLE `dummy_hospital.dokter` (
  dokter_id INT64 OPTIONS(description="ID unik untuk setiap dokter (Primary Key)"),
  nama_dokter STRING OPTIONS(description="Nama lengkap beserta gelar dokter"),
  spesialisasi STRING OPTIONS(description="Bidang keahlian medis dokter"),
  PRIMARY KEY (dokter_id) NOT ENFORCED
) 
OPTIONS(description="Tabel master yang menyimpan data dokter di rumah sakit");

-- 2. Membuat Tabel Master Pasien
CREATE TABLE `dummy_hospital.pasien` (
  pasien_id INT64 OPTIONS(description="ID unik untuk setiap pasien (Primary Key)"),
  nama_lengkap STRING OPTIONS(description="Nama lengkap pasien sesuai KTP"),
  tanggal_lahir DATE OPTIONS(description="Tanggal lahir pasien untuk menghitung umur"),
  jenis_kelamin STRING OPTIONS(description="Jenis kelamin pasien: 'L' untuk Laki-laki, 'P' untuk Perempuan"),
  golongan_darah STRING OPTIONS(description="Golongan darah pasien (A, B, AB, O)"),
  PRIMARY KEY (pasien_id) NOT ENFORCED
) 
OPTIONS(description="Tabel master yang menyimpan data demografi pasien");

-- 3. Membuat Tabel Transaksi Kunjungan
CREATE TABLE `dummy_hospital.kunjungan` (
  kunjungan_id INT64 OPTIONS(description="ID unik untuk setiap rekam kunjungan (Primary Key)"),
  pasien_id INT64 OPTIONS(description="ID Pasien yang berkunjung (Foreign Key ke tabel pasien)"),
  dokter_id INT64 OPTIONS(description="ID Dokter yang menangani (Foreign Key ke tabel dokter)"),
  tanggal_kunjungan DATE OPTIONS(description="Tanggal saat pasien melakukan kunjungan"),
  keluhan_utama STRING OPTIONS(description="Keluhan yang dirasakan pasien saat mendaftar"),
  diagnosis_akhir STRING OPTIONS(description="Hasil diagnosis dokter setelah pemeriksaan"),
  
  -- Mendefinisikan Konstrain
  PRIMARY KEY (kunjungan_id) NOT ENFORCED,
  FOREIGN KEY (pasien_id) REFERENCES `dummy_hospital.pasien`(pasien_id) NOT ENFORCED,
  FOREIGN KEY (dokter_id) REFERENCES `dummy_hospital.dokter`(dokter_id) NOT ENFORCED
) 
OPTIONS(description="Tabel transaksi yang mencatat riwayat kunjungan medis pasien beserta dokter yang menangani");
```
---
# 2. Insert Dummy Data

```sql
-- Insert data ke tabel dokter
INSERT INTO `dummy_hospital.dokter` (dokter_id, nama_dokter, spesialisasi)
VALUES 
  (1, 'Dr. Andi Pratama, Sp.PD', 'Penyakit Dalam'),
  (2, 'Dr. Budi Santoso, Sp.A', 'Anak'),
  (3, 'Dr. Citra Kirana, Sp.M', 'Mata');

-- Insert data ke tabel pasien
INSERT INTO `dummy_hospital.pasien` (pasien_id, nama_lengkap, tanggal_lahir, jenis_kelamin, golongan_darah)
VALUES 
  (101, 'Ahmad Fauzi', '1985-04-12', 'L', 'O'),
  (102, 'Siti Aminah', '1992-08-25', 'P', 'A'),
  (103, 'Bagas Dwi', '2015-11-03', 'L', 'B'),
  (104, 'Rina Marlina', '1978-12-30', 'P', 'AB');

-- Insert data ke tabel kunjungan (menghubungkan pasien dan dokter)
INSERT INTO `dummy_hospital.kunjungan` (kunjungan_id, pasien_id, dokter_id, tanggal_kunjungan, keluhan_utama, diagnosis_akhir)
VALUES 
  (1001, 101, 1, '2024-02-15', 'Nyeri ulu hati dan mual', 'Gastritis (Maag)'),
  (1002, 103, 2, '2024-02-16', 'Demam tinggi selama 3 hari', 'Gejala Tifus'),
  (1003, 102, 3, '2024-02-18', 'Mata merah dan gatal', 'Konjungtivitis'),
  (1004, 101, 1, '2024-03-01', 'Kontrol rutin tekanan darah', 'Hipertensi Ringan');
```