from My_News_Portal.models import *

# Создание пользователей
u1 = User.objects.create_user(username='Джордж Лукас')
u2 = User.objects.create_user(username='Нил Деграсс Тайсон')

# Создание авторов
a1 = Author.objects.create(authorUser=u1)
a2 = Author.objects.create(authorUser=u2)

# Создание категорий
c1 = Category.objects.create(name='StarWars')
c2 = Category.objects.create(name='Astrophysics')
c3 = Category.objects.create(name='Space')
c4 = Category.objects.create(name='Writer')

# Посты
p1 = Post.objects.create(author=a1, categoryType='AR', title='Episode 1', text='Эпизод1:Скрытая угроза. Неспокойные времена настали для Галактической респеблики.')
p2 = Post.objects.create(author=a2, categoryType='AR', title='Послание звезд...', text='Послание звезд. Космические перспективы человечества', text='Эта книга – тревожный сигнал, обращенный к цивилизации и призывающий ее пробудиться. Люди сбиты с толку и не понимают, кому или чему они могут доверять.')
p3 = Post.objects.create(author=a1, categoryType='NW', title='Продаю Звездные войны!', text='Чет я устал писать и проект так себе получился, продамка я права на Звездные войны мышиному дому, что может пойти не так?')

# Категории постов
p1.postCategory.add(c1, c3, c4)
p2.postCategory.add(c2, c3, c4)
p3.postCategory.add(c1, c4)

# Комментарии
Comment.objects.create(commentPost=p1, commentUser=u2, text='Когда я подхожу к двери...')
Comment.objects.create(commentPost=p3, commentUser=u2, text='Это худшая новость!')
Comment.objects.create(commentPost=p2, commentUser=u1, text='Твои книги, взрывают мозг!')
Comment.objects.create(commentPost=p3, commentUser=u1, text='О боже, что я наделал!')

# Лайки / дизлайки
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
p3.dislike()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
p2.like()
p2.like()
p2.like()
p2.like()
p1.like()
p1.like()
p1.like()

# Обновляем рейтинг авторов
a1.update_rating()
a2.update_rating()

#Имя и рейтинг лучшего пользователя
c = Author.objects.order_by('-ratingAuthor')[:1]
for i in c:
     i.ratingAuthor
     i.authorUser.username

# Выводим данные лучшего пользователя
z = Post.objects.order_by('-rating')[:1]
for i in z:
    print(i.dateCreation)
    print(i.author.authorUser.username)
    print(i.rating)
    print(i.title)
    print(i.preview())

# Получаем все комментарии к этой статье
comments = Comment.objects.filter(commentPost=z).order_by('-rating')

# Печатаем каждый комментарий
for comment in comments:
    print('Дата:', comment.dateCreation)
    print('Пользователь:', comment.commentUser.username)
    print('Рейтинг комментария:', comment.rating)
    print('Текст:', comment.text)
    print('---------------------------')