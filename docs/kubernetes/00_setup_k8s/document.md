# عنوان داکیومنت کلی
## مقدمه و هدف
این داکیومنت نحو پیاده سازی محیط تست برای تست کوبرنتیز رو مشخص میکند. 
## ابزار kubectl
ما برای ارتباط با Kubernetes API Server یک ابزار نیاز داریم تا باهاش ارتباط برقرار کنیم. با این ابزار میتونیم کوبرنتیز رو مدیریت کنیم. 

ابزار kubectl یک کامند لاین هستش که برای دپلوی و دیدن لاگ های و مدیریت کلاستر میتونیم ازش استفاده کنیم. برای جزئیات بیشتر به [داکیومنت رسمی](https://kubernetes.io/docs/reference/kubectl/) مراجعه کنید

[لینک نصب](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) `kubectl` 

## ابزار minikube و kind
ما برای استفاده کوبرنتیز داخل محیط تست میتوانیم از یک سری ابزار استفاده کنیم که کوبرنتیز رو برای ما شبیه سازی میکنند. برای مثال ابزار kind (Kubernetes in Docker) کلاستر کوبرنتیز رو روی داکر سیستم بالا میاره و هر نود رو یک کانتینر در نظر میگیره ولی ابزار minikube این عملیات رو روی محیط ماشین مجازی بالا میاره.

[لینک نصب](https://minikube.sigs.k8s.io/docs/start/) minikube

[لینک نصب](https://kind.sigs.k8s.io/docs/user/quick-start/) Kind

### مقایسه
ابزار minikube بیشتر در قسمت های زیر استفاده میشود:
-  یادگیری و آزمایش Kubernetes
-  توسعه لوکال با نیاز به dashboard و ابزارهای گرافیکی
-  شبیه‌سازی محیط production با VM
-  کار با LoadBalancer

ابزار kind بیشتر در قسمت های زیر استفاده میشود:
-  تست CI/CD پایپلاین‌ها
-  توسعه و تست Kubernetes controllers و operators
-  تست کلاسترهای چندنودی
-  محیط‌های سبک و سریع برای توسعه
-  تست compatibility با نسخه‌های مختلف Kubernetes

## جمع‌بندی
برای محیط تست، ابزارهای آماده‌ای مثل kind و minikube وجود دارند که استفاده از آن‌ها بسیار ساده است. اما برای محیط production، دو گزینه اصلی داریم:

**۱. استفاده از Managed Kubernetes سرویس‌های ابری** (مثل EKS، GKE، AKS) که تمام عملیات نگهداری و مدیریت کنترل پلین را ارائه‌دهنده سرویس بر عهده می‌گیرد.

**۲. راه‌اندازی Self-Managed Kubernetes** که در آن خودمان مسئول پیاده‌سازی، پیکربندی و نگهداری کامل کلاستر هستیم.
## منابع
https://kubernetes.io/docs/tasks/tools/
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
https://kind.sigs.k8s.io/docs/user/quick-start/
https://kubernetes.io/docs/reference/kubectl/
https://minikube.sigs.k8s.io/docs/start/
