---
id: cpu-scheduling
title: مفاهیم CPU Scheduling و الگوریتم‌ها
sidebar_label: 1. CPU Scheduling
description: بررسی نحوه تصمیم‌گیری سیستم‌عامل برای اجرای پروسه‌ها و انواع الگوریتم‌های زمان‌بندی مثل CFS و Round Robin.
tags: [linux, os, cpu, scheduling]
---


### مفهوم CPU Scheduling چیست؟
مغز تصمیم‌گیر سیستم‌عامل : **CPU Scheduler** 

وظایف Scheduler:

1. تصمیم‌گیری: کدام Process بعدی اجرا شود؟
2. مدیریت صف‌های آماده (Ready Queue)
3. اجرای الگوریتم زمان‌بندی


#### انواع Scheduling Algorithms:

#### 1. **FCFS (First Come First Serve)**

```
P1 ────────────
P2             ────────
P3                     ──────

ساده ولی ناکارآمد!
```

#### 2. **Round Robin (RR)**

```
P1 ──  ──  ──
P2   ──  ──  
P3     ──  ──

عادلانه! هرکس نوبت می‌گیرد
```

#### 3. **Priority Scheduling**

```
High Priority   ────────
Medium Priority        ────
Low Priority              ────

مهم‌ترها اول!
```

#### 4. **CFS (Completely Fair Scheduler)** - Linux مدرن


هر Process باید زمان "منصفانه" بگیرد
بر اساس Virtual Runtime

