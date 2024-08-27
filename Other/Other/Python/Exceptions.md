# Exceptions

## **KeyError - Ошибка ключа**

```python
try:
	return w_json["key"]
except KeyError:
	return 'Нет данных'
```