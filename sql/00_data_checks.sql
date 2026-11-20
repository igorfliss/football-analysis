SELECT
    league,
    COUNT(*) AS matches,
    COUNT(DISTINCT season) AS seasons,
    MIN(odds_home) AS min_odds,
    MAX(odds_home) AS max_odds,
    SUM(CASE WHEN odds_home IS NULL THEN 1 ELSE 0 END) AS missing_odds,
    SUM(CASE WHEN home_shots IS NULL THEN 1 ELSE 0 END) AS missing_shots
FROM matches
GROUP BY league;
