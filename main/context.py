context = [
    (
        'main_page/', 'Ютуб видео на главной странице',
        '''
            <p><strong>Метод:</strong> GET </p>
            <p><strong>Описание:</strong> В ответе будет, список словарей, каждый элемент списка имеет структуру: </p>  
            <p><strong>Формат ответа:</strong></p>
                <pre style="padding-left: 20px;">
                    {
                        "id": int,
                        "title": str,
                        "url": str,
                        "image_url": str,
                    }
                </pre>  
            <p><strong></strong></p>
            <ul>
                <li><code>"id"</code> - Идентификатор, целое натурально число </li>
                <li><code>"title"</code> - Название видео на ютубе</li>
                <li><code>"url"</code> - Ссылка на видео</li>
                <li><code>"image_url"</code> - Ссылка на обложку видео, ссылка будет действительна одну минуту</li>
            </ul>
        '''
    ),
    (
        'side_panel/', 'Последнее обновления на сайте',
        '''
        <b>Метод:</b> GET<br><br>
        <p>Вернёт последние пять аниме, которые были обновлены (добавлена серия или озвучка).</p>
        <p>В ответе будет: Список словарей, каждый элемент списка имеет структуру:</p>
        <pre style="padding-left: 20px;">
        {
            "id": int,
            "title": str,
            "title_latin": str,
            "slug": str,
            "description": str,
            "episodes_number": int,
            "image_url": str,
        }
        </pre>
    <ul>
        <li><code>"title"</code> — Название аниме на русском</li>
        <li><code>"title_latin"</code> — Название аниме на латинице (прямая транслитерация с японского)</li>
        <li><code>"slug"</code> — URL-адрес аниме на сайте</li>
        <li><code>"description"</code> — Описание аниме на русском</li>
        <li><code>"episodes_number"</code> — Количество эпизодов</li>
        <li><code>"image_url"</code> — Ссылка на обложку аниме, ссылка будет действительна одну минуту</li>
    </ul>
        '''
    ),

    (
        'release/', 'Список всех релизов на сайте',
        '''
        <b>Метод:</b> GET<br><br>
        <p>Вернётся словарь из двух элементов:</p>
        
            <p><strong>pages</strong>: <code>int</code> — Количество страниц на сайте. На каждой странице отображается по 12 аниме.</p>
            <p><strong>anime_list</strong>: Список всех аниме на сайте, отсортированный по популярности. Каждый элемент списка представляет собой словарь с информацией об аниме. Структура словаря следующая:</p>
        
        
        <pre style="padding-left: 20px;">
        {
            "id": int,
            "title": str,
            "title_latin": str,
            "slug": str,
            "description": str,
            "episodes_number": int,
            "image_url": str,
        }
        </pre>
        <ul>
            <li><code>"id"</code> — Целое число больше или равное нулю</li>
            <li><code>"title"</code> — Название аниме на русском</li>
            <li><code>"title_latin"</code> — Название аниме на латинице, прямая транслитерация с японского названия</li>
            <li><code>"slug"</code> — На основе "title_latin", представляет собой URL-строку</li>
            <li><code>"description"</code> — Описание аниме на русском, длинный текст</li>
            <li><code>"episodes_number"</code> — Количество эпизодов</li>
            <li><code>"image_url"</code> — Строка с URL на картинку, ссылка будет действительна одну минуту</li>
        </ul>

        <p><strong>Примечания:</strong></p>
        <pre style="padding-left: 20px;">
        - В случае ошибок <code>image_url</code> может возвращаться неверная ссылка на несуществующее изображение.
        - Если аниме нет в базе данных, в <code>image_url</code> вернётся пустая строка.
        </pre>
        
        '''
    ),
    (
        'release/2/', 'Переход на конкретную страницу в релизах, в этом примере стр - 2',
        '''
        <b>Метод:</b> GET<br><br>
        Переходя по URL release/ вы на самом деле прописывали release/1. Автоматом прописывается первая страница
        '''
    ),
    (
        'release/filter/', 'Фильтрация',
        '''
        <b>Метод:</b> GET<br><br>
        
        <p>После указания URL можно указать через знак вопроса <code>data={}</code> параметры фильтрации и сортировки.</p>
        <p>Если не указать <code>data</code> и сделать запрос по <code>release/filter/</code>, не будут применены параметры фильтрации, и будут выведены все аниме в порядке популярности в формате <code>anime_panel</code>.</p><br>
        <pre>
        data = {
            "genres": [str, ...],
            "year": [int, ...],
            "season": [str, ...],
            "popular_or_new": str,
            "is_completed": bool,
        }
        </pre>
        <b>Параметры фильтрации:</b><br>
        <ul>
            <li><b>genres</b>: [str, ...] — Список жанров для фильтрации. Например: <code>"genres": ["Экшен", "Сёнен"]</code>. В данном примере будут выведены только те аниме, которые имеют в жанрах "Экшен" и "Сёнен". Аниме могут иметь и другие жанры, но все жанры из <code>genres</code> должны быть в аниме.</li>
            <li><b>year</b>: [int, ...] — Список годов для фильтрации. Например: <code>"year": [2020, 2021]</code>. В данном примере будут выведены аниме, выпущенные в 2020 и 2021 годах.</li>
            <li><b>season</b>: [str, ...] — Список сезонов для фильтрации. Например: <code>"season": ["Весна", "Осень"]</code>. В данном примере будут выведены аниме, которые выходили в сезоны "Весна" и "Осень".</li>
            <li><b>popular_or_new</b>: str — Параметр сортировки. Может принимать значения <code>"popular"</code> или <code>"new"</code>. Например: <code>"popular_or_new": "popular"</code> для сортировки по популярности, или <code>"new"</code> для сортировки по новизне.</li>
            <li><b>is_completed</b>: bool — Фильтр для завершенных аниме. Может быть <code>true</code> или <code>false</code>. Например: <code>"is_completed": true</code> для фильтрации только завершенных аниме.</li>
        </ul>
        '''
    ),
    (
        'release/filter/1/', 'Пагинация по фильтрации, стр - 1',
        'Параметр data={...} нужно прописывать после relase/int/'
    ),
    (
        'release/watch/black-clover/', 'Страница конкртеного аниме, после watch/ нужно прописать его id или slug',
        '''
        <p><strong>URL:</strong> <code>release/watch/&lt;int:anime_id&gt;/</code> или <code>release/watch/&lt;slug:anime_slug&gt;/</code></p>
        <p><strong>Метод:</strong> GET</p>
        <p><strong>Описание:</strong> Возвращает аниме с <code>id=anime_id</code> или <code>slug=anime_slug</code> в формате <code>anime_dict</code>. Если в базе данных нет такого аниме, вернётся ответ с статусом 404 и информацией об ошибке:</p>
        
        <pre style="padding-left: 20px;">
        {
            "detail": "Информация об ошибке"
        }
        </pre>
        
        <p><strong>Формат ответа:</strong></p>
        <pre style="padding-left: 20px;">
            <strong>anime_dict</strong> = {
                "id": int,
                "title": str,
                "title_latin": str,
                "slug": str,
                "description": str,
                "episodes_number": int,
                "image_url": str,
                "year": int,
                "season": str,
                "favorites_count": int,
                "status": str,
                "genres": [str, str, ...],
                "voices": [str, str, ...],
                "timings": [str, str, ...],
                "subtitles": [str, str, ...],
                "episode_url": str,
                "episode_number": int
            }
        </pre> 
        <p><strong>anime_dict:</strong></p>
        <ul>
    <li><code>"id"</code> — Целое число больше или равное нулю</li>
    <li><code>"title"</code> — Название аниме на русском</li>
    <li><code>"title_latin"</code> — Название аниме на латинице, прямая транслитерация с японского названия, реже перевод на английский</li>
    <li><code>"slug"</code> — На основе <code>title_latin</code>, представляет собой URL-строку</li>
    <li><code>"description"</code> — Описание аниме на русском, длинный текст</li>
    <li><code>"episodes_number"</code> — Количество эпизодов</li>
    <li><code>"image_url"</code> — Ссылка на обложку аниме в S3 AWS хранилище</li>
    <li><code>"year"</code> — Год</li>
    <li><code>"season"</code> — Сезон, может быть одним из: [winter, spring, summer, autumn]</li>
    <li><code>"favorites_count"</code> — Количество людей, добавивших аниме в любимые</li>
    <li><code>"status"</code> — Статус аниме, может быть одним из: [completed, ongoing, announcement]</li>
    <li><code>"genres"</code> — Список жанров. Если аниме не имеет жанров, список будет пустым</li>
    <li><code>"voices"</code> — Список голосов. Если аниме не имеет голосов, список будет пустым</li>
    <li><code>"timings"</code> — Список тех, кто отвечал за тайминги. Если аниме не имеет таймингов, список будет пустым</li>
    <li><code>"subtitles"</code> — Список тех, кто отвечал за субтитры. Если аниме не имеет субтитров, список будет пустым</li>
    <li><code>"episode_url"</code> — Ссылка на эпизод <code>episode_number</code> в S3 AWS хранилище. По умолчанию первый эпизод. Если аниме нет в базе данных или имеет ноль серий, вернётся пустая строка</li>
    <li><code>"episode_number"</code> — Номер серии</li>

        </ul>
        
        '''
    ),
    (
        'release/watch/random/', 'Страница рандомного анмие, работает анлогично release/watch/<anime_key>/',
        'Под капотом, просто вместо random ставится рандомное число'
    ),
    ('release/watch/31/1/', 'Возвращает episode_url, ссылка на эпизод, и  episode_number, номер серии',
     '''
    <p><strong>URL:</strong> <code> release/watch/<anime_id>/<episode_number>/ или release/watch/<anime_slug>/<episode_number>/</code></p>
    <p><strong>Метод:</strong> GET </p>
    <p><strong>Описание:</strong> Возвращает ссылку на конкретный эпизод episode_number для аниме с id=anime_id или slug=anime_slug </p>
    <p><strong>Формат ответа:</strong></p>
        <pre style="padding-left: 20px;">
            {
                "episode_url": str,
                "episode_number": int,
            }
        </pre> 
    <ul>
        <li><code>"episode_url"</code> - Ссылка на видео, ссылка будет действительна одну минуту</li>
        <li><code>"episode_number"</code> - Номер эпизода</li>
    </ul>
        
    <p><strong>Примечания:</strong></p>
        <ul>
        <li> - Если же в базе данных нету такого эпизода, то статус в ответе будет 404 и также информация об ошибке {"detail": "информация"} </li>
        <li> - Если же в s3 хранилище нету такой серии, а в бд она есть, то будет возвращена нерабочая ссылка на несуществующее аниме </li>
        </ul>
     '''),
]

'''
    <p><strong>URL:</strong> <code> URL </code></p>
    <p><strong>Метод:</strong> Method </p>
    <p><strong>Описание:</strong> Description </p>
        <pre style="padding-left: 20px;">
            {
                maybe
            }
        </pre>    
    <p><strong>Формат ответа:</strong></p>
    <pre style="padding-left: 20px;">
            {
                maybe
            }
        </pre>    
    <p><strong>anime_dict:</strong></p>
    <ul>
        <li><code>id</code>: <code>int</code> — Целое число больше или равное нулю</li>
    </ul>
'''
#
#
#     'release/watch/1/': 'Страница конкртеного аниме, число это индекс тайтла',
#
#     'release/watch/1/0':
# '''Конкретная серия какого-то аниме, первое число это индекс аниме тайтла, а второе число это конкретный эпизод.
# Нулевой эпизод это опенинг''',
#
#     'user/signup/':
# '''Регистрация на сайте, форма для POST запроса, которая принимает username, email и password.
# Если данные валидны то будет создан пользователь и ссылка на активацию будет отправлен на почту''',
#
#     'user/login/': 'Авторизация на сайте',
#
#     'user/logout/': 'Разлогинивание от сайта',
#
#     'user/user_info/': 'Тестовый маршрут для проверки авторизации и прав',
#
#     'user/activate/<какой-то токен>/': 'Активация аккаунта по ссылке, отправленной на почту',
#
#     'user/profile/': 'Профиль пользователя'
# }
