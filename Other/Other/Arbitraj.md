# Arbitraj

**Терминология**

- **Арбитраж криптовалюты** - это несколько логически связанных сделок, направленных на извлечение прибыли из разницы в ценах на одинаковые или связанные активы в одно и то же время на разных биржах или на разных рынках одной и той же платформы. Простыми словами - это покупка актива на бирже, где на него спрос (соответственно и цена) ниже, а продажа там, где выше.
- **P2P** (от англ. peer-to-peer, person-to-person — от человека к человеку, от равного к равному) - это денежные переводы от одного человека напрямую к другому.
- **Стакан P2P** - таблица лимитных заявок на покупку и продажу конкретных криптовалют. Каждая заявка содержит цену и количество токенов на покупку и продажу.
- **Спред** - разница курса между ценой покупки и ценой продажи.
- **Депозит** - это капитал, которым вы перегоняете.
- **Объявление (ордер)** — заявка на покупку или продажу криптовалюты.
- режим расчёта **Т+2** - это значит, что акцию вы покупаете сейчас, а расчёты по данной сделке произойдут через 2 рабочих дня

**Binance**

[https://www.binance.com/ru/markets/coinInfo-](https://www.binance.com/ru/markets/coinInfo-)

GET wss://stream.binance.com/stream

```json
{
  "stream": "!ticker_4h@arr@3000ms",
  "data": [
		{
		  "e": "1hTicker",    // Event type
		  "E": 123456789,     // Event time
		  "s": "BNBBTC",      // Symbol
		  "p": "0.0015",      // Price change
		  "P": "250.00",      // Price change percent
		  "o": "0.0010",      // Open price
		  "h": "0.0025",      // High price
		  "l": "0.0010",      // Low price
		  "c": "0.0025",      // Last price
		  "w": "0.0018",      // Weighted average price
		  "v": "10000",       // Total traded base asset volume
		  "q": "18",          // Total traded quote asset volume
		  "O": 0,             // Statistics open time
		  "C": 86400000,      // Statistics close time
		  "F": 0,             // First trade ID
		  "L": 18150,         // Last trade Id
		  "n": 18151          // Total number of trades
		}
  ]
}
```

**Coinbase**

[https://www.coinbase.com/explore](https://www.coinbase.com/explore)

curl "[https://www.coinbase.com/api/v2/assets/search?base=RUB&country=RU&filter=listed&include_prices=true&limit=7&order=asc&page=1&query=&resolution=day&sort=rank](https://www.coinbase.com/api/v2/assets/search?base=RUB&country=RU&filter=listed&include_prices=true&limit=7&order=asc&page=1&query=&resolution=day&sort=rank)" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0" -H "Accept: */*" -H "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3" -H "Accept-Encoding: gzip, deflate, br" -H "Referer: [https://www.coinbase.com/explore](https://www.coinbase.com/explore)" -H "credentials: same-origin" -H "Content-Type: application/json" -H "X-CB-Device-ID: d01edb5b-dcc2-4e39-964a-8fa5eb19eeb2" -H "X-CB-Is-Logged-In: false" -H "X-CB-Pagekey: price" -H "X-CB-Platform: web" -H "X-CB-Project-Name: consumer" -H "X-CB-Session-UUID: f591f22d-7477-4e3e-ae91-73548f0ec792" -H "X-CB-Version-Name: 56388e23ca0e5b958ff7bdcce94152101bb15a5d" -H "DNT: 1" -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" -H "Connection: keep-alive" -H "Cookie: cb_dm=9ee5ca39-184a-4836-9058-9b33a75a2b39; coinbase_currency=RUB; coinbase_locale=en; coinbase_device_id=d01edb5b-dcc2-4e39-964a-8fa5eb19eeb2; _ga_90YJL6R0KZ=GS1.1.1661297040.2.1.1661297074.26.0.0; _ga=GA1.1.1568171179.1661294938; __cf_bm=rwyT6556hKd25nGJJQxxlDi0Ug.MhMf.KntsgQQS31I-1661297079-0-AUs38sCspDusHQvETa5suiq7UsBv76BplgpcSD8UjGASwyrugApKgU2Ab4PeABOgRjEcQv1wjh3sUYq21yqvuN8="

```json
{
  "pagination": {
    "ending_before": null,
    "starting_after": null,
    "previous_ending_before": null,
    "next_starting_after": "63062039-7afb-56ff-8e19-5e3215dc404a",
    "limit": 7,
    "order": "asc",
    "previous_uri": null,
    "next_uri": "/api/v2/assets/search?base=RUB&country=RU&filter=listed&include_prices=true&limit=7&order=asc&page=2&query=&resolution=day&sort=rank&starting_after=63062039-7afb-56ff-8e19-5e3215dc404a&timestamp=1661296326674",
    "page": 1,
    "total_pages": 31,
    "total": 215,
    "timestamp": "1661296326674"
  },
  "data": [
    {
      "id": "5b71fc48-3dd3-540c-809b-f8c94d0e68b5",
      "symbol": "BTC",
      "name": "Bitcoin",
      "slug": "bitcoin",
      "color": "#F7931A",
      "image_url": "https://dynamic-assets.coinbase.com/e785e0181f1a23a30d9476038d9be91e9f6c63959b538eabbc51a1abc8898940383291eede695c3b8dfaa1829a9b57f5a2d0a16b0523580346c6b8fab67af14b/asset_icons/b57ac673f06a4b0338a596817eb0a50ce16e2059f327dc117744449a47915cb2.png",
      "listed": true,
      "launched_at": "9 years ago",
      "description": "The world’s first cryptocurrency, Bitcoin is stored and exchanged securely on the internet through a digital ledger known as a blockchain. Bitcoins are divisible into smaller units known as satoshis — each satoshi is worth 0.00000001 bitcoin.",
      "exponent": 8,
      "unit_price_scale": 2,
      "transaction_unit_price_scale": 2,
      "address_regex": "^([13][a-km-zA-HJ-NP-Z1-9]{25,34})|^(bc1[qzry9x8gf2tvdw0s3jn54khce6mua7l]([qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}|[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{58}))$",
      "resource_urls": [
        {
          "type": "white_paper",
          "icon_url": "https://www.coinbase.com/assets/resource_types/white_paper-1129060acdfdb91628bf872c279435c9ce93245a40f0227d98f0aa0a93548cb4.png",
          "title": "Whitepaper",
          "link": "https://bitcoin.org/bitcoin.pdf"
        },
        {
          "type": "website",
          "icon_url": "https://www.coinbase.com/assets/resource_types/globe-58759be91aea7a349aff0799b2cba4e93028c83ebb77ca73fd18aba31050fc33.png",
          "title": "Official website",
          "link": "https://bitcoin.org"
        }
      ],
      "base": "BTC",
      "currency": "RUB",
      "rank": 1,
      "market_cap": "23381445607497.27",
      "percent_change": -0.041145712834960685,
      "latest": "1223422.2743987974126056",
      "volume_24h": "1811964517374.20",
      "circulating_supply": "19130043.0",
      "tradable_on_wallet": false,
      "latest_price": {
        "amount": {
          "amount": "1223422.2743987974126056",
          "currency": "RUB",
          "scale": "2"
        },
        "timestamp": "2022-08-23T23:24:39+00:00",
        "percent_change": {
          "hour": -0.05819390521133646,
          "day": -0.041145712834960685,
          "week": -0.16623279565790858,
          "month": -0.06250102614992503,
          "year": -0.6665563902562289,
          "all": 353.7995691540838
        }
      },
      "prices": [
        "1297428.3630681601",
        "1293978.44795364"
      ]
    }
  ]
}
```