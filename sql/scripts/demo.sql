WITH agg AS (
    SELECT [sg].[atk_strength],
           [sg].[def_strength],
           CAST(AVG(CAST(outcome AS DECIMAL(5,4))) AS DECIMAL(4,3)) AS [mean_outcome],
           CAST(AVG(CAST(atk_losses AS DECIMAL(4,2))) AS DECIMAL(5,3)) AS [mean_atk_losses]
      FROM [sim].[sim_games] sg
     GROUP BY [sg].[atk_strength],
              [sg].[def_strength]
)
SELECT a.atk_strength,
       a.def_strength,
       a.mean_outcome
  FROM agg a
 WHERE atk_strength IN (1,2,3,4,5)
   AND def_strength IN (1,2,3,4,5)
 ORDER BY atk_strength, def_strength
 