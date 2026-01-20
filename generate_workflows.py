#!/usr/bin/env python3
import random
import yaml
from pathlib import Path

# Workflow names simulating a large-scale DevOps operation
workflow_templates = [
    # CI/CD Pipelines
    ("ci-build-frontend", "build", "main"),
    ("ci-build-backend-api", "build", "main"),
    ("ci-build-mobile-app-ios", "build", "main"),
    ("ci-build-mobile-app-android", "build", "main"),
    ("ci-test-unit", "test", "main"),
    ("ci-test-integration", "test", "main"),
    ("ci-test-e2e", "test", "main"),
    ("ci-security-scan", "security", "main"),
    ("ci-lint-codebase", "lint", "main"),
    ("cd-deploy-staging", "deploy", "main"),

    # Production Deployments
    ("cd-deploy-production-us-east", "deploy", "production"),
    ("cd-deploy-production-us-west", "deploy", "production"),
    ("cd-deploy-production-eu-west", "deploy", "production"),
    ("cd-deploy-production-ap-south", "deploy", "production"),
    ("cd-deploy-canary", "deploy", "production"),
    ("cd-blue-green-deployment", "deploy", "production"),
    ("cd-rollback-protection", "deploy", "production"),
    ("cd-deploy-edge-locations", "deploy", "production"),

    # Infrastructure & DevOps
    ("infra-provision-ecs-clusters", "infrastructure", "ops"),
    ("infra-update-lambda-functions", "infrastructure", "ops"),
    ("infra-terraform-apply", "infrastructure", "ops"),
    ("infra-k8s-rolling-update", "infrastructure", "ops"),
    ("infra-vpn-configuration", "infrastructure", "ops"),
    ("infra-certificate-renewal", "infrastructure", "ops"),
    ("infra-network-acls", "infrastructure", "ops"),

    # Database Operations
    ("db-migration-runner", "database", "ops"),
    ("db-backup-daily", "database", "ops"),
    ("db-backup-weekly", "database", "ops"),
    ("db-optimization-vacuum", "database", "ops"),
    ("db-replica-sync", "database", "ops"),
    ("db-connection-pooler", "database", "ops"),
    ("db-query-analytics", "database", "ops"),

    # Monitoring & Observability
    ("monitor-health-checks", "monitoring", "ops"),
    ("monitor-log-aggregation", "monitoring", "ops"),
    ("monitor-metrics-collection", "monitoring", "ops"),
    ("monitor-uptime-synthesis", "monitoring", "ops"),
    ("monitor-apm-synthesis", "monitoring", "ops"),
    ("alert-synthetic-tests", "monitoring", "ops"),

    # Security & Compliance
    ("security-vulnerability-scan", "security", "ops"),
    ("security-compliance-audit", "security", "ops"),
    ("security-secret-rotation", "security", "ops"),
    ("security-access-review", "security", "ops"),

    # Data & Analytics
    ("data-etl-pipeline", "data", "analytics"),
    ("data-warehouse-sync", "data", "analytics"),
    ("data-analytics-reports", "data", "analytics"),
    ("data-cleanup-retention", "data", "analytics"),

    # Operational Workflows
    ("ops-cache-invalidation", "operations", "maintenance"),
    ("ops-cdn-purge", "operations", "maintenance"),
    ("ops-queue-drain", "operations", "maintenance"),
    ("ops-cron-scheduler", "operations", "maintenance"),
    ("ops-service-restart", "operations", "maintenance"),
    ("ops-log-rotation", "operations", "maintenance"),
]

def random_schedule():
    """Generate a random cron schedule within a week"""
    minute = random.randint(0, 59)
    hour = random.randint(0, 23)
    day_of_month = random.randint(1, 28)
    month = random.randint(1, 12)
    day_of_week = random.randint(0, 6)

    interval1 = random.choice([2, 4, 6, 8, 12])
    interval2 = random.choice([10, 15, 20, 30])
    schedule_formats = [
        f"{minute} {hour} * * {day_of_week}",
        f"{minute} {hour} {day_of_month} * *",
        f"{minute} */{interval1} * * *",
        f"*/{interval2} * * * *",
    ]
    return random.choice(schedule_formats)

def create_workflow(name, category, env):
    """Generate a single workflow configuration"""
    is_disabled = random.random() < 0.15  # 15% disabled
    has_manual_trigger = random.random() < 0.40  # 40% can be triggered manually
    failure_rate = random.randint(10, 40)  # 10-40% failure rate

    # Determine number of jobs (1-4)
    num_jobs = random.randint(1, 4)

    workflow = {
        'name': name.replace('-', ' ').title(),
        'on': {}
    }

    # Add schedule
    if not is_disabled:
        workflow['on']['schedule'] = [{'cron': random_schedule()}]

    # Add manual trigger
    if has_manual_trigger:
        workflow['on']['workflow_dispatch'] = {}

    # Add concurrency settings
    if random.random() < 0.3:
        workflow['concurrency'] = {
            'group': f"{name}-group",
            'cancel-in-progress': random.choice([True, False])
        }

    # Add env variables
    workflow['env'] = {
        'WORKFLOW_NAME': name,
        'ENVIRONMENT': env,
        'FAILURE_RATE': str(failure_rate),
        'LOG_LEVEL': random.choice(['INFO', 'DEBUG', 'WARN']),
    }

    # Create jobs
    workflow['jobs'] = {}

    for job_idx in range(num_jobs):
        job_name = f"{category}-{job_idx + 1}"

        # Generate random job steps
        num_steps = random.randint(2, 5)

        steps = [
            {'name': 'Checkout', 'uses': 'actions/checkout@v4'},
            {'name': 'Setup Environment', 'run': 'echo "Setting up environment..."\necho "Workflow: $WORKFLOW_NAME"\necho "Environment: $ENVIRONMENT"\necho "Job: ' + job_name + '"'},
        ]

        # Add random operational steps
        step_templates = [
            ('Validate Configuration', 'echo "Validating configuration files..."\npython3 -c "import random; print(\'Config valid:\', random.choice([True, False]))"'),
            ('Run Pre-flight Checks', 'echo "Running pre-flight checks..."\nsleep $((RANDOM % 5 + 2))'),
            ('Connect to Service', 'echo "Establishing connection..."\nsleep $((RANDOM % 3 + 1))'),
            ('Execute Task', 'echo "Executing primary task..."\nsleep $((RANDOM % 8 + 3))'),
            ('Verify Results', 'echo "Verifying results..."\nsleep $((RANDOM % 4 + 1))'),
            ('Generate Report', 'echo "Generating execution report..."\ndate +"%Y-%m-%d %H:%M:%S"'),
            ('Cleanup Resources', 'echo "Cleaning up temporary resources..."\nsleep 1'),
            ('Sync State', 'echo "Synchronizing state..."\nsleep $((RANDOM % 3 + 1))'),
            ('Update Cache', 'echo "Updating cache..."\nsleep 2'),
            ('Run Diagnostics', 'echo "Running diagnostics..."\npython3 -c "import random; print(\'Health score:\', random.randint(70, 100), \'%\')"'),
            ('Optimize Resources', 'echo "Optimizing resource allocation..."\nsleep 3'),
            ('Validate Deployment', 'echo "Validating deployment state..."\nsleep $((RANDOM % 4 + 2))'),
        ]

        selected_steps = random.sample(step_templates, min(num_steps - 2, len(step_templates)))

        for step_name, step_command in selected_steps:
            steps.append({
                'name': step_name,
                'run': step_command
            })

        # Add final step with potential failure
        final_step = {
            'name': 'Finalize Job',
            'run': f'echo "Job completion check..."\nFAILURE_CHANCE=$((RANDOM % 100))\nif [ $FAILURE_CHANCE -lt {failure_rate} ]; then\n  echo "Job failed: Random failure triggered"\n  exit 1\nelse\n  echo "Job completed successfully"\nfi'
        }
        steps.append(final_step)

        # Configure job
        job_config = {
            'runs-on': 'ubuntu-latest',
            'steps': steps,
            'timeout-minutes': 1,
        }

        # Add conditional matrix or strategy for some jobs
        if random.random() < 0.25 and num_jobs > 1:
            job_config['strategy'] = {
                'matrix': {
                    'instance': [1, 2]
                }
            }

        # Add dependencies between jobs
        if job_idx > 0 and random.random() < 0.60:
            job_config['needs'] = [f"{category}-{job_idx}"]

        workflow['jobs'][job_name] = job_config

    # Add comment to disable if needed
    yaml_content = yaml.dump(workflow, default_flow_style=False, sort_keys=False)

    if is_disabled:
        yaml_content = f"# DISABLED WORKFLOW\n# To enable, remove this comment and the 'on: workflow_dispatch only' line\n" + yaml_content
        workflow['on'] = {'workflow_dispatch': {}}
        yaml_content = yaml.dump(workflow, default_flow_style=False, sort_keys=False)

    return yaml_content

# Generate all workflows
workflows_dir = Path(".github/workflows")
workflows_dir.mkdir(exist_ok=True)

for idx, (name, category, env) in enumerate(workflow_templates, 1):
    workflow_content = create_workflow(name, category, env)

    filename = f"{idx:02d}-{name}.yml"
    filepath = workflows_dir / filename

    with open(filepath, 'w') as f:
        f.write(f"# Auto-generated workflow: {name}\n")
        f.write(f"# Category: {category} | Environment: {env}\n")
        f.write(f"# This workflow simulates a real DevOps operation\n\n")
        f.write(workflow_content)

    print(f"Created: {filename}")

print(f"\nGenerated {len(workflow_templates)} workflows successfully!")
