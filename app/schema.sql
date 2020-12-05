drop table if exists valid_words;
drop table if exists invalid_words;
drop table if exists language_titles;
drop table if exists first_names;
drop table if exists temp_words;
create table valid_words (word text);
create table invalid_words (word text);
create table language_titles (word text);
create table first_names (word text);
create table temp_words (word text);

drop view if exists remove_names;
drop view if exists word_validation;
drop view if exists lang_validation;


create view remove_names as
select a.word as tmp_word, b.word as name
from temp_words a
join first_names b
on a.word = b.word;

create view word_validation as
select a.word as tmp_word, b.word as valid_word
from temp_words a
join valid_words b
on a.word = b.word;
