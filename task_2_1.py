query = """
CREATE TABLE reports (
    id int PRIMARY KEY,
    user_id int,
    reward int,
    created_at timestamp without time zone
)
"""

answer_query = """
WITH first_users_in_2021 AS (
    SELECT user_id
    FROM reports
    WHERE EXTRACT(YEAR FROM created_at) = 2021
    GROUP BY user_id
    HAVING MIN(created_at) >= '2021-01-01' AND MIN(created_at) <= '2021-12-31'
)
SELECT SUM(reward)
FROM reports r
JOIN first_users_in_2021 fui ON r.user_id = fui.user_id
WHERE EXTRACT(YEAR FROM r.created_at) = 2022
"""