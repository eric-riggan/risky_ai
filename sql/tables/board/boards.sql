USE [risk];
GO

IF NOT EXISTS (
    SELECT *
      FROM sys.objects
     WHERE object_id = OBJECT_ID(
               N'[risk].[boards]'
           )
       AND TYPE IN (N'U')
)
BEGIN
CREATE TABLE [board].[boards] (
            [id] INT          NOT NULL IDENTITY(1,1), -- PK
    [board_name] VARCHAR(100) NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_boards PRIMARY KEY ([id] ASC),
-- INDEX
    INDEX IX_boards_board_name NONCLUSTERED ([board_name])
);
END
GO