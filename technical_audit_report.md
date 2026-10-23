# Chest X-Ray V5 — Son Teknik Kontrol ve Teslim Raporu

**Tarih:** 22 Ekim 2026. **Amaç:** Dr. Riel aracılığıyla Dr. Ko'ya sunulacak biyomedikal görüntü analizi kod örneğinin son kontrolü. Bu işlemde gönderim veya GitHub yayını yapılmadı. Notebook ve README akademik İngilizce; bu rapor Türkçedir.

## 1. Son karar

**Evet: proje, doğrulanan kapsamıyla biyomedikal görüntü analizi araştırmalarına ait bir kod örneği olarak Dr. Riel'e ve Dr. Ko'ya gönderilmeye hazırdır.** Bu karar kodun çalışabilirliği, dosya bütünlüğü, okunabilirliği ve sonuçların şeffaf sunulmasına dayanır. Bağımsız klinik doğrulamanın tamamlandığı, orijinal eğitimin yeniden üretildiği veya yeni bir yöntem üstünlüğünün kanıtlandığı anlamına gelmez.

İncelenecek dosya `Chest_XRay_Pneumonia_V5_Final_Research.ipynb`; çalıştırmak için yanındaki `assets/` ve `archive/` gereklidir. Önceki teslim ZIP'i korunmuştur. Yalnızca saptanan taşınabilirlik ve teslim eksikleri giderilmiş, yeni proje veya model eğitimi yapılmamıştır.

## 2. Kaynakların korunması ve SHA-256

Geliştirme kaydındaki 55 hücrenin tamamı, kodlar, 91 çıktı kaydı, 24 görsel, model referansları ve deney notları önceki denetimde incelendi; bu son kontrolde temiz notebookun 32 hücresi ve destek dosyaları yeniden kontrol edildi. Orijinal 55 hücrelik kaynakta hiçbir değişiklik yapılmadı.

Notebook metadata'sındaki `source_sha256`, arşivdeki Development Record ve mevcut orijinal dışa aktarımın SHA-256 değeri **aynıdır**:

`d3e37ab99931ea8aae0b0709d0fef20b10884fb1fede769e664733ae6335bcb6`

Seçili model SHA-256:

`2b9636582aa7281dcd01083931dcaabf5e0cff771405f6f81d88a4f03a455fc9`

İncelenen bu kaynak dosyalar arasında sürüm uyuşmazlığı yoktur. Önceki Colab içerik eşitliği denetimi kaynak/çıktı düzeyindedir; farklı arayüz metadata'sı veya sayaçlar için byte eşitliği iddia edilmez. Son temiz sürümün ayrıca yeni SHA-256 değeri vardır; temiz notebooktan Development Record ile aynı byte değerini vermesi beklenmez.

Kaynak hash kontrolü başlangıç koduna eklendi. Çalışma sırasında farklı bir Development Record verilirse işlem durur. Önceki temiz notebook, README, rapor ve çalıştırma kanıtları yerel yedekte; önceki tam inceleme ZIP'i de değişmeden korunur. Model ve `assets/` içindeki deney dosyaları değiştirilmez.

## 3. Harici dosyalar ve eksik varlıklar

`assets/integrity_manifest.json` ve listelenen 15 dosya mevcuttur; her biri kaydedilmiş SHA-256 değeriyle eşleşir. `assets/selected_model.keras` (23.50 MiB), doğrulama/test tahmin CSV'leri, orijinal test metrikleri, kilitli politika, veri ayrımı manifestosu, önceki ayrım denetimi, epoch seçim kayıtları, ortam bilgisi ve eğitim günlüğü/provenans dosyaları bulunmuştur. `archive/Chest_XRay_Pneumonia_V5_Development_Record.ipynb` de mevcuttur.

**Varsayılan kaydedilmiş-model akışını engelleyen eksik destek dosyası yoktur.** Ham görüntüler pakete alınmamıştır; bu kontrolde mevcut 5.856 görüntülük yerel veri ağacı kullanılmıştır. Yeni ortamda kullanıcı veriyi sağlayıcıdan indirmeli veya yerel kök dizinini belirtmelidir. Ayrıntılı dosya/hücre bağımlılıkları `evidence/submission_asset_audit.json` içindedir.

V1'in tam modeli/tahminleri ve V3 adaylarının tamamı V5 paketinde bulunmaz. Önceki sürümlerin karşılaştırma tablosu tarihsel kayıttır; bu sürümlerin yeniden değerlendirilmiş olduğu iddia edilmez. Ara `*_best.weights.h5` dosyaları, orijinal optimizer durumu ve native History nesneleri yoktur. Bunlar varsayılan V5 çıkarımı için gerekli değildir; orijinal eğitimi kaldığı yerden sürdürme veya birebir yeniden üretme iddiasını sınırlar. İlgili eğitim dalı açıkça kapalıdır.

## 4. Dosya yolları ve ortam uyumu

Kodda kişisel Windows kullanıcı dizinine zorunlu bağımlılık yoktur. Proje kökü `CONFIG['project_root']`, veri kökü ayrı bir ayardır. Veri dosya adları veri köküne, model/kanıt/sonuç yolları proje köküne görelidir. Önceki çıktıların yerine gerçek yeniden çalıştırmadan gelen çıktılar kaydedildi; çıktı klasörü artık göreli gösterilir. Harici veri dizininin kişisel tam yolu görüntülenmez, yeni dışa aktarılan ayarlarda açıkça 'yerel yol çıkarıldı' açıklaması bulunur. Çalıştırılabilir dosyanın yalnızca adı kaydedilir.

Bu işlem deney skorlarını veya klinik örnekleri silmez. Orijinal arşiv ve geçmiş ham kanıt dosyaları anonimleştirilmiş gibi gösterilmez; kişisel yol temizliği güncel teslim yüzeyi içindir. Önceki kanıtların korunmuş kopyaları ayrı tarihsel kayıt olarak tutulur.

Windows/CPU üzerinde yeni çekirdekle tüm akış çalıştırıldı. Colab için tam paketi açma, bağımlılıkları yükleme, runtime'ı yeniden başlatma ve proje kökünü ayarlama talimatları eklendi. Bu son kontrolde Colab'da ikinci bir uçtan uca yürütme yapılmadı; platform uyumu, taşınabilir kod ve talimat düzeyinde incelendi. Colab görüntüleme kopyası da güncellendi; 32 hücrenin kaynak/sıra/çıktı eşitliği ve sekiz görsel doğrulandı. Bu eşitlik yeni Colab yürütmesi anlamına gelmez. Colab aktarımda sayaçları temizler; yerel notebook gerçek sayaç/zamanları korur.

## 5. Ön işleme, mimari ve eğitim denetimi

Görüntü TensorFlow ile üç kanala çözülür, float32/0–255 aralığında 320×320 bilinear yeniden boyutlandırılır. Harici `/255` yoktur; EfficientNetV2 rescaling katmanı modelin içindedir. En-boy oranı korunmaz. ImageNet başlangıcı kaynak kod/günlüklerinde kayıtlıdır; eğitilmiş ağırlıklardan tek başına kanıtlanmış sayılmaz.

Mimari EfficientNetV2B0, global average pooling, 0,40 dropout ve sigmoid başlıktır. Kaydedilmiş model float32'dır. Genel seed 42, split seed 314, augmentation seed'leri 314–318, dropout seed 319'dur. Augmentation yalnızca eğitimdedir. Sınıf ağırlıkları yalnızca eğitim alt kümesinden hesaplanır: NORMAL 1,765172735761; PNEUMONIA 0,697601476015.

Tarihsel eğitim dört başlık ve on fine-tuning epoch'udur. Adam öğrenme oranları 0,001 ve 0,00001; label smoothing 0,04'tür. Son 160 backbone katmanı değerlendirilmiş; batch normalization donuk kalmış, ağırlıksız katmanlar dahil 128 katman bayrağı etkinleşmiştir. Backbone çağrısı `training=False` kullanır. Early stopping val_loss/patience 4; LR azaltma faktörü 0,3, patience 2, minimum 1e-7'dir. Model `compile=False` ile yüklenir, çıkarımda augmentation/dropout devre dışıdır.

Epoch içi checkpoint eşitlik bozma kuralı ile son eşik kuralı farklıdır ve bu tarihsel ayrıntı korunmuştur. Son eşik, doğrulamada precision/recall ≥%95 koşulunu sağlayan noktalar arasında özgüllük, daha yüksek eşik, ardından F1 sırasıyla seçilir. Eşik **0,72 yeniden hesaplanmıştır**, sonuç hedefi olarak zorlanmamıştır. Proje hedefleri klinik standart veya güven aralığı değildir. Eğitim accuracy eşiği 0,50, son değerlendirme eşiği 0,72'dir.

## 6. Veri ayrımı ve yöntemsel sınırlar

| Küme | NORMAL | PNEUMONIA | Toplam |
|---|---:|---:|---:|
| Eğitim | 1.071 | 2.710 | 3.781 |
| Doğrulama | 269 | 687 | 956 |
| Tarihsel test | 234 | 390 | 624 |

Görüntü byte hash'leri gerçek dosyalardan hesaplandı; mevcut orijinal havuz/test hash'leriyle eşleşti. Gruplu ayrım yeniden kuruldu ve kayıtlı dosya listeleriyle birebir uyuştu. Son kümeler arasında ortak yol, birebir hash ve dosya adı grup vekili sayısı sıfırdır. Hasta/site kimlikleri ve yakın tekrar denetimi yoktur; hasta bağımsızlığı iddia edilmez. Önceki görüntü düzeyi ayrımda saptanan 7 ortak hash ve 409 ortak dosya adı grubu bilgisi korunur.

V1 test tahminlerinden eşik seçmiş; V2–V4 aynı benchmark'ı geliştirme sırasında yeniden kullanmıştır. V3 normal sınıf hatalarının incelenmesi ve V4 deneyleri V5 tasarımından öncedir. V5 eşik seçimini doğrulamada yapar, fakat tarihsel testi tamamen bağımsız hale getirmez. Kaynakta doğrulama aşamasında eklenen kalibrasyon notu saklanır; tam ön kayıt iddiası yoktur.

## 7. Sonuçların yeniden doğrulanması

Arşiv tahminlerinin standart kütüphaneyle bağımsız hesabı, scikit-learn hesabı ve son yeni model çıkarımı aynı kararlara/metriklere ulaşmıştır. ROC-AUC ayrıca pozitif/negatif skor çiftlerinin sıralamasıyla kontrol edilmiştir.

| Ölçüt | 624 dosya | 618 benzersiz byte dizisi |
|---|---:|---:|
| TN / FP / FN / TP | 186 / 48 / 10 / 380 | 185 / 46 / 10 / 377 |
| Accuracy | %90,7051 | %90,9385 |
| Pnömoni precision | %88,7850 | %89,1253 |
| Recall | %97,4359 | %97,4160 |
| Specificity | %79,4872 | %80,0866 |
| F1 | %92,9095 | %93,0864 |
| ROC-AUC | 0,974567170721 | 0,974607649026 |

Altı fazladan yinelenen test dosyası vardır; birebir aynı byte dizisinde etiket çelişkisi yoktur. Benzersiz byte hesabı hasta bağımsızlığı anlamına gelmez. Doğrulamada TN/FP/FN/TP = 267/2/34/653; precision %99,6947 ve recall %95,0509'dur. Tarihsel test precision'ı %95 hedefini sağlamaz; bu durum gizlenmemiştir.

Tüm 48 FP ve 10 FN; dosya, gerçek sınıf, skor ve eşikten uzaklıkla sunulur. NORMAL hata sayıları IM 5/69 ve NORMAL2 43/165'tir; bunlar klinik alt grup/site kanıtı değildir. README ve notebook aynı sonuçları kullanır. Başarıyı artırmak için hiçbir sonuç değiştirilmemiştir.

## 8. Grafik ve Grad-CAM kontrolü

Sekiz gömülü görsel bulunur: eğitim/doğrulama eğrileri, doğrulama eşik grafiği, confusion matrix/ROC/precision–recall paneli, doğru/yanlış tahmin örnekleri ve dört Grad-CAM paneli. Eksenler, sınıf sırası, başlıklar, skor ve eşik etiketleri kontrol edilmiştir. Eğitim eğrileri, kaynak hücre 49'daki dört ondalıklı günlüklerden gelir; native History veya bu son kontrol sırasında yeniden eğitim olarak sunulmaz.

TN/TP/FP/FN örnekleri deterministik ilk dosya kuralıyla seçilir. Akciğer dışı işaret/boyun çevresindeki dikkat örnekleri saklanır; görüntüler bunu gizlemek için kırpılmamış veya değiştirilmemiştir. Isı haritası göreli ve kabadır. Grad-CAM klinik doğruluk, doğru lezyon lokalizasyonu veya nedensel kısa yol kanıtı değildir. Lezyon anotasyonu, açıklama sanity-check çalışması ve kontrollü maskeleme deneyi bu doğrulamanın parçası değildir.

Son yürütmedeki sekiz gömülü PNG, önceki incelenmiş sürümdeki sekiz PNG ile byte düzeyinde aynıdır. Görsel içeriğin değiştirilmediği ayrıca doğrulanmıştır (`evidence/submission_preservation.json`).

## 9. Gerçek çalıştırma kapsamı

Son kod değişikliklerinden sonra mevcut sabit bağımlılıklı ayrı ortamda **yeni bir ipykernel** başlatıldı. Python 3.12.14, TensorFlow 2.21.0, Keras 3.13.2; Windows/CPU kullanıldı. **16/16 kod hücresi, 86.5 saniye, sıfır hata çıktısı.** Bu turda ortam yeniden kurulmadı; daha önce temiz kurulmuş doğrulama ortamı kullanıldı. Model eğitimi yapılmadı.

Doğrulama skorlarının arşivden maksimum farkı `1.40500434875e-06`, tarihsel skorların farkı `1.34069679258e-06`; model tekrar yükleme farkı `0.0`. Sınıflandırma kararları ve metrikler aynıdır. Çekirdek dışındaki eski değişkenlere dayanılmamıştır. Import/model yükleme/tahmin/Grad-CAM ve çıktı üretimi gerçekten çalıştırılmıştır. Orijinal GPU eğitimini, optimizer devamını ve bağımsız dış değerlendirmeyi yeniden üretme iddiası yoktur.

Ham veri sağlayıcısının yinelenen ZIP'i yerine bir tam görüntü ağacı alınmıştır. Seçilen her üyenin ZIP CRC'si kontrol edilmiş; tam yinelenen arşivin MD5'i kontrol edilmemiştir. Mevcut orijinal SHA-256 görüntü kontrolleri ayrıca yapılmıştır. Eski hazırlık girişimleri başarılı son yürütme gibi gösterilmez.

## 10. Paylaşım ve GitHub hazırlığı

İngilizce README; proje, veri, yöntem, mimari, eğitim/değerlendirme, sonuçlar, Grad-CAM, sınırlamalar, yeniden çalıştırma ve klasör yapısını kapsar. Bağımlılıklar sabitlenmiştir; `.gitignore` ortam/cache/ham veri/ZIP dosyalarını dışlar, gerekli model ve kanıtları dışlamaz. Model 23.50 MiB'dir ve pakete dahil olduğundan uydurma indirme bağlantısı gerekmez. GitHub'a çıkarılmış dosyalar yüklenebilir; ham veri, yerel ortam ve cache yüklenmemelidir. GitHub deposu oluşturulmamış veya mevcut depoya push yapılmamıştır.

Üst veri kaynağının sayfasında CC BY 4.0 görüldü; kaynak/yaratıcı atfı ve görsellerdeki değişiklik açıklaması eklendi. Kaggle'ın güncel lisans alanı araçtan okunamadığından ayrıca doğrulanmış sayılmadı. Veri açıklamasındaki bağımsız hasta cümlesi OCT hakkındadır; X-ray için kullanılmadı. Kod/model için yeni toplu lisans atanmadı. Kurumsal yükümlülükler ve yazarın tüm dosyalar üzerindeki paylaşım yetkisi bu dosya denetimiyle kesinleştirilemez; genel kamuya yeniden lisanslama yapılmış gibi sunulmaz. Ayrıntılar İngilizce `THIRD_PARTY_NOTICES.md` dosyasındadır.

## 11. Yapılan sınırlı değişiklikler

1. Başlangıçta orijinal kaynak SHA-256 doğrulaması eklendi.
2. Güncel çıktılardaki gereksiz kişisel yollar kaldırıldı; proje çıktısı göreli gösterildi, harici veri yolu dışa aktarımda açıkça çıkarıldı.
3. Colab/yerel tam paket kullanımı ve bağımlılık talimatları netleştirildi.
4. Kaynak atıfları, paylaşım kontrolünün sınırları ve akciğer dışı Grad-CAM dikkati açıklaması eklendi.
5. README istenen başlıklara göre düzenlendi; teknik son rapor Türkçe yazıldı.
6. Destek dosyası/hücre eşlemesi, son teslim denetimi ve GitHub ignore dosyası eklendi.
7. Güncel notebook yeni oturumda yeniden çalıştırıldı; yeni sonuçlar ayrı zaman damgalı dizine yazıldı. Önceki kaynak/model/tahmin dosyaları değiştirilmedi.

Ek olarak bazı kod hücrelerinin satır düzeni otomatik biçimlendirildi. Bu hücrelerin Python sözdizim ağaçları önceki sürümle aynı; model, eşik, metrik ve Grad-CAM işlemlerinin mantığı değişmedi. Gerçek içerik değişiklikleri ve yalnızca biçimlenen hücreler `evidence/submission_change_log.json` içinde ayrı listelenir.

## 12. Dr. Ko'nun incelemesi açısından değerlendirme

| Soru | Doğrulanmış bulgulara dayalı değerlendirme |
|---|---|
| Teknik olarak düzgün mü? | Evet; varsayılan akış yeni çekirdekte tamamlandı, model/varlık/hash denetimleri geçti. |
| Kod okunabilir mi? | Evet; tek CONFIG, açıklayıcı fonksiyonlar, sıralı 32 hücre ve akademik İngilizce açıklamalar var. |
| Değerlendirme metodolojisi tutarlı mı? | Mevcut tarihsel benchmark iddiası kapsamında tutarlı; bağımsız genelleme/klinik doğrulama için yetersiz. |
| Sonuçlar doğru ve şeffaf mı? | Evet; bağımsız yeniden hesaplama, yeni çıkarım, tekrar ek analizi, eksik eğitim kanıtları ve test yeniden kullanımı açık. |
| Becerileri gösteriyor mu? | Evet; Python veri denetimi, TensorFlow/Keras model yükleme/eğitim kodu, transfer learning, eşik seçimi, metrik ve Grad-CAM uygulaması görülebiliyor. Bu, her özgün eğitim dalının yeniden yürütüldüğü anlamına gelmez. |
| Dr. Riel'e gönderilebilir mi? | Evet; tam paket veya aynı yapıyı koruyan erişilebilir depo ile kod örneği olarak gönderilebilir. |
| Gönderim öncesi zorunlu teknik eksik var mı? | Varsayılan inceleme/çıkarım akışını engelleyen saptanmış teknik eksik kalmadı. Bağımsız klinik sonuç iddiası için ek çalışma gerekir. |

Bilimsel sonraki adım: seçilmiş modeli, ön işlemeyi ve 0,72 eşiğini sabitleyip uygun yaş/çekim/etiket tanımı olan, güvenilir hasta/site ayrımı bulunan bağımsız kohortta önceden tanımlanmış bir protokolle tek değerlendirme yapmaktır. Böyle bir sonuç üretilmemiştir.

## Kanıt konumları ve kaynaklar

`evidence/fresh_execution.json`, `final_quality_checks.json`, `submission_asset_audit.json`, `cell_inventory.csv`, `model_reference_inventory.csv`, `verification_environment_freeze.txt`; güncel sonuç dizini: `results/20261022T185949_703755Z`. Orijinal hücre envanteri 55 satırdır. Önceki paket ve yerel yedek önceki sürümü korur.

Birincil dış kaynaklar: [Mendeley Data v2](https://data.mendeley.com/datasets/rscbjbr9sj/2), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [GitHub dosya boyutu belgeleri](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [Keras EfficientNetV2](https://keras.io/api/applications/efficientnet_v2/efficientnet_v2_models/), [Keras transfer learning](https://keras.io/guides/transfer_learning/), [Grad-CAM makalesi](https://arxiv.org/abs/1610.02391). Bu kaynaklar projenin klinik başarısını doğrulamaz.
