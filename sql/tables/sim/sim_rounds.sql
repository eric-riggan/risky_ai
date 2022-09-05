USE [risk];
GO

IF NOT EXISTS(
    SELECT *
      FROM INFORMATION_SCHEMA.TABLES
     WHERE TABLE_NAME = 'sim_rounds'
       AND TABLE_SCHEMA = 'sim'
)
CREATE TABLE [sim].[sim_rounds](
              [id] UNIQUEIDENTIFIER NOT NULL, --PK
         [game_id] UNIQUEIDENTIFIER NOT NULL,
    [atk_strength] INT NOT NULL,
    [def_strength] INT NOT NULL,
      [atk_losses] INT NOT NULL,
      [def_losses] INT NOT NULL,
         [outcome] BIT NOT NULL,
-- PRIMARY KEY
    CONSTRAINT PK_sim_rounds PRIMARY KEY ([id]),
-- INDICES
    INDEX IX_sim_rounds_atk_strength_def_strength NONCLUSTERED (
        [atk_strength], [def_strength]
    ) INCLUDE (
        [atk_losses],
        [def_losses],
        [outcome]
    ),
    INDEX IX_sim_rounds_game_id NONCLUSTERED ([game_id] ASC),
-- FOREIGN KEYS
    CONSTRAINT FK_sim_rounds_sim_games
               FOREIGN KEY ([game_id])
                REFERENCES [risk].[sim].[sim_games] ([id])
                 ON DELETE CASCADE
                 ON UPDATE CASCADE
);
GO