#-----------------------------------------------------------------------------------Section dealing with Tag information
CREATE_TAG_RAW_TABLE = '''
                        CREATE TABLE stackoverflow_tags_info (
                            tag_record_id PRIMARY KEY BIGSERIAL, 
                            tag_name TEXT,
                            tag_count INT,
                            action_tag  BOOLEAN,
                            moderator_tag BOOLEAN,
                            has_synonyms BOOLEAN,
                            record_date DATE NOT NULL DEFAULT (SELECT CURRENT_DATE - INTEGER '1' )
                        );
                    '''

INSERT_TAG_RAW = '''
                    INSERT INTO stackoverflow_tags_info(tag_name, tag_count, action_tag, moderator_tag, has_synonyms, record_date) VALUES ('{}','{}','{}','{}','{}','{}');
                '''

#-----------------------------------------------------------------------------------Section dealing with Answers information
CREATE_ANSWERS_RAW_TABLE = '''
                        CREATE TABLE stackoverflow_answers_info (
                            answer_record_id PRIMARY KEY BIGSERIAL, 
                            answer_id DOUBLE,
                            answer_question_id DOUBLE,
                            answer_owner DOUBLE,
                            answer_acceptance_status BOOLEAN,
                            answer_score INT,
                            answer_creation_datetime DATETIME,
                            answer_last_activity_datetime DATETIME,
                            answer_downvote_count INT,
                            answer_upvote_cout INT,
                            answer_lock_status BOOLEAN,
                            answer_content_license TEXT,
                            record_date DATE NOT NULL DEFAULT (SELECT CURRENT_DATE - INTEGER '1' )
                        );
                    '''

INSERT_ANSWER_RAW = '''
                    INSERT INTO stackoverflow_answers_info(answer_id, question_id, , answer_owner, answer_acceptance_status, answer_score, answer_creation_datetime, answer_last_activity_datetime, answer_downvote_count, answer_upvote_count, answer_lock_status, answer_content_license, record_date) 
                    VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                 '''

#-----------------------------------------------------------------------------------Section dealing with Questions information
CREATE_QUESTIONS_RAW_TABLE = '''
                        CREATE TABLE stackoverflow_questions_info (
                            question_record_id PRIMARY KEY BIGSERIAL, 
                            question_id DOUBLE,
                            question_title TEXT,
                            question_creation_datetime DATETIME,
                            question_is_answered BOOLEAN,
                            question_owner DOUBLE,
                            question_score INT,
                            question_tags TEXT[],
                            question_view_count INT,
                            question_acceptance_answer_id DOUBLE,
                            question_last_activity_datetime DATETIME,
                            question_last_edit_datetime DATETIME,
                            question_answer_cout INT,
                            question_content_license TEXT,
                            question_link TEXT,
                            record_date DATE NOT NULL DEFAULT (SELECT CURRENT_DATE - INTEGER '1' )
                        );
                    '''

INSERT_QUESTION_RAW = '''
                      INSERT INTO stackoverflow_questions_info( question_id, question_title, question_creation_datetime, question_is_answered, question_owner, question_score, question_tags,  question_view_count, question_acceptance_answer_id, question_last_activity_datetime, question_last_edit_datetime, question_answer_cout, question_content_license, question_link, record_date )
                      VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                      '''