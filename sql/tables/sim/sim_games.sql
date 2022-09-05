USE [risk];
GO

IF NOT EXISTS(
    SELECT *
      FROM INFORMATION_SCHEMA.TABLES
     WHERE TABLE_NAME = 'sim_games'
       AND TABLE_SCHEMA = 'sim'
)
CREATE TABLE [sim].[sim_games](
              [id] UNIQUEIDENTIFIER NOT NULL, --PK
    [atk_strength] INT NOT NULL,
    [def_strength] INT NOT NULL,
      [atk_losses] INT NOT NULL,
      [def_losses] INT NOT NULL,
          [rounds] INT NOT NULL,
         [outcome] BIT NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_sim_games PRIMARY KEY ([id]),
-- INDICES
    INDEX IX_sim_games_atk_strength_def_strength NONCLUSTERED (
        [atk_strength], [def_strength]
    ) INCLUDE (
        [atk_losses],
        [def_losses],
        [rounds],
        [outcome]
    )
);
GO