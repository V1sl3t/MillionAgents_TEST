query = """
CREATE TABLE pos (
    id int PRIMARY KEY,
    title character varying
)
CREATE TABLE reports (
    id int PRIMARY KEY,
    barcode character varying,
    price float,
    pos_id int
)
"""

answer_query = """
SELECT r.barcode, r.price, p.title
FROM reports r
JOIN pos p ON r.pos_id = p.id
GROUP BY r.barcode, r.price, p.title
HAVING COUNT(*) > 1;
"""