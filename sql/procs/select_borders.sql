USE [risk];
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