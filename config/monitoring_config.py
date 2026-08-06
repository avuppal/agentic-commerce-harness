from prometheus_client import Histogram, Counter

# --- Agent Response Latency Metrics ---

AGENT_RESPONSE_LATENCY = Histogram(
    'agent_response_latency_seconds',
    'Histogram of agent response latency for JSON-LD payloads.',
    buckets=[0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.5, 1.0, float('inf')], # Buckets covering the target latency and beyond
    labelnames=['endpoint', 'agent_type', 'status_code']
)

AGENT_RESPONSE_ERRORS = Counter(
    'agent_response_errors_total',
    'Total count of agent response errors.',
    labelnames=['endpoint', 'agent_type', 'status_code']
)

# --- Cryptographic VC Validation Metrics ---

VC_VALIDATION_LATENCY = Histogram(
    'vc_validation_latency_seconds',
    'Histogram of time taken for cryptographic VC validation steps.',
    buckets=[0.001, 0.002, 0.005, 0.01, 0.015, 0.02, 0.05, 0.1, float('inf')],
    labelnames=['credential_type', 'validation_step', 'status']
)

VC_VALIDATION_ERRORS = Counter(
    'vc_validation_errors_total',
    'Total count of VC validation errors.',
    labelnames=['credential_type', 'validation_step', 'status']
)

# --- General Metrics ---

UPTIME = Counter(
    'uptime_seconds_total',
    'Total uptime of the harness service.',
    documentation='Total uptime of the harness service.'
)

# --- Configuration for Dashboarding/Alerting (Conceptual) ---
# These would typically be managed by external configuration files or infrastructure.

MONITORING_TARGETS = {
    "agent_response_latency_ms": {
        "metric_name": "agent_response_latency_seconds",
        "target": 45,
        "unit": "ms",
        "description": "Target for agent response latency for JSON-LD payloads."
    },
    "vc_validation_latency_ms": {
        "metric_name": "vc_validation_latency_seconds",
        "target": 15,
        "unit": "ms",
        "description": "Target for cryptographic VC validation latency per credential proof."
    }
}

# --- Example of how these might be used (this part would be in your application logic) ---
# import time
#
# def process_request(endpoint, agent_type):
#     start_time = time.time()
#     try:
#         # ... actual request processing ...
#         status_code = 200
#         # AGENT_RESPONSE_LATENCY.labels(endpoint=endpoint, agent_type=agent_type, status_code=status_code).observe(time.time() - start_time)
#     except Exception as e:
#         status_code = 500
#         AGENT_RESPONSE_ERRORS.labels(endpoint=endpoint, agent_type=agent_type, status_code=status_code).inc()
#         raise
#
# def verify_credential(credential_type, validation_step, status):
#     start_time = time.time()
#     try:
#         # ... actual VC verification logic ...
#         # VC_VALIDATION_LATENCY.labels(credential_type=credential_type, validation_step=validation_step, status=status).observe(time.time() - start_time)
#     except Exception as e:
#         VC_VALIDATION_ERRORS.labels(credential_type=credential_type, validation_step=validation_step, status='failed').inc()
#         raise
