# معمارية النظام

## الـ workflows الأربعة

### المرسل (Sender)
يصحى كل 5 دقايق (`Every 5 min`).
- `Gate`: بيكمّل بس إذا في حملة إجا دورها (ساعاتها، أيامها، «كل كم دقيقة»، ووقف صلاة الجمعة)، أو إذا صار وقت فحص المتابعات.
- `Check Quality`: بيقرأ `quality_rating` للرقم من ميتا. حسب `quality_guard` بيوقف كل الحملات إذا صارت صفرا أو حمرا.
- `Decide`: قلب الإرسال. لكل حملة بيحسب الحد اليومي مع التدرّج (`ramp`)، والعدد الكلي (`total_cap`)، ونسبة «مش مهتم»، والأخطاء، وقاعدة الأيام بين حملتين لنفس الشخص (`min_gap_days`). بيوزّع النسخ A/B/C بالتساوي. واللي كتبلنا آخر 23 ساعة (`last_in_at`) بيطلعله دور قبل الكل. بيطلع أفعال: `pause`، `batch`، `send`، `giveup`.
- `Send Template` ← `Result` ← `Update Contacts`: الإرسال ونتيجته. 131049 بيرجع `retry_later` بعد `cap_retry_hours` ساعة. بعد `max_tries` محاولة بيصير `capped`.
- `Follow Ups`: رسالة متابعة للمهتم بعد `followup_after` دقيقة، إذا ما رد بسؤال.
- `Daily Checks`: تذكير بانتهاء السيرفر (`server_expires`).

### المستقبل (Receiver)
Webhook على `/webhook/whatsapp-controller` (GET للتحقق، POST للأحداث).
- `Parse Events`: بيقبل بس أحداث `phone_number_id` و `waba_id` تبع الإعدادات.
- الحالات: `Map Status` ← `Chat Status Now` (فوري) و `Wait Status` (45 ثانية، لحد ما يتسجل سطر الإرسال) ← تحديث `Contacts` و `WAC Chats`. سبب الفشل بينحفظ بالمحادثة كـ `failed_<رمز ميتا>`.
- الرسائل: `Chat In` بيسجلها، `Classify` بيصنّف (`interested`، `opted_out`، `replied`) حسب الأزرار وكلمات `yes_words` و `stop_words`، `Build Reply` بيبعت الرد التلقائي، `Message Notes` بيبعت الإشعار.
- موافقة القوالب: `Template Event` بيحدّث `Messages`.

### لوحة التحكم (Panel)
- `/webhook/wac`: الصفحة (HTML كامل جوا عقدة `Send Page`).
- `/webhook/wac-status`: الحالة، والحملات، والإعدادات. `x-campaign` لحملة وحدة، و `?full=1` لكل الصفوف.
- `/webhook/wac-action` (POST نص JSON): كل الأفعال. `Route` بيفحص الرمز وكل قيمة، وبيرفض الغلط برسالة عربية.
- `/webhook/wac-chats`: صندوق المحادثات. `x-wa: <رقم>` لمحادثة، و `x-wa: test:<cid>` لنتيجة رسائل التجربة.
- `/webhook/wac-file`: أيقونات، manifest، وملف service worker.
- الرمز بيتبعت بالهيدر `x-pin`. 10 محاولات غلط بربع ساعة بتقفل الدخول مؤقتًا.

### الإشعارات (Notify)
بيستدعيه الثلاثة بـ Execute Workflow. `Plan` بيقرر: إشعار بالجدول (`WAC Notes`)، وإشعار Push للأجهزة المسجلة (VAPID)، وتنبيه واتساب لأرقام `alert_numbers` عبر قالب `alert_template` (فيه متغير واحد بالنص، وفئته Utility).

## الجداول

كل الأعمدة نص (string).

- `Contacts`: كل رقم بكل حملة. `delivery`: `pending`، `sending`، `sent`، `delivered`، `read`، `retry_later`، `retry_alt` (بس فلسطين)، `no_whatsapp`، `send_error`، `failed`، `capped`، `skip`. `response`: `interested`، `opted_out`، `replied`.
- `Settings`: مفتاح وقيمة لكل الإعدادات العامة.
- `Messages`: النسخ A/B/C لكل حملة، واسم القالب عند ميتا، وحالته (`PENDING`، `APPROVED`، `REJECTED`).
- `Log`: أحداث الحملات.
- `WAC Chats`: كل رسالة داخلة وطالعة. `kind`: `template`، `auto`، `followup`، `manual`، `test`، `button`، `text`، `media`. `status`: `sent`، `delivered`، `read`، `failed_<رمز>`.
- `WAC Campaigns`: إعدادات كل حملة.
- `WAC Notes`: الإشعارات.
- `WAC Push`: أجهزة الإشعارات.

## الإعدادات المهمة (جدول Settings)

- الربط: `phone_number_id`، `waba_id`، `api_version`، `template_language`، `template_category`.
- الدخول: `panel_pin`، `panel_url`.
- الأرقام: `primary_cc` (مفتاح الدولة للأرقام المحلية؛ فاضي يعني الأرقام دولية جاهزة)، `wa_phone` (رقم الحملة للرابط والـ QR).
- السرعة: `daily_limit`، `ramp`، `batch_size`، `send_hour_start`، `send_hour_end`، `min_gap_days`.
- الحماية: `quality_guard`، `max_optout_rate`، `optout_min`، `max_errors`.
- الإعادة: `cap_retry_hours`، `max_tries`، `retry_days`.
- التجربة: `test_numbers`، `test_name`، `name_fallback`.
- التنبيهات: `alert_numbers`، `alert_whatsapp` (`auto` أو `off`)، `alert_template`، `alert_language`، `alert_throttle_min`، `notify_kinds`.
- الفهم: `yes_words`، `stop_words`، `question_len`.

كلها بتتعدل من اللوحة ← الإعدادات العامة، والتغيير بيمشي من أول دورة.
