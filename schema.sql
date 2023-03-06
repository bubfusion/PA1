DROP DATABASE photoshare;

CREATE DATABASE IF NOT EXISTS photoshare;
USE photoshare;
DROP TABLE IF EXISTS Pictures CASCADE;
DROP TABLE IF EXISTS Users CASCADE;

CREATE DATABASE IF NOT EXISTS photoshare;
USE photoshare;
DROP TABLE IF EXISTS Pictures CASCADE;
DROP TABLE IF EXISTS Users CASCADE;


CREATE TABLE Users (
    user_id int4  AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    hometown VARCHAR(35),
    gender VARCHAR(50),
    PRIMARY KEY(user_id)
);

CREATE TABLE Albums(
    album_id int4 AUTO_INCREMENT,
    user_id int4,
    creation_date DATE,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(album_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Pictures
(
    picture_id int4  AUTO_INCREMENT,
    user_id int4,
    imgdata longblob ,
    caption VARCHAR(255),
    album_id int4 NOT NULL,
    INDEX upid_idx (user_id),
    PRIMARY KEY (picture_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE CASCADE
);

CREATE TABLE Comments(
    commentid int4  AUTO_INCREMENT,
    date DATE,
    text VARCHAR(255),
    user_id int4 NOT NULL,
    picture_id int4 NOT NULL,
    PRIMARY KEY(commentid),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (picture_id) REFERENCES Pictures(picture_id) ON DELETE CASCADE
);

CREATE TABLE Friends(
    user_id1 int4,
    user_id2 int4,
    CHECK(user_id1 <> user_id2),
    FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE CASCADE,
	PRIMARY KEY(user_id1, user_id2)
);

CREATE TABLE Likes(
    picture_id int4,
    user_id int4,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (picture_id) REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    PRIMARY KEY(user_id, picture_id)
);

CREATE TABLE Tags(
	tag_id int4  AUTO_INCREMENT, 
    name VARCHAR(100),
    PRIMARY KEY(tag_id)
);

CREATE TABLE Tagged(
	picture_id int4,
    tag_id int4,
    FOREIGN KEY (picture_id) REFERENCES Pictures(picture_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id),
    PRIMARY KEY(picture_id, tag_id)
);


DELIMITER $$
CREATE TRIGGER commentingOwnPost BEFORE INSERT ON Comments
FOR EACH ROW
BEGIN
   SET @picture_user_id = (SELECT user_id FROM Pictures WHERE picture_id = NEW.picture_id);
   IF NEW.user_id = @picture_user_id THEN
		CALL RAISE_APPLICATION_ERROR(-20999, "Can't comment on own post!");
   END IF;
END$$
DELIMITER ;


INSERT INTO Users (email, password, dob, first_name) VALUES ('test@bu.edu', 'test', STR_TO_DATE('12-04-2002','%m-%d-%Y'), 'Brenton');
INSERT INTO Users (email, password, dob, first_name) VALUES ('test2@bu.edu', 'test', STR_TO_DATE('12-04-2002','%m-%d-%Y'), 'Brenton');