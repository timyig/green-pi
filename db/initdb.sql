CREATE TABLE sensor_data (
	id SERIAL NOT NULL, 
	air_temp NUMERIC, 
	humidity NUMERIC, 
	moister NUMERIC, 
	created_date TIMESTAMP DEFAULT now(), 
	PRIMARY KEY (id)
)