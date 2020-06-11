CREATE TABLE sensor_data (
	id SERIAL NOT NULL, 
	air_temp NUMERIC, 
	humidity NUMERIC, 
	moister NUMERIC, 
	created_date TIMESTAMP DEFAULT now(), 
	PRIMARY KEY (id)
);

CREATE TABLE schedule_data (
	id SERIAL NOT NULL, 
	device_id INTEGER,
    start_schedule TIMESTAMP,
    end_schedule TIMESTAMP,
    enable_schedule INTEGER,
    last_state INTEGER,
	PRIMARY KEY (id)
);
