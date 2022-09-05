USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[cards]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[cards] (
              [id] INT         NOT NULL IDENTITY(1,1), -- PK,
    [territory_id] INT         NULL, --FK
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
END
GO