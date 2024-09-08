use alibaba_db;
SET SQL_SAFE_UPDATES = 0;
WITH DUPLICATE AS (
	SELECT id, product_link, product_name, 
    row_number() over (partition by product_link, product_name order by id) as RN 
    from product_data
)
delete from product_data
where id in ( select id from DUPLICATE where RN > 1 );

UPDATE product_data
SET product_price = 0
WHERE product_price IS NULL;
