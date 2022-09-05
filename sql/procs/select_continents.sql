USE [risk];
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

