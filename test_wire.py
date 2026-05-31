from wire_client import get_medical_context
from wire_client import get_job_result

print("Starting...")

job = get_medical_context("headache dizziness fatigue")

print("JOB:")
print(job)

if "poll_url" in job:

    print("Polling...")

    result = get_job_result(job["poll_url"])

    print("RESULT:")
    print(result)

else:

    print("No poll_url found")
