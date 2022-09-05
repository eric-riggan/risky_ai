USE [risk];
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