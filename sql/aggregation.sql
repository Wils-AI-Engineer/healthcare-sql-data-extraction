
-- Count total patients
SELECT 
    COUNT(*) AS total_patients
FROM healthcare.patients;

-- Count total appointments
SELECT 
    COUNT(*) AS total_appointments
FROM healthcare.appointments;

-- Count appointments by status
SELECT 
    status,
    COUNT(*) AS appointment_count
FROM healthcare.appointments
GROUP BY status
ORDER BY appointment_count DESC;

-- Count appointments by doctor
SELECT 
    doctor_id,
    COUNT(*) AS appointment_count
FROM healthcare.appointments
GROUP BY doctor_id
ORDER BY appointment_count DESC;

-- Count appointments by duration and visit type
SELECT
	visit_type,
	duration_mins,
	COUNT(*)AS appointment_count
	FROM healthcare.appointments
	GROUP BY visit_type, duration_mins
	ORDER BY appointment_count DESC;

-- Total billing amount
SELECT 
    SUM(amount_charged) AS total_billing_amount
FROM healthcare.billing;

-- Billing summary by payment status
SELECT 
    payment_status,
    COUNT(*) AS bill_count,
    SUM(amount_charged) AS total_amount,
    AVG(amount_charged) AS average_amount
FROM healthcare.billing
GROUP BY payment_status
ORDER BY total_amount DESC;

-- Count total number of Doctors
SELECT
	COUNT(*) AS total_doctors
	FROM healthcare.doctors

	-- Count doctors by specialization and years of experience
SELECT 
	specialization,
	years_exp,
	COUNT(*) AS doctor_count
	FROM healthcare.doctors
	GROUP BY specialization, years_exp
	ORDER BY doctor_count 

-- Doctor summary by salary
SELECT 
    specialization,
    COUNT(*) AS doctor_count,
    SUM(salary) AS total_salary,
    AVG(salary) AS average_salary
FROM healthcare.doctors
GROUP BY specialization
ORDER BY  total_salary DESC;

-- Department Data
SELECT
	count(*)AS num_department
	FROM healthcare.departments

-- Count number of beds in each department
-- 7. Count number of beds in each department
SELECT 
    dept_name,
    SUM(bed_count) AS total_beds
FROM healthcare.departments
GROUP BY dept_name
ORDER BY total_beds DESC;
	
	