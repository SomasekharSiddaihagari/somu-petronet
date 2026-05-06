
DECLARE
    station_summary JSON;
    monthly_trends JSON;
BEGIN
    ------------------------------------------------------------------
    -- 1. STATION SUMMARY + PERCENTAGE SPLIT
    ------------------------------------------------------------------
    WITH leave_data AS (
        SELECT
            s.station_id,
            s.station_name,
            COALESCE(SUM(hla.number_of_days), 0) AS total_leaves
        FROM station s
        LEFT JOIN users u ON u.station_id = s.station_id
        LEFT JOIN hr_leave_application hla 
            ON hla.user_id = u.user_id 
           AND hla.status ILIKE 'approved'
        GROUP BY s.station_id, s.station_name
    ),
    total_sum AS (
        SELECT SUM(total_leaves) AS grand_total FROM leave_data
    )
    SELECT json_agg(
        json_build_object(
            'station_id', station_id,
            'station_name', station_name,
            'total_leaves', total_leaves,
            'percentage_split',
            CASE 
                WHEN (SELECT grand_total FROM total_sum) = 0 THEN 0
                ELSE ROUND((total_leaves * 100.0) / (SELECT grand_total FROM total_sum), 2)
            END
        )
    )
    INTO station_summary
    FROM leave_data;

    ------------------------------------------------------------------
    -- 2. MONTHLY LEAVE TRENDS (MONTH NAME ONLY)
    ------------------------------------------------------------------
    WITH monthly AS (
        SELECT
            s.station_id,
            s.station_name,
            TRIM(TO_CHAR(hla.from_date, 'Month')) AS month,   -- 👈 Month name only
            COALESCE(SUM(hla.number_of_days), 0) AS total_leaves
        FROM station s
        LEFT JOIN users u ON u.station_id = s.station_id
        LEFT JOIN hr_leave_application hla
            ON hla.user_id = u.user_id 
           AND hla.status ILIKE 'approved'
        GROUP BY 
            s.station_id, 
            s.station_name, 
            TRIM(TO_CHAR(hla.from_date, 'Month'))
        ORDER BY s.station_id
    )
    SELECT json_agg(
        json_build_object(
            'station_id', station_id,
            'station_name', station_name,
            'month', month,
            'total_leaves', total_leaves
        )
    )
    INTO monthly_trends
    FROM monthly;

    ------------------------------------------------------------------
    -- 3. FINAL COMBINED JSON OUTPUT
    ------------------------------------------------------------------
    RETURN json_build_object(
        'station_summary', station_summary,
        'monthly_trends', monthly_trends
    );

END;
