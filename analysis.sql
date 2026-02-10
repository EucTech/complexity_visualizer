-- SQL dump for 'analysis' table used in your Flask app
CREATE TABLE IF NOT EXISTS analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    algo VARCHAR(100) NOT NULL,
    items INT NOT NULL,
    steps INT NOT NULL,
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,
    total_time_ms FLOAT NOT NULL,
    time_complexity VARCHAR(50) NOT NULL,
    path_to_graph VARCHAR(500)
);
