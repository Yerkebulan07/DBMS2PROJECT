DROP SEQUENCE USERS_SEQ;
CREATE SEQUENCE USERS_SEQ;
DROP TABLE users;
CREATE TABLE Users(
    id          NUMBER PRIMARY KEY,
    first_name  VARCHAR2(255),
    last_name   VARCHAR2(255),
    email       VARCHAR2(255),
    password    VARCHAR2(255),
);
SELECT * FROM Users;

DROP PACKAGE sign_pkg;


CREATE OR REPLACE PACKAGE sign_pkg
AS
    FUNCTION signInByFunction(v_email VARCHAR2, v_password VARCHAR2) RETURN VARCHAR2;
    PROCEDURE signUp(first_name users.first_name%TYPE,last_name users.last_name%TYPE,email users.email%TYPE, password users.password%TYPE);
END sign_pkg;

DROP PACKAGE BODY sign_pkg;

CREATE OR REPLACE PACKAGE BODY sign_pkg
AS
        
    FUNCTION signInByFunction(v_email VARCHAR2, v_password VARCHAR2) RETURN VARCHAR2 IS
        TYPE t_email_array IS TABLE OF users%ROWTYPE
        INDEX BY BINARY_INTEGER;
        v_email_array t_email_array;
        v_str VARCHAR2(20):='Fail';
    BEGIN
        FOR rec IN (SELECT * FROM users) LOOP
            v_email_array(rec.id) := rec;
            IF v_email_array(rec.id).email = v_email AND v_email_array(rec.id).password = v_password THEN
                v_str:='Success';           
            END IF;
        END LOOP;
        RETURN v_str;
    END;

    
    PROCEDURE signUp(first_name users.first_name%TYPE,last_name users.last_name%TYPE,email users.email%TYPE, password users.password%TYPE) IS
    BEGIN
        INSERT INTO USERS(id, first_name, last_name, email, password) VALUES(USERS_SEQ.nextval,first_name, last_name, email, password);
        COMMIT;
    END;
END sign_pkg;




DROP SEQUENCE PRODUCTS_SEQ; 
CREATE SEQUENCE PRODUCTS_SEQ;
DROP TABlE product;
CREATE TABLE PRODUCT(
    id NUMBER PRIMARY KEY,
    merchant_id NUMBER,
    name VARCHAR2(100),
    price NUMBER,
    created_at DATE DEFAULT SYSDATE,
    image_url VARCHAR2(700),
    description VARCHAR2(3000)
);

create or replace PACKAGE product_pkg AS
    PROCEDURE  addProduct(name VARCHAR2, merchant_id NUMBER, price NUMBER, image_url VARCHAR2, description VARCHAR2);
    FUNCTION deleteProduct(product_id NUMBER) RETURN VARCHAR2;
    FUNCTION updateProduct(product_id NUMBER, product_name VARCHAR2, p_price NUMBER, p_image_url VARCHAR2, p_description VARCHAR2) RETURN VARCHAR2;
END product_pkg;

create or replace PACKAGE BODY product_pkg AS
    PROCEDURE  addProduct(name VARCHAR2, merchant_id NUMBER, price NUMBER, image_url VARCHAR2, description VARCHAR2) IS    
    BEGIN
        INSERT INTO PRODUCT VALUES(PRODUCTS_SEQ.nextval, merchant_id ,name, price,sysdate, image_url,description);
    END;

    FUNCTION deleteProduct(product_id NUMBER) RETURN VARCHAR2 AS
        TYPE t_product_array IS TABLE OF product%ROWTYPE
        INDEX BY BINARY_INTEGER;
        v_product_array t_product_array;
        v_str VARCHAR2(20);
    BEGIN
        FOR rec IN (SELECT * FROM product) LOOP
            v_product_array(rec.id) := rec;
            IF v_product_array(rec.id).id = product_id THEN
                DELETE FROM product WHERE id = product_id;
                v_str:='Deleted';           
            END IF;
        END LOOP;
        RETURN v_str;
    END;

    FUNCTION updateProduct(product_id NUMBER, product_name VARCHAR2, p_price NUMBER, p_image_url VARCHAR2, p_description VARCHAR2) RETURN VARCHAR2 AS
        TYPE t_product_array IS TABLE OF product%ROWTYPE
        INDEX BY BINARY_INTEGER;
        v_product_array t_product_array;
        v_str VARCHAR2(20);
    BEGIN
        FOR rec IN (SELECT * FROM product) LOOP
            v_product_array(rec.id) := rec;
            IF v_product_array(rec.id).id = product_id THEN
                UPDATE product SET name = product_name, price = p_price, CREATED_AT = sysdate, image_url = p_image_url, description = p_description WHERE id = product_id;
                v_str:='Updated';           
            END IF;
        END LOOP;
        RETURN v_str;
    END;

END product_pkg;


DROP SEQUENCE MERCHANTS_SEQ; 
--TRUNCATE TABLE merchants; 
CREATE SEQUENCE MERCHANTS_SEQ;
DROP TABLE merchants;
CREATE TABLE merchants(
    id NUMBER PRIMARY KEY,
    merchant_name VARCHAR2(100),
    admin_id NUMBER,
    created_at DATE DEFAULT SYSDATE
);

CREATE SEQUENCE merchId;

DROP TABLE kart;
CREATE TABLE kart
        (id NUMBER,userId NUMBER, productId NUMBER
);

CREATE OR REPLACE PACKAGE kart_pkg AS
    PROCEDURE addKart(user_id users.id%TYPE, product_id product.id%TYPE);
    PROCEDURE deleteProductInKart(product_id product.id%TYPE);
END kart_pkg;
DROP sequence kart_seq;
CREATE SEQUENCE kart_seq;

CREATE OR REPLACE PACKAGE BODY kart_pkg AS
    PROCEDURE addKart(user_id users.id%TYPE, product_id product.id%TYPE) AS
        TYPE t_product_array IS TABLE OF kart%ROWTYPE
        INDEX BY BINARY_INTEGER;
        v_product_array t_product_array;
        v_str VARCHAR2(20):='null';
    BEGIN
        FOR rec IN (SELECT * FROM kart) LOOP
            v_product_array(rec.id) := rec;
            IF v_product_array(rec.id).productId = product_id and v_product_array(rec.id).userId = user_id THEN
                  v_str:='Product in kart';
            END IF;
        END LOOP;
        IF v_str <> 'Product in kart' THEN
            INSERT INTO kart(id, userId, productId) VALUES (kart_seq.nextval,user_id, product_id);
            v_str:='Added';
        END IF;
        DBMS_OUTPUT.PUT_LINE(v_str);
    END;
    PROCEDURE deleteProductInKart(product_id product.id%TYPE) AS
        CURSOR delete_cur IS SELECT * FROM kart;
        v_str VARCHAR2(20):='null';
    BEGIN
        FOR rec IN delete_cur LOOP
            IF rec.productId = product_id THEN
                DELETE FROM kart WHERE productId = product_id;
                v_str := 'Deleted';
            END IF;
        END LOOP;
        DBMS_OUTPUT.PUT_LINE(v_str);
    END;
END kart_pkg;



create or replace PACKAGE kart_price AS
    FUNCTION calculatePrice(P_USERID USERS.ID%TYPE) RETURN NUMBER;
END kart_price;

create or replace PACKAGE BODY kart_price AS
    FUNCTION calculatePrice(P_USERID USERS.ID%TYPE) RETURN NUMBER AS
        CURSOR cur1 IS SELECT PRODUCTID FROM kart WHERE USERID=P_USERID;
        CURSOR cur2(product_id NUMBER) IS SELECT price FROM product WHERE id = product_id;
        sumOfProducts NUMBER:=0;
    BEGIN
        FOR rec1 IN cur1 LOOP
            FOR rec2 IN cur2(rec1.PRODUCTID) LOOP
                sumOfProducts := sumOfProducts + rec2.price;
            END LOOP;
        END LOOP;
    RETURN sumOfProducts;
    END;
END kart_price;



CREATE TABLE ddl_log
  (
    ddl_time       DATE,
    ddl_user       VARCHAR2(15),
    object_created VARCHAR2(15),
    object_name    VARCHAR2(15),
    ddl_operation  VARCHAR2(15)
  );

CREATE OR REPLACE TRIGGER log
AFTER DDL ON SCHEMA
BEGIN
    INSERT INTO ddl_log VALUES (
    sysdate, 
    sys_context('USERENV','CURRENT_USER'), 
    ora_dict_obj_type, 
    ora_dict_obj_name, 
    ora_sysevent);
END;



/




CREATE OR REPLACE PACKAGE triggers_pkg AS 
    PROCEDURE create_log_trg(p_table_name VARCHAR2);
END triggers_pkg;

CREATE OR REPLACE PACKAGE BODY triggers_pkg AS
    PROCEDURE create_log_trg(p_table_name VARCHAR2) IS 
	create_log VARCHAR2(32767);
	create_trg VARCHAR2(32767);
    create_seq VARCHAR2(32767);

	CURSOR column_name_cur IS
		SELECT column_name, data_type, data_length 
		FROM all_tab_cols
		WHERE table_name = p_table_name;
BEGIN
	-- CREATE LOG TABLE
	create_log := 'CREATE TABLE '||p_table_name||'_LOG(ID NUMBER, OPERATION_DATE DATE, ';
	FOR i IN column_name_cur LOOP
		IF i.data_type IN ('NUMBER', 'DATE') THEN
			create_log := create_log||'OLD_'||i.column_name||' '||i.data_type||', ';
			create_log := create_log||'NEW_'||i.column_name||' '||i.data_type||', ';
		ELSE
			create_log := create_log||'OLD_'||i.column_name||' '||i.data_type||'('||i.data_length||'), ';
			create_log := create_log||'NEW_'||i.column_name||' '||i.data_type||'('||i.data_length||'), ';
		END IF;
	END LOOP;
	create_log := create_log ||'ACTION VARCHAR(255), ACTIONAUTHOR VARCHAR(255))';
	EXECUTE IMMEDIATE create_log;
  DBMS_OUTPUT.PUT_LINE('LOG TABLE CREATED');
    create_seq:= 'CREATE SEQUENCE '||p_table_name||'_LOG_SEQ';
    EXECUTE IMMEDIATE create_seq;
    
	-- CREATE LOG TRIGGER
	create_trg := 'CREATE OR REPLACE TRIGGER '||p_table_name||'_TRIGGER '||
		'AFTER INSERT OR UPDATE OR DELETE ON '||p_table_name||' FOR EACH ROW '||
		'DECLARE '||
			'PROCEDURE insert_into_LOG (p_action VARCHAR2) IS '||
			'BEGIN '||
				'INSERT INTO '||p_table_name||'_LOG VALUES ('||
					p_table_name||'_LOG_SEQ.NEXTVAL,'||
					'SYSDATE,';
					FOR i IN column_name_cur LOOP
						create_trg := create_trg||':OLD.'||i.column_name||',';
						create_trg := create_trg||':NEW.'||i.column_name||',';
					END LOOP;
					create_trg := create_trg||
					'p_action,'||
					'USER'||
				');'||
			'END;'||
		'BEGIN '||
			'IF inserting THEN '||
				'insert_into_log(''INSERT'');'||
			'ELSIF deleting THEN '||
				'insert_into_log(''DELETE'');'||
			'ELSIF updating THEN '||
				'insert_into_log(''UPDATE'');'||
			'END IF;'||
		'END;';
	EXECUTE IMMEDIATE create_trg;
  DBMS_OUTPUT.PUT_LINE('LOG TRIGGER CREATED');
  END;
END triggers_pkg;



select * from product;

BEGIN
    kart_pkg.addKart(5,2);
    product_pkg.
END;







