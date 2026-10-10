# تجهيز ميتا

## الخطوات

1. **حساب Meta Business** على business.facebook.com باسم النشاط.
2. **تطبيق** على developers.facebook.com ← Create app ← نوع Business ← أضف منتج **WhatsApp**.
3. **الرقم:** من WhatsApp ← API Setup ← Add phone number. الأسهل رقم جديد مش مستخدم على تطبيق واتساب. خذ من نفس الصفحة: **Phone number ID** و **WhatsApp Business Account ID** (WABA ID).
4. **مفتاح دائم:** Business Settings ← Users ← System users ← أضف System user (Admin) ← Add assets: التطبيق وحساب واتساب ← Generate token بصلاحيات `whatsapp_business_messaging` و `whatsapp_business_management`، وبدون تاريخ انتهاء. المفتاح المؤقت من صفحة API Setup بينتهي بعد ساعات، فما تستعمله.
5. **وسيلة دفع:** WhatsApp Manager ← Payment settings.
6. **التأكد:** من API Setup ابعت `hello_world` لجوالك.
7. **Webhook:** WhatsApp ← Configuration ← Callback URL والـ Verify token ← Verify and save ← Manage ← اشترك بـ `messages` و `message_template_status_update`.
8. **توثيق النشاط التجاري (Business Verification)** بيرفع الحدود وبيحمي الحساب. بلّش فيه بكير لأنه بياخد أيام.

## قوالب الرسائل

- الحملات والعروض فئتها **Marketing**. اللوحة بتبعت القالب لميتا لحالها مع زرّين Quick reply، وميتا بترد بالموافقة على الـ Webhook.
- المتغير `{{1}}` هو اسم الشخص، ويُكتب باللوحة `{الاسم}`.
- أسباب الرفض الشائعة: صيغة غلط، رسالة غامضة أو مشبوهة، فئة غلط. اكتب واضح وباسم النشاط.
- تنبيه المالك (`alert_template`) قالب منفصل فئته **Utility**، وفيه متغير واحد بالنص.

## الحدود والجودة

- الرقم الجديد بيبلّش بحد عدد أشخاص باليوم، وميتا بترفعه لحالها لما الجودة تضل منيحة. خلّي `daily_limit` أقل منه.
- الجودة (`quality_rating`): أخضر، أصفر، أحمر. البلاغات والحظر بينزّلوها.

## حد رسائل التسويق لكل شخص (131049)

ميتا ممكن تمنع رسالة تسويق عن شخص إذا وصله تسويق كثير مؤخرًا من أي شركة. الحد بيعتمد كمان على كم بيفتح رسائل التسويق.
- لا تعيد قبل 24 ساعة على الأقل، لأن الإعادة الأسرع بتطوّل المنع.
- رسائل التسويق جوا نافذة خدمة مفتوحة (الشخص كتب خلال 24 ساعة) ما بيطبّق عليها الحد.
- بأوروبا وبريطانيا واليابان وكوريا الحد مش مفعّل، وأرقام أمريكا (+1) ما بتوصلها رسائل تسويق.

المصدر: developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits/

## التسعير (من 1 تموز 2025)

- الحساب على **رسالة القالب لما توصل**. السعر حسب الفئة ومفتاح دولة المستلم.
- مجاني: الرسائل العادية جوا نافذة الخدمة (24 ساعة من آخر رسالة من الشخص)، وقوالب Utility جوا النافذة.
- إعلانات «انقر لإرسال رسالة واتساب» بتفتح نافذة مجانية 72 ساعة لكل الرسائل.

المصدر: developers.facebook.com/documentation/business-messaging/whatsapp/pricing
