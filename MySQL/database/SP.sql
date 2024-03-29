USE MYCHAT;

-- procedure đăng nhập, trả về 0 nếu sai thông tin, 1 nếu thành công
DELIMITER //
CREATE PROCEDURE SIGN_IN(usrName VARCHAR(20), pass VARCHAR(20), OUT res INT)
BEGIN
    IF EXISTS (SELECT * FROM AL_USER WHERE AL_USERNAME = usrName AND AL_PASSWORD = pass)
		THEN SET res = 1;
	ELSE SET RES = 0;
    END IF;
END//
DELIMITER ;

CALL SIGN_IN('alice', '123456', @v);
select @v;

-- procedure lấy kết quả từ sign in do python chỉ bắt được kết quả của lệnh select
DELIMITER //

CREATE PROCEDURE SIGN_IN_WRAP(usrName VARCHAR(20), pass VARCHAR(20), OUT res INT)
BEGIN
	CALL SIGN_IN(usrName, pass, res);
    SELECT res;
END//

DELIMITER ;

-- procedure tạo acc
DELIMITER //
CREATE PROCEDURE CREATE_ACC
(
	usrName VARCHAR(20),
    pass VARCHAR(20),
    if_name NVARCHAR(30),
    email VARCHAR(40),
    phone VARCHAR(11),
    stt VARCHAR(15)
)
BEGIN
	INSERT INTO AL_USER (AL_USERNAME, AL_PASSWORD, AL_NAME, AL_EMAIL, AL_PHONE, AL_STATUS) VALUES (usrName, pass, if_name, email, phone, stt);
END//
DELIMITER ;

-- pro kiểm tra username đã tồn tại hay chưa
DELIMITER //

CREATE PROCEDURE CHECK_USRNAME
(
	usrName VARCHAR(20),
    OUT res INT
)
BEGIN
	IF EXISTS (SELECT * FROM AL_USER WHERE AL_USERNAME = usrName) THEN SET res = 1;
    ELSE SET res = 0;
    END IF;
END//

DELIMITER ;

-- proc bắt kết quả của proc kiểm tra user
DELIMITER //

CREATE PROCEDURE CHECK_USRNAME_WRAP(usrName VARCHAR(20), OUT res INT)
BEGIN
	CALL CHECK_USRNAME(usrName, res);
    SELECT res;
END//

DELIMITER ;

call CHECK_USRNAME_WRAP ('ali', @v);


-- pro xóa tài khoản
DELIMITER //

CREATE PROCEDURE DROP_USR
(
	usrName VARCHAR(20)
)
BEGIN
	DELETE FROM AL_USER WHERE AL_USERNAME = usrName;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UPDATE_STT (usrName VARCHAR(20), stt VARCHAR(15))
BEGIN
	UPDATE AL_USER SET AL_STATUS = stt WHERE AL_USERNAME = usrName;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE SEND_FRRQ
(
	usrFrom VARCHAR(20),
    usrTo VARCHAR(20),
    mes NVARCHAR(100)
)
BEGIN
	DECLARE FromId INT DEFAULT 0;
    DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO FromId FROM AL_USER WHERE AL_USERNAME = usrFrom;
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrTo;
    
	INSERT INTO AL_FR_REQUEST (AL_FROM, AL_TO, AL_CONTENT, AL_DATE_CREATE, AL_STATUS)
					   VALUES (FromId , ToId , mes       , NOW()     , 'waiting');
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE ACCEPT_FRRQ
(
	usrFrom VARCHAR(20),
    usrTo VARCHAR(20)
)
BEGIN
	DECLARE FromId INT DEFAULT 0;
    DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO FromId FROM AL_USER WHERE AL_USERNAME = usrFrom;
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrTo;
    
    INSERT INTO AL_RELA (AL_USER1, AL_USER2, AL_RELA) VALUES (FromId, ToId, 'friend');
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UPDATE_FRRQ(usrFrom VARCHAR(20), usrTo VARCHAR(20), stt varchar(20))
begin
	DECLARE FromId INT DEFAULT 0;
    DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO FromId FROM AL_USER WHERE AL_USERNAME = usrFrom;
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrTo;
    
	UPDATE AL_FR_REQUEST
    SET AL_STATUS = stt
    WHERE AL_FROM = FromId AND AL_TO = ToId;
end//

DELIMITER ;

call UPDATE_FRRQ ('mel', 'ali', 'accept');

DELIMITER //

CREATE PROCEDURE CHECK_RELA
(
	usrFrom VARCHAR(20),
    usrTo VARCHAR(20),
    OUT res INT
)
BEGIN
	DECLARE FromId INT DEFAULT 0;
    DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO FromId FROM AL_USER WHERE AL_USERNAME = usrFrom;
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrTo;
    
    IF EXISTS (SELECT * FROM AL_RELA WHERE (AL_USER1 = FromId AND AL_USER2 = ToId) OR (AL_USER1 = ToId AND AL_USER2 = FromId))
		THEN SET res = 1;
	ELSE SET res = 0;
    END IF;
    SELECT res;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE GET_USR_INFOR
(
	usrName VARCHAR(20),
    OUT alName NVARCHAR(40),
    OUT alEmail VARCHAR(30),
    OUT alPhone VARCHAR(11),
    OUT alStt VARCHAR(20)
)
BEGIN
	SELECT AL_NAME INTO alName FROM AL_USER WHERE AL_USERNAME = usrName;
    SELECT AL_EMAIL INTO alEmail FROM AL_USER WHERE AL_USERNAME = usrName;
    SELECT AL_PHONE INTO alPhone FROM AL_USER WHERE AL_USERNAME = usrName;
    SELECT AL_STATUS INTO alStt FROM AL_USER WHERE AL_USERNAME = usrName;
    SELECT alName, alEmail, alPhone, alStt;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE SHOW_FRRQ
(
	usrName VARCHAR(20),
    out res int
)
BEGIN
	SELECT FR.AL_RQID, USRFR.AL_USERNAME, FR.AL_CONTENT, FR.AL_DATE_CREATE
    FROM AL_FR_REQUEST FR, AL_USER USRTO, AL_USER USRFR
    WHERE FR.AL_TO = USRTO.AL_USERID AND USRTO.AL_USERNAME = usrName
    AND FR.AL_STATUS = 'waiting' AND USRFR.AL_USERID = FR.AL_FROM;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE CHAT_USR(usrFrom varchar(20), usrTo varchar(20), mess varchar(1000))
begin
	DECLARE FromId INT DEFAULT 0;
    DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO FromId FROM AL_USER WHERE AL_USERNAME = usrFrom;
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrTo;
    
	INSERT INTO AL_MESS (AL_FROM, AL_TO, AL_CONTENT, AL_DATE, AL_STATUS, AL_TYPE)
    VALUES (FromId, ToId, mess, NOW(), 'send', 'user');
end//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE LOAD_OLD_MSR(usrFrom varchar(20), usrTo varchar(20))
BEGIN
	DECLARE FromId INT DEFAULT 0;
    DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO FromId FROM AL_USER WHERE AL_USERNAME = usrFrom;
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrTo;
    
    SELECT USR.AL_USERNAME, AL_CONTENT, AL_DATE
    FROM AL_MESS M, AL_USER USR
    WHERE ((AL_FROM = FromId AND AL_TO = ToId) OR (AL_FROM = ToId AND AL_TO = FromId))
    AND M.AL_FROM = USR.AL_USERID;
    
    UPDATE AL_MESS
    SET AL_STATUS = 'seen'
    WHERE (AL_FROM = FromId AND AL_TO = ToId) OR (AL_FROM = ToId AND AL_TO = FromId);
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE CHECK_NEWMSG(usrName VARCHAR(20), res int)
BEGIN
	DECLARE ToId INT DEFAULT 0;
    
    SELECT AL_USERID INTO ToId FROM AL_USER WHERE AL_USERNAME = usrName;
    
    SELECT USR.AL_USERNAME, AL_CONTENT, AL_DATE
    FROM AL_MESS M, AL_USER USR
    WHERE AL_TO = ToId AND M.AL_STATUS = 'send' AND M.AL_TYPE = 'user'
    AND M.AL_FROM = USR.AL_USERID;
    
	UPDATE AL_MESS
    SET AL_STATUS = 'seen'
    WHERE AL_TO;
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE SHOW_FRL(usrName VARCHAR(20), res INT)
BEGIN
	SELECT USR.AL_USERNAME, USR.AL_NAME, USR.AL_STATUS
    FROM AL_RELA RL, AL_USER USR
    WHERE 
END//
DELIMITER ;