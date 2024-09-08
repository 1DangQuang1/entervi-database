use alibaba_db;
select	 * from product_data;
select * from company_data;
SET SQL_SAFE_UPDATES = 0;

WITH DUPLICATE AS(
	SELECT company_name, link, company_id,
    row_number() over ( partition by company_name, link order by company_id) as RN
    from company_data
)
delete from company_data 
where company_id in (select company_id from DUPLICATE where RN>1);


update company_data 
set company_name = trim(company_name)
where (company_name like ' %' or company_name like '% ') and company_name is not null;

UPDATE company_data
SET rating = IF(rating = '', 'N/A', rating),
    response_time = IF(response_time = '', 'N/A', response_time),
    main_products = IF(main_products = '', 'N/A', main_products),
    capacity_info = IF(capacity_info = '', 'N/A', capacity_info),
    product_1_price = IF(product_1_price = '', 'N/A', product_1_price),
    product_1_moq = IF(product_1_moq = '', 'N/A', product_1_moq),
    product_1_img = IF(product_1_img = '', 'N/A', product_1_img),
    product_2_price = IF(product_2_price = '', 'N/A', product_2_price),
    product_2_moq = IF(product_2_moq = '', 'N/A', product_2_moq),
    product_2_img = IF(product_2_img = '', 'N/A', product_2_img),
    view_images = IF(view_images = '', 'N/A', view_images)
;


SET SQL_SAFE_UPDATES = 1;
