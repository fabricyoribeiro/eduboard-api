-- Tabela: actor
CREATE TABLE IF NOT EXISTS actor (
    username VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL
);

-- Tabela: verb
CREATE TABLE IF NOT EXISTS verb (
    id VARCHAR(100) PRIMARY KEY,
    display_pt VARCHAR(100) NOT NULL,
    display_en VARCHAR(100) NOT NULL
);

-- Tabela: object
CREATE TABLE IF NOT EXISTS object (
    id VARCHAR(100) PRIMARY KEY,
    name_pt VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description_pt TEXT NOT NULL,
    description_en TEXT NOT NULL
);

-- Tabela: subject
CREATE TABLE IF NOT EXISTS subject (
    id SERIAL PRIMARY KEY,
    name_pt VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description_pt TEXT NOT NULL,
    description_en TEXT NOT NULL
);

-- Tabela: result
CREATE TABLE IF NOT EXISTS result (
    id SERIAL PRIMARY KEY,
    success BOOLEAN NOT NULL,
    response VARCHAR(10) NOT NULL,
    response_time_seconds INTEGER NOT NULL
);

-- Tabela: event (interação)
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    actor_username VARCHAR(50) NOT NULL,
    verb_id VARCHAR(100) NOT NULL,
    object_id VARCHAR(100) NOT NULL,
    subject_id INTEGER NOT NULL,
    result_id INTEGER NOT NULL,
    date_time TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_actor FOREIGN KEY (actor_username) REFERENCES actor(username),
    CONSTRAINT fk_verb FOREIGN KEY (verb_id) REFERENCES verb(id),
    CONSTRAINT fk_object FOREIGN KEY (object_id) REFERENCES object(id),
    CONSTRAINT fk_subject FOREIGN KEY (subject_id) REFERENCES subject(id),
    CONSTRAINT fk_result FOREIGN KEY (result_id) REFERENCES result(id)
);
