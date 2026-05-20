-- Purpose: Join patient, appointment, billing, doctor, and department data.

-- Join patients with appointments
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    p.date_of_birth,
    p.gender,
    a.appointment_id,
    a.appointment_date,
    a.status
FROM healthcare.patients AS p
JOIN healthcare.appointments AS a
    ON p.patient_id = a.patient_id
LIMIT 50;

-- Join patients, appointments, and billing
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    a.appointment_id,
    a.appointment_date,
    a.status,
    b.bill_id,
    b.amount_charged,
    b.payment_status
FROM healthcare.patients AS p
JOIN healthcare.appointments AS a
    ON p.patient_id = a.patient_id
LEFT JOIN healthcare.billing AS b
    ON a.appointment_id = b.appointment_id
LIMIT 50;
