use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
select name
from store
where is_automated=1

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total)
from sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
SELECT DISTINCT store_id
FROM sale

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
SELECT store_id
FROM store
WHERE store_id NOT IN (SELECT store_id
FROM sale)

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
SELECT product.name, avg(total/quantity)
FROM sale
    LEFT JOIN product
    ON sale.product_id = product.product_id
GROUP BY product.product_id

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
SELECT name
FROM product NATURAL JOIN sale 
GROUP BY product_id
HAVING count(distinct store_id) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
SELECT name
FROM store NATURAL JOIN sale 
GROUP BY store_id
HAVING count(DISTINCT product_id) = 1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
SELECT *
FROM sale
WHERE total = (SELECT max(total)
FROM sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
SELECT date
FROM sale
GROUP BY date
ORDER BY sum(total) DESC, date ASC
LIMIT 1