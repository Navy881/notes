# Consumer-side contract test (Тестирование контрактов на стороне потребителя)

В терминологии тестирования потребительских контрактов между двумя сервисами имеется связь *«потребитель — провай­дер».* Проверка потребительского контракта — это интеграционный тест для провайдера, он позволяет убедиться в том, что API провайдера отвечает ожиданиям потребителя.

Тестирование потребительского контракта сосредоточено на проверке того, что API провайдера по своей форме отвечает ожиданиям потребителя.

Следует помнить, что тесты контрактов не занимаются тщательной проверкой бизнес-логики провайдера. За это отвечают модульные тесты.

### Проблема

Как проверить, предоставляет ли сервис API, который ожидают его клиенты?
					

### Решение

Потребительским тестам нужны и примеры ответов. Несмотря на то что основной задачей данного подхода является проверка провайдера, контракты также проверяют, соответствует ли им потребитель. Например, потребительский контракт для REST-клиента конфигурирует заглушку сервиса, которая проверяет, совпадает ли HTTP-запрос с запросом контракта, и возвращает обратно его НТТР-ответ. Тестирование обеих сторон взаимодействия позволяет убедиться в том, что потребитель и провайдер согласовали API.

### Преимущества

- 

### Недостатки

-