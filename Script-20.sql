drop table students, activity_scores;

create table if not exists students (
    id serial primary key,
    name text,
    total_score integer
);

create table if not exists activity_scores (
    student_id integer references students(id),
    activity_type text,
    score integer
);

create or replace function update_total_score(student_id_arg integer) 
returns void as $$
declare
    total integer := 0;
begin
    select coalesce(sum(score), 0) into total
    from activity_scores
    where student_id = student_id_arg;

    update students
    set total_score = total
    where id = student_id_arg;
end;
$$ language plpgsql;

create or replace function update_total_score_trigger() 
returns trigger as $$
begin
    perform update_total_score(new.student_id);
    return new;
end;
$$ language plpgsql;

create trigger after_insert_activity_score
after insert on activity_scores
for each row
execute function update_total_score_trigger();

insert into students (name, total_score) values
    ('Alex', 0),
    ('Kock', 0),
    ('KoLyan', 0),
    ('Kick', 0);

insert into activity_scores (student_id, activity_type, score) values
    (1, 'homework', 33),
    (1, 'project', 33),
    (2, 'project', 33),
    (2, 'exam', 33),
    (3,'pesnya',33),
    (3,'real pazan',33),
    (4,'network',33),
    (4, 'quiz', 33);

select * from students s 