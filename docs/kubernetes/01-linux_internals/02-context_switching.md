---
id: context-switching
title: هزینه‌ها و انواع Context Switch
sidebar_label: 2. Context Switching
description: تحلیل هزینه سوئیچ بین پروسه‌ها، تفاوت سوئیچ‌های داوطلبانه و اجباری و تاثیر آن بر پرفورمنس.
tags: [linux, performance, context-switch, kernel]
---
## هزینه Context Switch

**رایگان نیست**! Context Switch هزینه‌هایش:
1. ذخیره Registers: ~100 cycles
2. بارگذاری Registers: ~100 cycles
3. TLB Flush: ~1000 cycles
4. Cache Miss: ~10,000 cycles 
 جمع: ~1-10 میکروثانیه  


بعضی وقت ها هستش که برنامه کارش تمام میشود و برنامه را تحویل میدهد ولی بعضی وقت ها نه CPU به موقعیت timer interrupt میرسد و برنامه رو توی حالت Ideal میبرد و CPU رو ازش میگیرید.


```bash
$ cat /proc/[PID]/status | grep ctxt
voluntary_ctxt_switches:    1523
nonvoluntary_ctxt_switches: 234
```

>مفهوم Voluntary Process : خودش منتظر ماند (I/O)
مفهوم Nonvoluntary: زمانش تمام شد، اجباری گرفته شد!


##### Voluntary Context Switch (داوطلبانه)
**یعنی چی؟** Process خودش تصمیم گرفت که CPU را رها کند.

چرا این اتفاق می‌افتد؟

1. پروسه در حال اجراست و برای خواندن داده از دیسک درخواست می‌دهد.  
2. چون باید منتظر عملیات ورودی/خروجی بماند، به‌صورت داوطلبانه CPU را آزاد می‌کند.  
3. سیستم‌عامل یک Context Switch انجام می‌دهد، پروسه را به حالت **Waiting** می‌برد و CPU را به پروسهٔ دیگری واگذار می‌کند تا عملیات دیسک تمام شود.


مثال‌های Voluntary:
1. منتظر I/O
2. منتظر Network
3. خواب رفتن
4. منتظر Lock/Mutex

##### Nonvoluntary Context Switch (اجباری)

**یعنی چی؟** Process نمی‌خواست CPU را رها کند ولی سیستم‌عامل زورش داد!

چرا این اتفاق می‌افتد؟

1. پروسه در حال انجام محاسبات سنگین است و بدون توقف روی CPU کار می‌کند.  
2. تایمر سیستم‌عامل منقضی می‌شود؛ وقفه ایجاد می‌شود و Scheduler تصمیم می‌گیرد پروسه را اجباراً متوقف کند (Context Switch غیر داوطلبانه).  
3. پروسه از CPU کنار گذاشته می‌شود، حتی اگر هنوز کارش تمام نشده باشد، و نوبت به پروسهٔ بعدی می‌رسد.

مثال‌های Nonvoluntary:
1. وقتی **Time Slice تمام شود**
2. موقعی که **Process با Priority بالاتر بیاید**

برای مثال :

```
voluntary_ctxt_switches:    1,974,733
nonvoluntary_ctxt_switches: 1,092,815
```

نسبت: 1,974,733 / 1,092,815 ≈ 1.8

این چه معنایی داره؟

این Process احتمالاً:
- پروسه **I/O-bound** است (زیاد منتظر I/O می‌ماند)
- عملیات شبکه یا دیسک زیاد انجام می‌دهد
- خیلی وقت‌ها خودش CPU را رها می‌کند


مقایسه با انواع مختلف:
یک Process نوع I/O-bound (مثل Web Server):

```
voluntary:    10,000,000
nonvoluntary:  1,000,000
```

نسبت: 10:1 که یعنی ← زیاد منتظر Network/Disk می‌ماند


نگاه کردن به وضعیت فعلی : 

```bash
cat /proc/127245/status | grep State
# State: S (sleeping)
```

تحلیل State:
- S = Sleeping (منتظر I/O)
- R = Running
- D = Uninterruptible sleep

با دستور زیر میتونیم اطلاعات خیلی بیشتری رو پیدا کنیم:

```bash
$ ps -p 127245 -o comm,state,wchan
COMM       S  WCHAN
firefox    S  poll_schedule_timeout
```

کلید `WCHAN` یعنی چی؟ 

توضیح میده که الان پروسه منتظر چیست یعنی : Wait Channel


برای مثال `do_poll_constprop.0` یعنی تابع `()poll` در کرنل که یعنی این منتظر شبکه هست.

همچنین میتونیم با دستور زیر عملکرد و تابع هایی که فراخوانی میکند در سطح کرنل رو مشاهده کنیم:

```bash
strace -c -p [PID]
```


.