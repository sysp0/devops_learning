---
id: linux-internals-fs
title: معماری لینوکس و فایل‌سیستم‌های مجازی
sidebar_label: 5. Kernel Space & /proc
description: تفاوت فضای کاربر و کرنل، و نحوه استخراج اطلاعات سیستمی از /proc و /sys.
tags: [linux, kernel, architecture, procfs, sysfs]
---

# User Space vs Kernel Space

ما و تمامی اپلیکشین ها در `user space` هستیم و برای ارتباط با سخت افزار و مدیریت باید از `Kernel Space` استفاده کنیم.

ما اگر بخواهیم چیزی رو بخونیم یا بنویسیم روی سخت افزار باید از کرنل استفاده کنیم.

دروازه کرنل چیزی هست به نام `syscal` که پلی بین کرنل و `user space` هستش.

از جمله `sycall` هایی که داریم : 
- `write()`
- `fork()`
- `read()`
- .....

# /proc Filesystem
ما داخل لینوکس میتوانیم لیست پروسه هارو توی یک پوشه داریم (در لینوکس همه چیز یک فایل هست) و هر اطلاعات خاصی از پروسه هارو که بخواهیم میتونیم پیدا کنیم.

وقتی فایل `status` رو مشاهده کنیم یک سری اطلاعات داریم:

```bash
➜  ~ cat /proc/603797/status               
Name:	code
Umask:	0002
State:	S (sleeping)
Tgid:	603797
Ngid:	0
Pid:	603797
PPid:	603508
TracerPid:	0
Uid:	1000	1000	1000	1000
Gid:	1000	1000	1000	1000
FDSize:	1024
Groups:	4 24 27 30 46 100 114 984 1000 
NStgid:	603797
NSpid:	603797
NSpgid:	603508
NSsid:	603508
Kthread:	0

```

و خیلی چیز های دیگری که ما به بیشتر این دیتا ها در آینده نیاز پیدا خواهیم کرد و تمامی بخش هارو توضیح میدیم.

همچنین ما یک پوشه داریم داخل `porc/` که `self` هستش. توضیح `self`:

پوشه **`/proc/self`** = یک symlink به `/proc/[PID]` خود Process فعلی است.

برای مثال :

```bash
$ echo $$
12345    ← PID bash

$ ls -l /proc/self
lrwxrwxrwx /proc/self -> 12345
```

مثال استفاده:
```bash
#!/bin/bash
# script.sh

echo "PID: $(cat /proc/self/status | grep Pid)"
echo "mem: $(cat /proc/self/status | grep VmRSS)"
echo "CPU: $(cat /proc/self/stat | awk '{print $14}')"
```

# /sys Filesystem

پوشه /sys در لینوکس یه «سیستم فایل مجازی» (virtual filesystem) هست که مستقیم به کرنل لینوکس وصل میشه و اطلاعات زنده و تنظیمات کرنل رو نشون میده.

با این پوشه میتونیم موارد زیر رو داشته باشیم
- چک کردن سخت‌افزار: `cat /sys/block/sda/size` → سایز دیسک
- دیدن CPU و فرکانس: `/sys/devices/system/cpu/cpu0/cpufreq/`
- تنظیم پارامترهای کرنل بدون ریبوت: `echo 1 > /sys/kernel/mm/transparent_hugepage/enabled`
- مانیتورینگ شبکه، مموری، swap، vm.drop_caches و …
- دیدن وضعیت دستگاه‌ها (USB، PCI، بلاک دیوایس‌ها)

و در آینده بیشتر درگیر این پوشه میشیم و cgroup هارو داخل این مدیریت میکنیم.
