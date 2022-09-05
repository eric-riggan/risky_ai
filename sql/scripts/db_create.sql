/*
* Run this script to generate the entire schema at once :-)
*/

USE [master];
GO

IF NOT EXISTS (
    SELECT *
      FROM [sys].[databases]
     WHERE [name] = 'risk'
)
BEGIN
CREATE DATABASE [risk];
END
GO

USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM INFORMATION_SCHEMA.SCHEMATA
     WHERE SCHEMA_NAME = 'board'
       AND CATALOG_NAME = 'risk'
)
BEGIN
EXEC(N'CREATE SCHEMA [board];');
END
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[board].[boards]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[boards] (
            [id] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(), -- PK
    [board_name] VARCHAR(100)     NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_boards PRIMARY KEY ([id] ASC),
-- INDEX
    INDEX IX_boards_board_name NONCLUSTERED ([board_name])
);

INSERT INTO [board].[boards] (
    [board_name]
) VALUES ('Original');
END
GO

USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[board].[continents]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[continents] (
                [id] UNIQUEIDENTIFIER NOT NULL CONSTRAINT DF_continents_id DEFAULT NEWID(), -- PK
          [board_id] UNIQUEIDENTIFIER NOT NULL, -- FK
    [continent_name] VARCHAR(20)      NOT NULL,
      [supply_bonus] INT              NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_continents PRIMARY KEY ([id] ASC),
-- FOREIGN KEY
    CONSTRAINT FK_continents_boards
               FOREIGN KEY ([board_id])
                REFERENCES [board].[boards] ([id])
                 ON DELETE CASCADE
                 ON UPDATE CASCADE
);

CREATE TABLE #temp_continents (
        [board_name] VARCHAR(100),
    [continent_name] VARCHAR(20),
      [supply_bonus] INT
);
INSERT INTO #temp_continents (
    [board_name],
    [continent_name],
    [supply_bonus]
) VALUES ('Original','North America',5),
         ('Original','South America',2),
         ('Original','Europe',5),
         ('Original','Africa',3),
         ('Original','Asia',7),
         ('Original','Australia',2);

INSERT INTO [board].[continents] (
    [board_id],
    [continent_name],
    [supply_bonus]
)
SELECT [b].[id],
       [c].[continent_name],
       [c].[supply_bonus]
  FROM [#temp_continents] c
       INNER JOIN [board].[boards] b
          ON [c].[board_name] = [b].[board_name];
DROP TABLE #temp_continents;
END
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[board].[territories]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[territories] (
                [id] UNIQUEIDENTIFIER NOT NULL CONSTRAINT DF_territories_id DEFAULT NEWID(), -- PK
      [continent_id] UNIQUEIDENTIFIER NOT NULL, -- FK
    [territory_name] VARCHAR(100) NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_territories PRIMARY KEY ([id]),
-- INDEX
    INDEX IX_territories_territory_name NONCLUSTERED ([territory_name]),
-- FOREIGN KEYS
    CONSTRAINT FK_territories_continents
               FOREIGN KEY ([continent_id])
                REFERENCES [board].[continents] ([id])
                 ON DELETE CASCADE
                 ON UPDATE CASCADE
);

CREATE TABLE #temp_territories (
    [continent_name] VARCHAR(20),
    [territory_name] VARCHAR(100)
);

INSERT INTO #temp_territories(
    [continent_name],
    [territory_name]
) VALUES ('North America','Alaska'),
         ('North America','Northwest Territory'),
         ('North America','Greenland'),
         ('North America','Alberta'),
         ('North America','Ontario'),
         ('North America','Quebec'),
         ('North America','Western US'),
         ('North America','Eastern US'),
         ('North America','Central America'),
         ('South America','Venezuela'),
         ('South America','Brazil'),
         ('South America','Peru'),
         ('South America','Argentina'),
         ('Europe','Great Britain'),
         ('Europe','Iceland'),
         ('Europe','Scandinavia'),
         ('Europe','Western Europe'),
         ('Europe','Northern Europe'),
         ('Europe','Southern Europe'),
         ('Europe','Ukraine'),
         ('Africa','North Africa'),
         ('Africa','Egypt'),
         ('Africa','East Africa'),
         ('Africa','Congo'),
         ('Africa','South Africa'),
         ('Africa','Madagascar'),
         ('Asia','Middle East'),
         ('Asia','Afghanistan'),
         ('Asia','Ural'),
         ('Asia','India'),
         ('Asia','China'),
         ('Asia','Siberia'),
         ('Asia','Yakutsk'),
         ('Asia','Irkutsk'),
         ('Asia','Siam'),
         ('Asia','Kamchatka'),
         ('Asia','Japan'),
         ('Asia','Mongolia'),
         ('Australia','Indonesia'),
         ('Australia','New Guinea'),
         ('Australia','Western Australia'),
         ('Australia','Eastern Australia');

INSERT INTO [board].[territories] (
    [continent_id],
    [territory_name]
)
SELECT [c].[id],
       [t].[territory_name]
  FROM #temp_territories t
       INNER JOIN [board].[continents] c
          ON [c].[continent_name] = [t].[continent_name];
DROP TABLE #temp_territories;
END
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[board].[borders]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[borders] (
                          [id] UNIQUEIDENTIFIER NOT NULL CONSTRAINT DF_borders_id DEFAULT NEWID(), -- PK
         [source_territory_id] UNIQUEIDENTIFIER NOT NULL,
    [destination_territory_id] UNIQUEIDENTIFIER NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_borders PRIMARY KEY ([id]),
-- INDEX
    INDEX IX_borders_source_territory_id_destination_territory_id
          UNIQUE NONCLUSTERED (
                                  [source_territory_id],
                                  [destination_territory_id]
                              ),
-- FOREIGN KEYS
    CONSTRAINT FK_borders_territories_source
               FOREIGN KEY ([source_territory_id])
                REFERENCES [board].[territories] ([id])
                 ON DELETE CASCADE
                 ON UPDATE CASCADE,
    CONSTRAINT FK_borders_territories_destination
               FOREIGN KEY ([destination_territory_id])
                REFERENCES [board].[territories] ([id])
                 ON DELETE NO ACTION
                 ON UPDATE NO ACTION
);

CREATE TABLE #temp_borders (
    [source_territory_name] VARCHAR(100),
    [destination_territory_name] VARCHAR(100)
);

INSERT INTO #temp_borders (
    [source_territory_name],
    [destination_territory_name]
) VALUES ('Alaska','Northwest Territory'),
         ('Alaska','Alberta'),
         ('Alaska','Kamchatka'),
         ('Northwest Territory','Greenland'),
         ('Northwest Territory','Alberta'),
         ('Northwest Territory','Ontario'),
         ('Greenland','Ontario'),
         ('Greenland','Quebec'),
         ('Greenland','Iceland'),
         ('Alberta','Ontario'),
         ('Alberta','Western US'),
         ('Ontario','Quebec'),
         ('Ontario','Western US'),
         ('Eastern US','Ontario'),
         ('Eastern US','Quebec'),
         ('Eastern US','Western US'),
         ('Eastern US','Central America'),
         ('Central America','Western US'),
         ('Central America','Venezuela'),
         ('Venezuela','Brazil'),
         ('Venezuela','Peru'),
         ('Brazil','Peru'),
         ('Brazil','Argentina'),
         ('Brazil','North Africa'),
         ('Peru','Argentina'),
         ('Great Britain','Iceland'),
         ('Scandinavia','Great Britain'),
         ('Scandinavia','Iceland'),
         ('Scandinavia','Northern Europe'),
         ('Scandinavia','Ukraine'),
         ('Western Europe','Great Britain'),
         ('Western Europe','Northern Europe'),
         ('Western Europe','Southern Europe'),
         ('Western Europe','North Africa'),
         ('Northern Europe','Great Britain'),
         ('Northern Europe','Southern Europe'),
         ('Northern Europe','Ukraine'),
         ('Southern Europe','Ukraine'),
         ('Southern Europe','North Africa'),
         ('Southern Europe','Egypt'),
         ('Southern Europe','Middle East'),
         ('Ukraine','Afghanistan'),
         ('Ukraine','Ural'),
         ('North Africa','Egypt'),
         ('North Africa','East Africa'),
         ('Egypt','East Africa'),
         ('Congo','North Africa'),
         ('Congo','East Africa'),
         ('Congo','South Africa'),
         ('South Africa','East Africa'),
         ('South Africa','Madagascar'),
         ('Madagascar','East Africa'),
         ('Middle East','Southern Europe'),
         ('Middle East','Ukraine'),
         ('Middle East','Egypt'),
         ('Middle East','Afghanistan'),
         ('Middle East','India'),
         ('Afghanistan','Ukraine'),
         ('Afghanistan','Ural'),
         ('Afghanistan','India'),
         ('Afghanistan','China'),
         ('Ural','China'),
         ('India','China'),
         ('Siberia','Ural'),
         ('Siberia','China'),
         ('Siberia','Yakutsk'),
         ('Siberia','Irkutsk'),
         ('Siberia','Mongolia'),
         ('Yakutsk','Irkutsk'),
         ('Yakutsk','Kamchatka'),
         ('Irkutsk','Kamchatka'),
         ('Irkutsk','Mongolia'),
         ('Siam','India'),
         ('Siam','China'),
         ('Siam','Indonesia'),
         ('Kamchatka','Japan'),
         ('Kamchatka','Mongolia'),
         ('Japan','Mongolia'),
         ('Mongolia','China'),
         ('New Guinea','Indonesia'),
         ('New Guinea','Western Australia'),
         ('New Guinea','Eastern Australia'),
         ('Western Australia','Indonesia'),
         ('Western Australia','Eastern Australia');

INSERT INTO [board].[borders] (
    [source_territory_id],
    [destination_territory_id]
)
SELECT [st].[id],
       [dt].[id]
  FROM #temp_borders tb
       INNER JOIN [board].[territories] st
          ON [tb].[source_territory_name] = [st].[territory_name]
       INNER JOIN [board].[territories] dt
          ON [tb].[destination_territory_name] = [dt].[territory_name];

DROP TABLE #temp_borders;
END
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[board].[cards]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[cards] (
              [id] UNIQUEIDENTIFIER NOT NULL CONSTRAINT DF_cards_id DEFAULT NEWID(), -- PK,
    [territory_id] UNIQUEIDENTIFIER NOT NULL, --FK
          [armies] INT         NOT NULL,
       [card_type] VARCHAR(20) NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_cards PRIMARY KEY ([id]),
-- FOREIGN KEYS
    CONSTRAINT FK_cards_territories
               FOREIGN KEY ([territory_id])
                REFERENCES [board].[territories] ([id])
                 ON DELETE CASCADE
                 ON UPDATE CASCADE
);

CREATE TABLE #temp_cards (
    [territory_name] VARCHAR(100),
    [armies] INT,
    [card_type] VARCHAR(20)
);
INSERT INTO #temp_cards (
    [territory_name],
    [armies],
    [card_type]
) VALUES ('Afghanistan','5','territory'),
         ('Ural','5','territory'),
         ('Northwest Territory','10','territory'),
         ('Scandinavia','5','territory'),
         ('Kamchatka','1','territory'),
         ('Alberta','5','territory'),
         ('Eastern US','10','territory'),
         ('Central America','10','territory'),
         ('East Africa','1','territory'),
         ('Venezuela','1','territory'),
         ('Egypt','1','territory'),
         ('Western Europe','10','territory'),
         ('India','5','territory'),
         ('Siberia','5','territory'),
         ('Brazil','10','territory'),
         ('North Africa','5','territory'),
         ('Iceland','1','territory'),
         ('Northern Europe','10','territory'),
         ('Great Britain','10','territory'),
         ('Japan','10','territory'),
         ('Yakutsk','5','territory'),
         ('China','1','territory'),
         ('Congo','1','territory'),
         ('Mongolia','1','territory'),
         ('New Guinea','1','territory'),
         ('Quebec','5','territory'),
         ('Western US','10','territory'),
         ('Middle East','1','territory'),
         ('Southern Europe','10','territory'),
         ('Ontario','5','territory'),
         ('Ukraine','5','territory'),
         ('Greenland','5','territory'),
         ('Madagascar','5','territory'),
         ('Alaska','1','territory'),
         ('Siam','1','territory'),
         ('Argentina','1','territory'),
         ('Irkutsk','5','territory'),
         ('Western Australia','10','territory'),
         ('South Africa','10','territory'),
         ('Peru','1','territory'),
         ('Indonesia','10','territory'),
         ('Eastern Australia','10','territory');

INSERT INTO [board].[cards] (
    [territory_id],
    [armies],
    [card_type]
)
SELECT [t].[id],
       [tc].[armies],
       [tc].[card_type]
  FROM #temp_cards tc
       INNER JOIN [board].[territories] t
          ON [tc].[territory_name] = [t].[territory_name];
DROP TABLE #temp_cards;
END
GO

CREATE OR ALTER PROCEDURE [board].[board_select_continents]
@board_name VARCHAR(30)
AS
SELECT [continent_name],
       [supply_bonus]
  FROM [board].[continents] c
       INNER JOIN [board].[boards] b
               ON [c].[board_id] = [b].[id]
 WHERE [b].[board_name] = @board_name;
GO

CREATE OR ALTER PROCEDURE [board].[board_select_territories]
@board_name VARCHAR(30)
AS 
SELECT [c].[continent_name],
       [t].[territory_name]
  FROM [board].[territories] t
       INNER JOIN [board].[continents] c
          ON [t].[continent_id] = [c].[id]
       INNER JOIN [board].[boards] b
          ON [c].[board_id] = [b].[id]
 WHERE [b].[board_name] = @board_name;
GO

CREATE OR ALTER PROCEDURE [board].[board_select_borders]
@board_name VARCHAR(30)
AS
SELECT st.territory_name AS 'source_territory',
       dt.territory_name AS 'destination_territory'
  FROM board.borders bo
       INNER JOIN board.territories st
               ON bo.source_territory_id = st.id
       INNER JOIN board.territories dt
               ON bo.destination_territory_id = dt.id
       INNER JOIN board.continents sc
               ON st.continent_id = sc.id
       INNER JOIN board.continents dc
               ON dt.continent_id = dc.id
       INNER JOIN board.boards sb
               ON sc.board_id = sb.id
       INNER JOIN board.boards db
               ON dc.board_id = db.id
 WHERE sb.board_name = @board_name
   AND db.board_name = @board_name;
GO