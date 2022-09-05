USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[territories]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[territories] (
                [id] INT          NOT NULL IDENTITY(1,1), -- PK
      [continent_id] INT          NOT NULL, -- FK
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
END
GO