---
id: system-performance
title: تحلیل پرفورمنس :‌ Load Average و I/O Wait
sidebar_label: 4. Performance & I/O
description: درک عمیق Load Average، تشخیص گلوگاه‌های دیسک (I/O Wait) و پروسه‌های Uninterruptible Sleep.
tags:
  - linux
  - troubleshooting
  - performance
  - load-average
  - io
---
سوال فنی:

یک زمانی پیش میاید که ما CPU مون کنده و هیچ پروسه ای Orphan و Zombie ای نداریم مشکل چیست؟

مشکل اصلی که ما در اینجا داریم `I/O Wai` هست که در نهایت موجب کندی CPU میشود.

حالا `I/O Wait` چیست ؟ زمانی که CPU منتظر دیسک ( یا سایر I/O Devices ) هست.

مراحل عملیات نوشتن روی دیسک:

1. ارسال درخواست
	- پروسه می‌خواهد روی دیسک بنویسد: `write(fd, data, 1MB)`

2. انتقال درخواست
	- سی پی یو درخواست را به دیسک می‌فرستد

3. حالت انتظار
	- سی پی یو منتظر می‌ماند
	- در وضعیت State: D (Uninterruptible Sleep)
	- **← این I/O Wait است!**

4. تاخیر دیسک
	- دیسک کند است
	- ممکن است 10-100ms طول بکشد

5. مسدود شدن CPU
	- سی پی یو نمی‌تواند کار دیگری انجام دهد
	- چون Process در حالت D است

چک کردن I/O Wait در سیستم:
دستور `top` :

```bash
$ top

top - 14:30:15 up 5 days
Tasks: 250 total, 1 running, 245 sleeping, 4 uninterruptible
%Cpu(s):  2.0 us,  1.0 sy,  0.0 ni, 10.0 id, 87.0 wa, 0.0 hi, 0.0 si
                                              ↑↑↑↑
                                         87% I/O Wait!
                                         
Meaning:
- us (user):     2%   ← کار واقعی
- sy (system):   1%   ← kernel overhead  
- id (Ideal):    10%   ← بیکار
- wa (iowait):  87%   ← منتظر I/O! ❌
```

دستور `iostat`: 

```bash
$ iostat

Device    r/s   w/s   rkB/s   wkB/s  await  %util
sda      50.0  200.0  1024    8192   125.5   98%
                                      ↑↑↑    ↑↑
                                   خیلی کند!  پر!

await: میانگین زمان انتظار (ms)
       - خوب:  < 10ms
       - بد:   > 50ms
       - وحشتناک: > 100ms

%util: درصد استفاده از دیسک
       - > 80% = مشکل!
```

دستور برای چک کردن پروسه هایی که در وضعیت D هستند:

```bash
$ ps aux | awk '$8 == "D"'

USER   PID  %CPU %MEM  STAT  WCHAN           CMD
mysql  1234  0.0  5.0   D    wait_on_buffer  mysqld
nginx  5678  0.0  1.0   D    io_schedule     nginx
app    9012  0.0  2.0   D    wait_on_page    ./app
        ↑                     ↑
    State: D          منتظر I/O کامل شود
```

اینها همه گیر کردند روی دیسک!

دستور `iotop` : 

```bash
$ sudo iotop -o

Total DISK READ: 5.00 M/s | Total DISK WRITE: 50.00 M/s
  PID  USER   DISK READ  DISK WRITE  COMMAND
 1234  mysql   0.00 B/s   45.00 M/s  mysqld
 5678  nginx   5.00 M/s    2.00 M/s  nginx
 9012  app     0.00 B/s    3.00 M/s  ./app
```

داخل خروجی بالا mysql دارد خیلی می‌نویسد!


حالا بریم سر وقت پروسه هایی که در وضعیت D هستند.

`State D -> Uninterruptible sleep`

این پروسه هارو نمیتوان `kill` کرد. چرا ؟

چون `process` در وسط عملیات `I/O` است و نمیتوان آن را قطع کرد. و همچنین چون در وضعیت `D` هستش signal نمیتواند به آن برسد باید صبر کنیم تا `I/O` تمام شود.

مثال process روی روی دیسک مینویسد اگر آن را `Interrupt` کنیم:
- داده ناقص نوشته میشود
- فایل سیستم خراب میشود

پس کرنل میگوید : نمیتوانی این را `Interrupt` کنی باید صبر کنی تا `I/O` تمام شود.

# مفهوم Load Average چیست؟
تعداد میانگین Process هایی که منتظر CPU هستند یا دارند اجرا میشود.

```bash
$ uptime
14:30:00 up 5 days, load average: 2.50, 1.80, 1.20
                                   ↑     ↑     ↑
                                   1min  5min  15min
```

ما در خروجی مورد نظرمون ۳ تا عدد داریم:

```
load average: 2.50, 1.80, 1.20
```

عدد اول از سمت چپ میانگین ۱ دقیقه گذشته است. 

عدد دوم از سمت چپ میانگین ۵ دقیقه گذشته است.

عدد سوم از سمت چپ میانگین ۱۵ دقیقه گذشته است.


حالا بریم ببینیم Load Average چه چیزی را می‌شمارد؟
داخل Load Average تعداد **Processهایی که در صف CPU هستند** یا **در حال اجرا هستند** را می‌شمارد.

در لینوکس سه دسته Process وارد Load Average می‌شوند:

۱) **Running (R)**  
پروسس‌هایی که همین الان روی CPU در حال اجرا هستند.

۲) **Runnable (R / Ready)**  
پروسس‌هایی که آمادهٔ اجرا هستند ولی CPU آزاد نشده، بنابراین در صف انتظار CPU هستند.

۳) **Uninterruptible Sleep (D)**  
این همان نکتهٔ همیشه غافلگیرکننده است. 

پروسس‌هایی که در حالت D هستند، یعنی «منتظر I/O به گونه‌ای که قطع‌پذیر نیست»، **در Load Average حساب می‌شوند**.

این یعنی: 

گاهی Load بالا می‌رود ولی CPU بیکار است → دلیلش I/O Wait است.

به زبان ساده:

Load Average =  

تعداد پروسه‌های **در حال اجرا** + تعداد **در صف CPU** + تعداد **در وضعیت D (I/O گیر کرده)**

```
Load = CPU-bound + I/O-bound processes
```

چگونه تفسیر کنیم؟

برای مثال یک سی پی یو ۴ هسته ای داریم:

با دستور زیر میتوانیم پیدا کنیم:

```
$ nproc
4 
```

حالا با هم بریم سناریو های مختلف رو بررسی کنیم:

```
4 core CPU
Load 2  → عالی  
Load 4  → مرز طبیعی  
Load 8  → CPU اشباع شده
Load 8 (اما 90% iowait) → CPU مشکلی ندارد؛ دیسک جهنم شده
```

خیلی خلاصه تر : 

`Load/Cores = X` :

تحلیل عدد بدست آمده به صورت زیر میباشد:

- `X < 1 → OK` ✅
- `X = 1-2 → Watch` ⚠️
- `X > 2 → Problem!` ❌
