USE [risk];
GO

IF NOT EXISTS (
SELECT *
  FROM INFORMATION_SCHEMA.SCHEMATA
 WHERE SCHEMA_NAME = 'sim'
)
EXEC(N'CREATE SCHEMA [risk].[sim]');
GO