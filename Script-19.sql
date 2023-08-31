drop table students, activity_scores;

create table students (
  id serial primary key,
  name text,
  total_score integer,
  scholarship integer
);

create table activity_scores (
  student_id integer references students(id),
  activity_type text,
  score integer
);

create or replace function calculate_scholarship(student_total integer) 
returns integer as $$
declare
  scholarship_amount integer;
begin
  if student_total >= 90 then
    scholarship_amount := 1000;
  elsif student_total >= 80 then
    scholarship_amount := 500;
  else
    scholarship_amount := 0;
  end if;

  return scholarship_amount;
end;
$$ language plpgsql;

create or replace function update_scholarship_trigger() 
returns trigger as $$
begin
  if tg_op = 'insert' or tg_op = 'update' then
    update students
    set total_score = (select sum(score) from activity_scores where student_id = new.student_id)
    where id = new.student_id;
    update students
    set scholarship = calculate_scholarship(total_score)
    where id = new.student_id;
  end if;

  return new;
end;
$$ language plpgsql;

create trigger update_scholarship_trigger
after insert or update on activity_scores
for each row
execute function update_scholarship_trigger();

create or replace function reset_total_score_trigger() 
returns trigger as $$
begin
  update students
  set total_score = total_score - old.score + new.score
  where id = old.student_id;

  return new;
end;
$$ language plpgsql;

create trigger reset_total_score_trigger
after update on activity_scores
for each row
execute function reset_total_score_trigger();

insert into students (name, id) values 
  ('john doe',1),
  ('jane smith',2),
  ('alex johnson',3),
  ('emily brown',4),
  ('michael lee',5);

insert into activity_scores (student_id, activity_type, score) values 
  (1, 'project', -25),
  (2, 'presentation', 2),
  (3, 'essay', 0),
  (4, 'lab report', 0),
  (5, 'discussion', 4);

select * from activity_scores;

select * from students s
