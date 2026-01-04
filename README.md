# InChef 🍳

**InChef** — это веб-платформа для продажи домашней еды, построенная на Django. Платформа соединяет домашних поваров (Chef) с клиентами (Client), позволяя продавать и покупать домашние блюда.

## 📋 Содержание

- [Описание](#описание)
- [Основные возможности](#основные-возможности)
- [Технологии](#технологии)
- [Требования](#требования)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Запуск проекта](#запуск-проекта)
- [Структура проекта](#структура-проекта)
- [Модели данных](#модели-данных)
- [URL-маршруты](#url-маршруты)
- [Docker](#docker)
- [Разработка](#разработка)
- [Лицензия](#лицензия)

## 📖 Описание

InChef - это маркетплейс домашней еды, где:
- **Повара (Chef)** могут создавать профили, добавлять свои блюда с фотографиями и описаниями, управлять каталогом
- **Клиенты (Client)** могут просматривать доступные блюда, фильтровать по категориям, добавлять в корзину и оставлять отзывы
- Система аутентификации с разделением ролей пользователей
- Корзина покупок для оформления заказов
- Система отзывов и оценок блюд

## ✨ Основные возможности

### Система пользователей
- ✅ Регистрация и аутентификация пользователей
- ✅ Два типа ролей: Chef (повар) и Client (клиент)
- ✅ Профили пользователей с аватарами
- ✅ Верификация пользователей
- ✅ Уникальные номера телефонов для каждого пользователя

### Управление продуктами
- ✅ Создание, редактирование и удаление продуктов (для поваров)
- ✅ Множественные изображения для каждого продукта
- ✅ Категоризация продуктов
- ✅ Система "корзины" для удаленных продуктов (soft delete)
- ✅ Фильтрация по категориям
- ✅ Детальные страницы продуктов

### Корзина покупок
- ✅ Добавление продуктов в корзину
- ✅ Управление количеством товаров
- ✅ Автоматический расчет общей стоимости
- ✅ Персональная корзина для каждого пользователя

### Система отзывов
- ✅ Оценка продуктов (1-5 звезд)
- ✅ Текстовые отзывы
- ✅ Один отзыв от пользователя на продукт
- ✅ Привязка отзывов к автору и продукту

## 🛠 Технологии

### Backend
- **Python 3.12**
- **Django 6.0** - веб-фреймворк
- **SQLite** - база данных (по умолчанию)
- **Pillow 12.1.0** - обработка изображений

### Frontend
- **HTML/CSS/JavaScript** - шаблоны Django
- **Static files** - стили и скрипты

### Дополнительно
- **Docker** - контейнеризация
- **Git** - контроль версий

## 📦 Требования

- Python 3.12 или выше
- pip (менеджер пакетов Python)
- Виртуальное окружение (рекомендуется)
- Docker и Docker Compose (для запуска в контейнере)

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd inchef
```

### 2. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate  # Для Linux/Mac
# или
.venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
cd inchef
python manage.py migrate
```

### 5. Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

Следуйте инструкциям для создания учетной записи администратора.

### 6. Сбор статических файлов

```bash
python manage.py collectstatic --noinput
```

## ⚙️ Конфигурация

### Настройки базы данных

По умолчанию проект использует SQLite. Для изменения базы данных отредактируйте `inchef/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Настройки медиа и статических файлов

В `inchef/settings.py`:

```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Секретный ключ

⚠️ **ВАЖНО**: Перед развертыванием в продакшн измените `SECRET_KEY` в `settings.py` на уникальный и сохраните его в безопасности!

### Разрешенные хосты

Для продакшена добавьте ваш домен в `ALLOWED_HOSTS`:

```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## 🎯 Запуск проекта

### Режим разработки

```bash
cd inchef
python manage.py runserver
```

Проект будет доступен по адресу: `http://127.0.0.1:8000/`

### Админ-панель

Доступ к админ-панели: `http://127.0.0.1:8000/admin/`

Войдите используя учетные данные суперпользователя.

## 📁 Структура проекта

```
inchef/
├── .venv/                      # Виртуальное окружение
├── inchef/                     # Основная директория проекта
│   ├── account/                # Приложение управления пользователями
│   │   ├── migrations/         # Миграции базы данных
│   │   ├── admin.py           # Настройки админ-панели
│   │   ├── forms.py           # Формы регистрации/входа
│   │   ├── models.py          # Модели User и Profile
│   │   ├── signals.py         # Сигналы (создание профиля)
│   │   ├── urls.py            # URL-маршруты
│   │   └── views.py           # Представления
│   │
│   ├── cart/                   # Приложение корзины
│   │   ├── models.py          # Модели Cart и CartItem
│   │   ├── views.py           # Логика корзины
│   │   └── ...
│   │
│   ├── product/                # Приложение продуктов
│   │   ├── models.py          # Product, Category, ProductImage, Review
│   │   ├── forms.py           # Формы продуктов
│   │   ├── views.py           # Представления продуктов
│   │   ├── urls.py            # URL-маршруты
│   │   └── ...
│   │
│   ├── main/                   # Главное приложение
│   │   ├── views.py           # Главная страница
│   │   └── urls.py            # URL-маршруты
│   │
│   ├── inchef/                 # Настройки проекта
│   │   ├── settings.py        # Основные настройки
│   │   ├── urls.py            # Главные URL
│   │   ├── wsgi.py            # WSGI конфигурация
│   │   └── asgi.py            # ASGI конфигурация
│   │
│   ├── templates/              # HTML шаблоны
│   │   ├── account/           # Шаблоны аккаунтов
│   │   │   ├── auth/          # Регистрация/вход
│   │   │   └── profile/       # Профили
│   │   ├── cart/              # Шаблоны корзины
│   │   ├── product/           # Шаблоны продуктов
│   │   ├── main/              # Главная страница
│   │   └── base.html          # Базовый шаблон
│   │
│   ├── static/                 # Статические файлы (CSS, JS)
│   ├── media/                  # Загруженные медиа файлы
│   ├── manage.py              # Django команды
│   └── db.sqlite3             # База данных SQLite
│
├── requirements.txt            # Python зависимости
├── Dockerfile                  # Docker конфигурация
├── docker-compose.yml          # Docker Compose файл
├── .gitignore                 # Git игнорируемые файлы
├── LICENSE                    # Лицензия проекта
└── README.md                  # Этот файл
```

## 🗄 Модели данных

### User (Пользователь)
```python
- username: CharField (имя пользователя)
- phone_number: CharField (уникальный номер телефона)
- role: CharField (chef/client)
- первичные поля от AbstractUser (email, password, etc.)
```

### Profile (Профиль)
```python
- user: OneToOneField (связь с User)
- avatar: ImageField (аватар пользователя)
- is_verified: BooleanField (верифицирован ли)
```

### Category (Категория)
```python
- name: CharField (название категории)
- slug: SlugField (URL-slug, генерируется автоматически)
```

### Product (Продукт)
```python
- owner: ForeignKey (владелец - повар)
- category: ForeignKey (категория)
- title: CharField (название блюда)
- description: TextField (описание)
- price: DecimalField (цена)
- is_active: BooleanField (активен ли)
- trashed_at: DateTimeField (дата удаления)
- created_at: DateTimeField (дата создания)
```

### ProductImage (Изображение продукта)
```python
- product: ForeignKey (связь с продуктом)
- image: ImageField (изображение)
- is_main: BooleanField (главное изображение)
```

### Review (Отзыв)
```python
- product: ForeignKey (продукт)
- author: ForeignKey (автор отзыва)
- grade: PositiveSmallIntegerField (оценка 1-5)
- text: TextField (текст отзыва)
- created_at: DateTimeField (дата создания)
```

### Cart (Корзина)
```python
- user: OneToOneField (связь с пользователем)
- created_at: DateTimeField (дата создания)
```

### CartItem (Элемент корзины)
```python
- cart: ForeignKey (корзина)
- product: ForeignKey (продукт)
- quantity: PositiveIntegerField (количество)
```

## 🌐 URL-маршруты

### Главные маршруты
- `/` - Главная страница
- `/admin/` - Административная панель Django

### Аккаунт (`/account/`)
- `/account/register/` - Регистрация нового пользователя
- `/account/login/` - Вход в систему
- `/account/logout/` - Выход из системы
- `/account/profile/<username>` - Профиль пользователя

### Продукты (`/products/`)
- `/products/` - Список всех продуктов (с фильтрацией по категориям)
- `/products/<id>/` - Детальная страница продукта

## 🐳 Docker

### Запуск с помощью Docker

```bash
# Сборка образа
docker build -t inchef .

# Запуск контейнера
docker run -p 8000:8000 inchef
```

### Использование Docker Compose

Если у вас есть `docker-compose.yml`:

```bash
docker-compose up -d
```

### Примечание по Dockerfile

Текущий `Dockerfile` требует доработки. Рекомендуется изменить последнюю команду:

```dockerfile
# Вместо RUN используйте CMD
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 👨‍💻 Разработка

### Создание миграций

После изменения моделей:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Запуск тестов

```bash
python manage.py test
```

### Создание нового приложения

```bash
python manage.py startapp app_name
```

Не забудьте добавить новое приложение в `INSTALLED_APPS` в `settings.py`.

### Полезные команды Django

```bash
# Создать суперпользователя
python manage.py createsuperuser

# Открыть Django shell
python manage.py shell

# Проверить конфигурацию
python manage.py check

# Очистить базу данных
python manage.py flush
```

## 🔧 Решение проблем

### Ошибка миграций

```bash
# Сбросить миграции (ОСТОРОЖНО: удалит данные)
python manage.py migrate --fake app_name zero
python manage.py migrate app_name
```

### Проблемы со статическими файлами

```bash
# Пересобрать статические файлы
python manage.py collectstatic --clear --noinput
```

### Проблемы с правами доступа к медиа

Убедитесь, что директория `media/` имеет правильные права доступа:

```bash
chmod -R 755 media/
```

## 📝 Рекомендации для продакшена

1. **Безопасность**:
   - Измените `SECRET_KEY` на уникальный
   - Установите `DEBUG = False`
   - Настройте `ALLOWED_HOSTS`
   - Используйте переменные окружения для чувствительных данных

2. **База данных**:
   - Используйте PostgreSQL вместо SQLite
   - Настройте регулярные бэкапы

3. **Статические файлы**:
   - Используйте CDN или nginx для раздачи статики
   - Включите компрессию и кэширование

4. **Сервер**:
   - Используйте Gunicorn или uWSGI
   - Настройте nginx в качестве reverse proxy
   - Включите HTTPS с Let's Encrypt

5. **Мониторинг**:
   - Настройте логирование
   - Используйте сервисы мониторинга (Sentry, etc.)

## 📄 Лицензия

Проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

---

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Если вы хотите помочь:

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 📧 Контакты

Если у вас есть вопросы, пожалуйста, создайте issue в репозитории.

---

**Приятного использования InChef! 🍳**
