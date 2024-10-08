# Aggregate (Агрегат)

### Проблема

Неопределённость области применения этой системной операции.

Обновление частей бизнес-объекта напрямую может вылиться в нарушение бизнес-правил.

### Решение

Организуют доменную модель в виде набора агрегатов — графов объектов, с которыми можно работать как с единым целым. 

*Агрегат* — это **кластер доменных объектов**, с которыми можно обращаться как с еди­ным целым. Он состоит из корневой сущности и иногда одной или нескольких сущ­ностей и объектов значений. Многие бизнес-объекты моделируются в виде агрегатов. 

Например, доменная модель общего вида. 

![Untitled](../../2%20%D0%9C%D0%B8%D0%BA%D1%80%D0%BE%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B%20(MSA)/Untitled%208.png)

Многие из этих имен существительных, такие как Order, Consumer и Restaurant, являются агрегатами.

Агрегат Order и его границы показаны на рис. 5.5. Он состоит из сущности Order и одного или нескольких объектов значений, таких как OrderLineltem, Address и Paymentinformation.

![Untitled](Aggregate%20(%D0%90%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%82)/Untitled.png)

- Агрегаты разбивают доменную модель на блоки, в которых легче разобраться по отдельности.
- Агрегаты проясняют область применения операций, таких как загрузка, обновление и удаление. Операции распространяются на весь агрегат, а не на какие-то его части.
- Агрегат часто загружается из базы данных целиком, что позволяет избежать любых проблем с ленивой загрузкой. Вместе с агрегатом из базы данных удаляются все его объекты.

**Агрегаты — это границы согласованности**

Обновление целого агрегата, а не отдельных его частей решает проблемы с согла­сованностью. Операции обновления вызываются для корня агрегата, который обеспечивает соблюдение инвариантов. Кроме того, чтобы поддерживать конкурентность, корень агрегата блокируется с помощью, скажем, номера версии или блокировки уровня базы данных. Напри­мер, вместо непосредственного обновления количества единиц для определенных позиций клиент должен вызвать метод из корня агрегата Order, который следит за соблюдением таких инвариантов, как минимальная сумма заказа. Однако следует упомянуть, что этот подход не требует обновления всего агрегата в базе данных. Приложение может, к примеру, обновить поля, относящиеся к заказу Order и из­мененному объекту OrderLineltem.

**Главное — определить агрегаты**

В DDD ключевым аспектом проектирования доменной модели является опре­деление агрегатов, их границ и корней. Детали внутренней структуры агрегатов вторичны. Однако преимущества этого подхода далеко не ограничены разделением доменной модели на модули. Причина этого в том, что агрегаты обязаны придержи­ваться определенных правил.

**Правила для агрегатов**

DDD требует, чтобы агрегаты подчинялись набору правил. Это делает агрегат авто­номной единицей, способной обеспечивать соблюдение инвариантов.

**Правило 1. Ссылайтесь только на корень агрегата**

Оно требует, чтобы корневая сущность была единственной частью агрегата, на которую могут ссылаться внешние классы. Для обновления агрегата клиенту необходимо вызвать метод из его корня.

Например, сервис использует репозиторий, чтобы загрузить агрегат из базы дан­ных и получить ссылку на его корень. С помощью метода, вызываемого из корня, он обновляет агрегат. Это правило гарантирует, что агрегат способен обеспечивать соблюдение своих инвариантов.

**Правило 2. Межагрегатные ссылки должны применять первичные ключи**

Правило состоит в том, что агрегаты ссылаются друг на друга по уникальному зна­чению, например по первичному ключу, а не по объектным ссылкам. На рис. 5.6 показано, как заказ ссылается на своего заказчика с помощью consumerld, а не ссылки на объект Consumer.

![Untitled](Aggregate%20(%D0%90%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%82)/Untitled%201.png)

Данный метод имеет ряд преимуществ: 

- Агрегаты слабо связаны между собой. Это позволяет четко определить границы между ними и избежать случайного обновления не того агрегата.
- Не нужно бес­покоиться об объектных ссылках, которые выходят за пределы одного сервиса. Этот подход также упрощает сохранение состояния, поскольку агрегат является единицей хранения.
- Агрегаты становится легче хранить в базах данных NoSQL, таких как MongoDB.
- Устраняет необходимость в про­зрачной ленивой загрузке и проблемы, которые с ней связаны. Масштабирование базы данных путем сегментирования агрегатов — довольно простая задача.

**Правило 3. Одна транзакция создает или обновляет один агрегат**

Транзакция может создать или обновить только один агрегат. Это ограничение идеально подходит для микросервисной архитектуры. Оно гарантирует, что транзакция не выйдет за пределы сервиса. А также хорошо согласуется с ограниченной транзакционной моделью большинства баз данных NoSQL.
Это правило усложняет реализацию операций, которым нужно создавать или об­новлять несколько агрегатов. Но для решения этих ситуаций предназначены повествования. Каждый этап повествования создает или обновляет ровно один агрегат.

![Untitled](Aggregate%20(%D0%90%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%82)/Untitled%202.png)

Чтобы обеспечить согласованность между не­сколькими агрегатами внутри одного сервиса, мы могли бы «сжульничать» и об­новить все эти агрегаты в рамках одной транзакции. Например, одной транзакции могло бы быть достаточно для обновления агрегатов У и Z в сервисе В. Но это воз­можно только в СУРБД с развитой транзакционной моделью. Если вы применяете базу данных NoSQL, которая поддерживает только простые транзакции, у вас нет другого варианта, кроме как использовать повествования.

**Размеры агрегатов**

С одной стороны, в идеале агрегаты должны быть мелкими. Это увеличит количество одновременных запросов, которые может об­ работать ваше приложение, и улучшит масштабируемость, поскольку обновления каждого агрегата сериализуются. Это также положительно скажется на опыте взаи­модействия, так как снижается вероятность того, что два пользователя попытаются внести конфликтующие изменения в один и тот же агрегат. 

С другой стороны, агрегат — это область применения транзакции, поэтому, чтобы обеспечить атомар­ность определенного обновления, иногда стоит сделать его более крупным.

В качестве альтернативы мы могли бы сделать Order частью Consumer (рис. 5.8).

![Untitled](Aggregate%20(%D0%90%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%82)/Untitled%203.png)

Преимущества:

- Приложение может атомарно обновлять заказчика и один или несколько его заказов.

Недостатки:

- Ухудшение масштабируемости. Транзакции, обновляющие разные заказы для одного клиента, будут сериализованы.
- Если два пользователя попытаются отредактировать разные заказы одного клиента, получится конфликт.
- Препятствие декомпозиции. Бизнес-логика для заказов и клиентов должна находиться в одном сервисе, что де­лает этот сервис более объемным.

Учитывая эти проблемы, агрегаты лучше делать как можно более мелкими.

**Проектирование бизнес-логики с помощью агрегатов**

- В типичном (микро)сервисе основная часть бизнес-логики состоит из агрегатов. Остальной код принадлежит доменным сервисам и повествованиям.
- Повествования оркестрируют цепочки локальных транзакций, чтобы обеспечить согласованность данных.
- Сервисы служат точками входа в бизнес-логику и вызываются входящими адаптерами.
- Сервис использует репозиторий для извлечения агрегатов или их со­хранения в базу данных.
- Каждый репозиторий реализуется исходящим адаптером, который обращается к БД.

![Untitled](Aggregate%20(%D0%90%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%82)/Untitled%204.png)

### Преимущества

### Недостатки