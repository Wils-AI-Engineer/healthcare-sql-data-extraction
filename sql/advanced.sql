-- Purpose: Use a CTE and window function to analyse patient billing history.

WITH patient_billing_summary AS (
    SELECT
        p.patient_id,
        p.first_name AS patient_first_name,
        p.last_name AS patient_last_name,
        p.insurance_type,
        COUNT(a.appointment_id) AS total_appointments,
        COUNT(b.bill_id) AS total_bills,
        ROUND(SUM(b.amount_charged)::NUMERIC, 2) AS total_amount_charged,
        ROUND(SUM(b.insurance_paid)::NUMERIC, 2) AS total_insurance_paid,
        ROUND(
            SUM(b.amount_charged - b.insurance_paid)::NUMERIC,
            2
        ) AS patient_balance
    FROM healthcare.patients AS p
    LEFT JOIN healthcare.appointments AS a
        ON p.patient_id = a.patient_id
    LEFT JOIN healthcare.billing AS b
        ON a.appointment_id = b.appointment_id
    GROUP BY
        p.patient_id,
        p.first_name,
        p.last_name,
        p.insurance_type
)

SELECT
    patient_id,
    patient_first_name,
    patient_last_name,
    insurance_type,
    total_appointments,
    total_bills,
    total_amount_charged,
    total_insurance_paid,
    patient_balance,

    -- Window function: ranks patients by highest outstanding balance
    RANK() OVER (
        ORDER BY patient_balance DESC
    ) AS balance_rank

FROM patient_billing_summary
ORDER BY balance_rank;