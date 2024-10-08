# Service instance per VM (Развёртывание сервиса в виде ВМ)

### Проблема

Как упаковать и развернуть сервис?

Представьте, что вам нужно развернуть сервис, но на этот раз в AWS ЕС2. Для этого вы можете создать и настроить сервер ЕС2 и скопиро­вать на него исполняемый файл или архив WAR. В этом случае вы бы получили определенные преимущества от использования облака, но у этого подхода те же не­ достатки, что и у развертывания сервисов с помощью пакетов для отдельных языков. Более современным решени­ем будет упаковать сервис в формате AMI (Amazon Machine Image). Каждый экземпляр сервиса будет представлен сервером ЕС2, созданным из этого AMI пакета. Серверами ЕС2 обычно управляет группа автомасштабирования AWS, которая пытается поддерживать желаемое количество работоспособных экземпляров.

### Решение

Упакуйте сервис в образ виртуальной машины и разверните каждый экземпляр сервиса как отдельную виртуальную машину.

Равёртывает в промышленной среде сервисы, упакованные в виде образов для виртуальной машины. Каждый экземпляр сервиса является отдельном виртуальной машиной (ВМ).

Образ виртуальной машины собирается в процессе развертывания сервиса. Процесс развертывания запускает сборщик образов ВМ, чтобы создать образ с кодом сервиса и тем программным обеспечением, которое ему нужно для работы. В случае с проектом FTGO сборщик ВМ устанавливает JDK и исполняемый JAR-файл сервиса. Он также настраивает виртуальную ма­шину для запуска приложения с помощью системы инициализации Linux, такой как Upstart.

![Untitled](Service%20instance%20per%20VM%20(%D0%A0%D0%B0%D0%B7%D0%B2%D0%B5%CC%88%D1%80%D1%82%D1%8B%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0%20%D0%B2/Untitled.png)

Существует множество инструментов, с помощью которых процесс развертыва­ния может собрать образ ВМ. Одна из первых утилит для создания образов ЕС2 AMI называлась Aminator, она была создана компанией Netflix для развертывания видеовещательного сервиса на AWS ([https://github.com/Netflix/aminator](https://github.com/Netflix/aminator)). Более совре­менный сборщик образов ВМ — Packer. В отличие от Aminator он поддерживает различные технологии виртуализации, включая ЕС2, Digital Ocean, Virtual Box и VMware ([www.packer.io](http://www.packer.io/)). Для его использования нужно написать конфигурацион­ный файл, в котором указать базовый образ и набор средств подготовки для уста­новки и конфигурации AMI.

Elastic Beanstalk - решения для развёртывания сервисов с помощью ВМ.

### Преимущества

- Образ ВМ инкапсулирует стек технологий.
Образ ВМ содержит сервис вместе со всеми его зависимостями. Это избавляет от необходимости устанавливать и конфигурировать ПО, нужное для работы сервиса, что может спасти от потен­циальных ошибок. После упаковки в образ ВМ сервис становится своеобразным черным ящиком, который инкапсулирует свой стек технологий. Такой образ можно развертывать где угодно, не внося изменений. API для развертывания сервиса ста­новится интерфейсом для управления ВМ, а сам процесс существенно упрощается и становится более надежным.
- Экземпляры сервиса изолированы.
Экземпляры сервисов выполняются в полной изоляции. Это, в конце концов, основная цель данной технологии. Каждая ВМ имеет фиксированное количество процессорного времени и памяти, что не позволяет ей занимать ресурсы других сервисов.
- Используется зрелая облачная инфраструктура.
Возможность задействования зрелой, высокоавтоматизированной облач­ной инфраструктуры. Публичные облака, например AWS, пытаются запланировать работу ВМ на физических серверах так, чтобы избежать перегрузок. Они также предоставляют полезные возможности — автомасштабирование и балансирование трафика между ВМ. Например, Elastic Load Balancer и группы автомасштабирования.
- Легко масштабировать сервис, увеличивая количество экземпляров. Amazon Autoscaling Groups могут делать это автоматически в зависимости от нагрузки.

### Недостатки

- Менее эффективно используются ресурсы.
Каждый экземпляр сервиса тянет за собой целую виртуальную машину, включая ее операционную систему. Более того, публичные платформы IaaS обычно предлагают ограниченный набор размеров ВМ, поэтому ваши ресурсы, скорее всего, будут использоваться не на полную мощь. Это в меньшей мере относится к сервисам,
основанным на Java, поскольку они относительно тяжеловесны. Но развертывание таким образом легковесных сервисов, написанных на NodeJS или GoLang, может оказаться неэффективным.
- Развертывание протекает довольно медленно.
Сборка образа ВМ обычно исчисляется минутами из-за размера виртуальной маши­ны. Для этого по сети нужно передать довольно много данных. Создание экземпляра ВМ из образа тоже требует некоторого времени — опять-таки из-за количества данных, перемещаемых по сети. К тому же операционная система, выполняемая внутри ВМ, загружается не сразу, хотя понятие *«медленно»* является относительным. Процесс может растянуться на минуты, но это все равно быстрее, чем традиционное развертывание. Вместе с тем он значительно уступает по скорости более легковес­ным шаблонам.
- Требуются дополнительные расходы на системное администрирование.
Вы сами отвечаете за обновление операционной системы и среды выполнения. Системное администрирование может показаться неотъемлемой частью разверты­вания ПО, но есть бессерверное развертывание, в котором этот аспект полностью искоренен.