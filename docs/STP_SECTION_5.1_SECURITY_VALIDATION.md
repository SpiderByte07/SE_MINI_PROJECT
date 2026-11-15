# STP section 5.1 - Security Validation

Use this section in the final Software Test Plan. The cases below are validation steps, not results; keep each status as `Not Run` until executed on the merged code. Record tester, date, application revision, actual result, and evidence for each run.

## Objective and scope

Validate the security controls implemented in the demo web/API layer: HTTPS enforcement when enabled, authentication, role checks, password handling, request validation, and rate limiting. These checks do not constitute a third-party penetration test or a production security certification.

## Environment and setup

- Run the application in a test environment with a strong `TTG_JWT_SECRET` and demo credentials supplied through environment variables. Never commit real credentials or token secrets.
- For HTTPS checks, configure the application behind a trusted TLS-terminating proxy and set `TTG_REQUIRE_HTTPS=1`.
- Use test accounts only. Clear test audit data after capturing approved evidence.
- Tools: pytest/FastAPI test client for automated cases; browser/API client for configured proxy behavior. Do not test against production accounts.

## Security test cases

| Case | Check | Expected result | Actual result/status |
|---|---|---|---|
| TC-SEC-01 | Send a request over HTTP with `TTG_REQUIRE_HTTPS=1`. | Request is rejected with HTTP 426. With trusted proxy HTTPS indication, request proceeds. | Not Run |
| TC-SEC-02 | Sign in with correct demo credentials, then try an incorrect password. | Correct credentials return a bearer token; wrong credentials return 401 and do not disclose whether the username exists. | Not Run |
| TC-SEC-03 | Call a protected API without a token and with an invalid/expired token. | Both requests are rejected with 401; no protected data is returned. | Not Run |
| TC-SEC-04 | Use a valid non-coordinator token on coordinator-only generation, move, and audit operations. | Access is rejected with 403; no operation is performed. | Not Run |
| TC-SEC-05 | Submit malformed login fields and out-of-range schedule fields. | Request validation rejects the values with 422; application state remains unchanged. | Not Run |
| TC-SEC-06 | Exceed the configured login and generation request limits from one client within the limit window. | Further requests are rejected with 429. Record the threshold/window observed in the code revision. | Not Run |
| TC-SEC-07 | Inspect normal UI/API responses for baseline security headers. | `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and Content-Security-Policy headers are present. | Not Run |

## Completion rule

Record actual outcomes and attach the automated report or redacted screenshots/logs. Do not mark security validation passed merely because the endpoints exist. Document that rate limits and async job state are process-local and that HTTPS depends on the deployment proxy configuration.
