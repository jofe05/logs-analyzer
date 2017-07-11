CREATE TABLE `experimentation` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT,
          `architecture` TEXT NOT NULL,
	`mapper` TEXT NOT NULL,
	`mode` TEXT NOT NULL,
	`run` INTEGER NOT NULL,
	`threads` INTEGER NOT NULL,
	`intances` INTEGER NOT NULL DEFAULT '1',
	`time` REAL NOT NULL,
          `type` TEXT NOT NULL DEFAULT 'raw'
);

CREATE TABLE `counter` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`experimentationId` INTEGER NOT NULL REFERENCES experimentation(id),
	`socket` INTEGER NOT NULL,
	`name` TEXT NOT NULL,
	`stat` REAL NOT NULL
);
