

DROP TABLE USERS;
DROP SEQUENCE USERS_SEQ;
/* */
CREATE TABLE USERS (
    id          NUMBER PRIMARY KEY,
    email       VARCHAR2(255) NOT NULL UNIQUE,
    password    VARCHAR2(510) NOT NULL,
    first_name  VARCHAR2(255) NOT NULL,
    last_name   VARCHAR2(255) 
);
CREATE SEQUENCE USERS_SEQ;
/* */
SELECT * FROM USERS;

TRUNCATE TABLE USERS; 

CREATE OR REPLACE PROCEDURE insert_into_users(v_column VARCHAR, email VARCHAR, password VARCHAR, first_name VARCHAR, last_name VARCHAR) IS
BEGIN
    INSERT INTO USERS(id, v_columns) VALUES(USER_SEQ.nextval, email, password, first_name, last_name);
END;





/* SQL> desc users;

 Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 ID                                        NOT NULL NUMBER(38)
 NAME                                      NOT NULL VARCHAR2(255)
 PASSWORD                                  NOT NULL VARCHAR2(4000)
 FIRST_NAME                                NOT NULL VARCHAR2(255)
 LAST_NAME                                 NOT NULL VARCHAR2(255)

*/

-- INSERT INTO USERS VALUES(3, 'jadeben', 'password', 'Jade', 'Ben');
