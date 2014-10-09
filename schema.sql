drop table if exists earthquakes;
create table earthquakes (
  id integer primary key autoincrement,
  event_name text not null,
  event_date text not null,
  location text not null,
  depth real not null,			
  magnitude real not null, 		
  latitude real not null,
  longitude real not null,
  strike real not null,
  dip real not null,
  rake real not null,
  mrr real not null,			
  mtt real not null,
  mpp real not null,
  mrt real not null,
  mrp real not null,
  mtp real not null
);