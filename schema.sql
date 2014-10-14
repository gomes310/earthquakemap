drop table if exists earthquakes;
create table earthquakes (
  id integer primary key autoincrement,
  event_name text not null,		 		
  latitude real not null,
  longitude real not null,
  strike_dip_rake text not null,
  moment_tensor text not null
);