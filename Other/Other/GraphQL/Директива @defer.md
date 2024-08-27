# Директива @defer

Поддержка @defer доступна, начиная с версии Apollo Router 1.8.0. [Подробнее об этапах запуска.](https://www.apollographql.com/docs/resources/product-launch-stages)

Запросы, отправляемые на Apollo Router, могут использовать эту директиву для инкрементальной доставки данных ответа.

На текущий для реализации GraphQL API состоит из:

- Ariadne - библиотека для Python, позволяющая запускать GraphQL ASGI приложение и реализовывать GraphQL подграф;
- Apollo Server (v3) - ****GraphQL сервер с открытым исходным кодом. Совместим с любым GraphQL клиентом. Реализует GraphQL федерация подграфов; Экземпляр Apollo Server, использующий специальные расширения из [`@apollo/gateway`](https://www.apollographql.com/docs/apollo-server/using-federation/api/apollo-gateway)библиотеки
- Apollo клиенты React/Kotlin/iOS - библиотеки, которые позволяет управлять как локальными, так и удаленными данными с помощью GraphQL на клиетах

## [Что такое `@defer`?](https://www.apollographql.com/docs/router/executing-operations/defer-support/#what-is-defer)

Директива позволяет клиентскому запросу указывать наборы полей, для которых не нужно получать данные *немедленно* . Это полезно, когда некоторые поля в запросе требуют гораздо больше времени для разрешения, чем другие.

```graphql
query GetTopProducts {
  topProducts {
    id
    name
    ... @defer {
      price
    }
  }
}
```

Поддержка маршрутизатора Apollo совместима `@defer`со всеми [библиотеками подграфов, совместимыми с федерациями](https://www.apollographql.com/docs/federation/building-supergraphs/supported-subgraphs/) , поскольку логика отсрочки существует полностью внутри самого маршрутизатора.

![Untitled](%D0%94%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D0%B0%20@defer/Untitled.png)

Subgraph 1

```graphql
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Int!
}

type Query {
  topProducts: [Product!]!
}
```

Subgraph 2

```graphql
type Product @key(fields: "id") {
  id: ID!
  reviews: [Review!]!
}

type Review {
  score: Int!
}
```

Query без @defer

```graphql
query GetTopProductsAndReviews {
  topProducts { # Resolved by Products subgraph
    id
    name
    reviews {   # Resolved by Reviews subgraph
      score
    }
  }
}
```

Query с @defer

```graphql
query GetTopProductsAndDeferReviews {
  topProducts {
    id
    name
    ... @defer {
      reviews { 
        score
      }
    }
  }
}
```

В GraphQL есть директива [`@defer`](https://www.apollographql.com/docs/router/executing-operations/defer-support/#what-is-defer), позволяющая  клиентскому запросу указывать наборы полей, для которых не нужно получать данные **немедленно. Это позволяет обеспечить инкрементальную доставку данных клиенту и полезно, когда некоторые поля требуют гораздо больше времени для резолвинга, чем другие.

Пример запроса с [`@defer`](https://www.apollographql.com/docs/router/executing-operations/defer-support/#what-is-defer)

```graphql
query GetTopProducts {
  topProducts {
    id
    name
    ... @defer {
      price
    }
  }
}
```

[RFC](https://github.com/graphql/graphql-wg/blob/main/rfcs/DeferStream.md)

В Apollo директива [`@defer`](https://www.apollographql.com/docs/router/executing-operations/defer-support/#what-is-defer) доступна в Apollo Router начинася с версии 1.8.0.

Apollo Router — это настраиваемый высокопроизводительный маршрутизатор для вашего федеративного GraphQL API. ([https://www.apollographql.com/docs/router/](https://www.apollographql.com/docs/router/))

> If you have an existing federated graph that currently uses `@apollo/gateway`, you can move to the Apollo Router without changing any other part of your graph.
> 

Поддержка `@defer` Apollo Router совместима с библиотекой Ariadne, т.к. логика отсрочки находиться полностью внутри самого Apollo Router.

![Untitled](%D0%94%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D0%B0%20@defer/Untitled.png)

Необходимо исследовать возможность переезда с @apollo/gateway на Apollo Router ([Инструкция по переезду](https://www.apollographql.com/docs/router/migrating-from-gateway)) 

Документация по директиве [`@defer`](https://www.apollographql.com/docs/router/executing-operations/defer-support/#what-is-defer) в Apollo Router [https://www.apollographql.com/docs/router/executing-operations/defer-support/](https://www.apollographql.com/docs/router/executing-operations/defer-support/)

Поддержка директивы `@defer` для клиентов:

- Apollo Client - с версии `3.7.0`
- Apollo Kotlin - с версии `3.6.0`
- Apollo iOS - в процессе https://github.com/apollographql/apollo-ios/issues/2395

Пример запроса

curl --request POST \
--header 'content-type: application/json' \
--header 'accept: multipart/mixed; deferSpec=20220824, application/json' \
--url '[http://127.0.0.1:4000/](http://127.0.0.1:4000/)' \
--data '{"query":"query TopProducts($first: Int) {\n  topProducts(first: $first) {\n    inStock\n    name\n    price\n    ... @defer {\n      reviews {\n        author {\n          id\n          name\n        }\n      }\n    }\n    ... @defer {\n      shippingEstimate\n    }\n  }\n}","variables":{"first":5}}'