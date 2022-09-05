USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[borders]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[borders] (
                          [id] INT NOT NULL IDENTITY(1,1), -- PK
         [source_territory_id] INT NOT NULL,
    [destination_territory_id] INT NOT NULL,
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
END
GO