select ticket_flights.fare_conditions, ticket_flights.flight_id, ticket_flights.amount, tickets.passenger_name
from bookings.ticket_flights
inner join bookings.tickets on ticket_flights.ticket_no = tickets.ticket_no;

select ticket_no, book_ref, passenger_name, passenger_id, null as fare_conditions 
from bookings.tickets
union
select ticket_no, null as passenger_name, null as flight_id, null as book_ref, fare_conditions
from bookings.ticket_flights

select * from bookings.seats
where aircraft_code ~ '^[0-9]+$'
  and cast(aircraft_code as int) > 500
order by aircraft_code desc
limit 20;

select ticket_flights.fare_conditions, ticket_flights.flight_id, sum(ticket_flights.amount), tickets.passenger_name
from bookings.ticket_flights 
inner join bookings.tickets on ticket_flights.ticket_no = tickets.ticket_no
group by ticket_flights.fare_conditions, ticket_flights.flight_id, tickets.passenger_name;

select 
    b.book_ref, 
    b.book_date, 
    b.total_amount,
    t.ticket_no, 
    t.passenger_id, 
    t.passenger_name, 
    t.contact_data,
    bp.flight_id, 
    bp.boarding_no, 
    bp.seat_no
from 
    bookings.bookings b
left join 
    bookings.tickets t
    on b.book_ref = t.book_ref
left join 
    bookings.boarding_passes bp 
    on bp.ticket_no = t.ticket_no  

drop view if exists seats_view;

create view seats_view as
select *
from bookings.seats
where aircraft_code ~ '^[0-9]+$'
  and cast(aircraft_code as integer) > 300
order by aircraft_code asc
limit 50;

select * from seats_view