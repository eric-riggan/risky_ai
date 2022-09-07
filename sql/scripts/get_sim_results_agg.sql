
SELECT [sg].[atk_strength],
       [sg].[def_strength],
       CAST(AVG(CAST(outcome AS DECIMAL(5,4))) AS DECIMAL(4,3)) AS [mean_outcome],
       CAST(AVG(CAST(atk_losses AS DECIMAL(4,2))) AS DECIMAL(5,3)) AS [mean_atk_losses]
  FROM [sim].[sim_games] sg
 GROUP BY [sg].[atk_strength],
          [sg].[def_strength]
 ORDER BY [sg].[atk_strength],
          [sg].[def_strength]