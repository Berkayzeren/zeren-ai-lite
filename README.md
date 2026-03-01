# Zeren AI Lite

Zeren AI Lite, ticari amaçlı geliştirilen ana **Zeren AI** projesinin açık kaynaklı, hafifletilmiş (lite) bir versiyonudur. Bu depo, projenin mimari yapısını, temel prensiplerini ve kodlama standartlarını iş arama süreçlerinde sergilemek amacıyla oluşturulmuştur.

> [!IMPORTANT]
> **Not:** Bu depo, projenin sadece temel iskeletini ve halka açık paylaşılabilecek kısımlarını içerir. Algoritmik ticaret stratejilerinin tamamı, tescilli modeller ve veri setleri gizlilik nedeniyle ana projede tutulmaktadır.

## 🚀 Proje Hakkında
Zeren AI, borsa ve kripto paralar üzerinde derin öğrenme ve takviyeli öğrenme (Reinforcement Learning) tabanlı otonom bir ticaret motorudur. Lite versiyonu şu temel özellikleri barındırır:

- **Modüler Mimari:** `AIModule` tabanlı asenkron yapı.
- **Risk Yönetimi:** Kelly Kriteri ve `Neural Risk Guard` mantığının temel implementasyonları.
- **Modern UI:** Next.js ve Shadcn UI kullanılarak tasarlanmış dashboard taslakları.
- **Evrensel Dil Desteği (i18n):** Türkçe ve İngilizce tam senkronize altyapı.

## 🛠️ Mimari Standartlar
Zeren AI geliştirme süreçlerinde şu prensipler kırmızı çizgidir:
1. **Tip Güvenliği:** Python'da Pydantic ve Type Hints, frontend'de TypeScript kullanımı zorunludur.
2. **Asenkron Operasyon:** Tüm I/O işlemleri `async/await` ile yönetilir.
3. **Dokümantasyon:** Tüm kodlar Google-style docstring'ler ile belgelenmiştir.

## 📂 Dosya Yapısı
- `src/core/`: Sistemin kalbi, temel modül sınıfları.
- `src/strategy/`: Risk yönetimi ve sinyal üretim mantığı.
- `dashboard/`: Kullanıcı arayüzü bileşenleri.
- `docs/`: Mimari ve kullanım dokümanları.

## ⚠️ Yasal Uyarı
Bu proje eğitim ve portfolyo amaçlıdır. **YATIRIM TAVSİYESİ DEĞİLDİR.** Finansal piyasalarda işlem yapmak yüksek risk içerir.

---
*© 2026 Zeren AI - Advanced Agentic Coding Team*
