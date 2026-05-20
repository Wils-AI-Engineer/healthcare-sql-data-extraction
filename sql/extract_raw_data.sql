-- 
-- Purpose: Create the final flat-file extract for analytics and ETL.

SELECT
-- Patient information
     p.patient_id,
    p.first_name AS patient_first_name,
    p.last_name AS patient_last_name,
    p.gender,
    p.date_of_birth,
    p.city,
    p.insurance_type,
    p.registered_at AS date_of_registration,

 -- Appointment information
    a.appointment_id,
    a.appointment_date,
    a.status AS appointment_status,
    a.duration_mins,

 -- Doctor information
    d.doctor_id,
    d.first_name AS doctor_first_name,
    d.last_name AS doctor_last_name,
    d.specialization,
    d.years_exp,
    d.salary,

 -- Department information
    dept.dept_id,
    dept.dept_name,
    dept.bed_count,
    dept.floor_number,

    -- Billing information
    b.bill_id,
    b.amount_charged,
    b.insurance_paid,
    b.payment_status,
    b.bill_date,
    b.payment_method,
    
 -- Metadata-----------------------------------------------------------------------
    'healthcare'::VARCHAR AS source_schema,
    NOW()::DATE AS extracted_date

FROM healthcare.patients AS p
JOIN healthcare.appointments AS a
    ON p.patient_id = a.patient_id
LEFT JOIN healthcare.billing AS b
    ON a.appointment_id = b.appointment_id
LEFT JOIN healthcare.doctors AS d
    ON a.doctor_id = d.doctor_id
LEFT JOIN healthcare.departments AS dept
    ON d.dept_id = dept.dept_id
ORDER BY 
    p.patient_id,
    a.appointment_date;