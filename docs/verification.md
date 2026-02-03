# Verification Checklist

## App 01
- Run: `python apps/app_01_minimal/main.py`
- Expect: a short, non-tool response from the agent

## App 02
- Run: `python apps/app_02_tools_fs/main.py`
- Expect: agent uses filesystem tools and writes files under the root

## App 03
- Run: `python apps/app_03_tests/main.py`
- Expect: agent calls the test tool and reports results

## App 04
- Run: `python apps/app_04_final_cli/main.py`
- Expect: agent uses filesystem tools and optionally tests
