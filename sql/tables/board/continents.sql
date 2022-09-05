USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[continents]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[continents] (
                [id] INT         NOT NULL IDENTITY(1,1), -- PK
          [board_id] INT         NOT NULL, -- FK
    [continent_name] VARCHAR(20) NOT NULL,
      [supply_bonus] INT         NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_continents PRIMARY KEY ([id] ASC),
-- FOREIGN KEY
    CONSTRAINT FK_continents_boards
               FOREIGN KEY ([board_id])
                REFERENCES [board].[boards] ([id])
                 ON DELETE CASCADE
                 ON UPDATE CASCADE
);
END
GO