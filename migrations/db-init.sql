create type category as enum (
    'gratitude',
    'suggestion',
    'claim'
);

create table responses (
    id bigint unique,
    original_text text,
    resp_category category
);
