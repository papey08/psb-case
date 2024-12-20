create type category as enum (
    'gratitude',
    'suggestion',
    'claim'
);

create table responses (
    id bigint unique,
    original_text text,
    resp_category category,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table tg_user (
    id serial primary key,
    tg_username varchar(256) unique,
    gratitude_id int default 0,
    suggestion_id int default 0,
    claim_id int default 0
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON responses
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE VIEW gratitude_v AS
SELECT
    ROW_NUMBER() OVER (ORDER BY responses.updated_at DESC) AS id,
    responses.original_text as original_text,
    id as response_id
FROM responses where resp_category='gratitude';

CREATE VIEW suggestion_v AS
SELECT
    ROW_NUMBER() OVER (ORDER BY responses.updated_at DESC) AS id,
    responses.original_text as original_text,
    id as response_id
FROM responses where resp_category='suggestion';

CREATE VIEW claim_v AS
SELECT
    ROW_NUMBER() OVER (ORDER BY responses.updated_at DESC) AS id,
    responses.original_text as original_text,
    id as response_id
FROM responses where resp_category='claim';