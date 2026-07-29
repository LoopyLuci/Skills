---
name: behavior-driven-development
description: "Use when implementing BDD with Gherkin and Cucumber."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [BDD, behavior-driven-development, Gherkin, Cucumber, SpecFlow, executable-specifications]
    related_skills: [test-driven-development, test-driven-workflow, code-review-checklist, api-testing-patterns]
---

# Behavior-Driven Development (BDD)

Implementing behavior-driven development — from Gherkin feature files and scenario design through step definitions, living documentation, and BDD in CI/CD.

## When to Use

- Bridging communication gap between business and technical teams
- Creating executable specifications that double as tests
- Building a shared understanding of requirements
- Automating acceptance criteria validation
- Generating living documentation from feature files

## Gherkin Syntax

```gherkin
Feature: User Login
  As a registered user
  I want to log into the application
  So that I can access my account
  
  Background:
    Given a registered user with email "user@example.com" and password "SecurePass123"
  
  Scenario: Successful login with valid credentials
    When I navigate to the login page
    And I enter "user@example.com" in the email field
    And I enter "SecurePass123" in the password field
    And I click the "Sign In" button
    Then I should be redirected to the dashboard
    And I should see "Welcome, User!" in the header
  
  Scenario: Login with invalid password
    When I navigate to the login page
    And I enter "user@example.com" in the email field
    And I enter "WrongPassword" in the password field
    And I click the "Sign In" button
    Then I should see "Invalid email or password" error message
```

## Step Definitions (Python)

```python
from behave import given, when, then
from selenium import webdriver

@given('a registered user with email "{email}" and password "{password}"')
def step_register_user(context, email, password):
    context.driver = webdriver.Chrome()
    # Register user via API or directly in database
    register_user(email, password)

@when('I navigate to the login page')
def step_navigate_to_login(context):
    context.driver.get("https://example.com/login")

@then('I should be redirected to the dashboard')
def step_check_dashboard(context):
    assert "dashboard" in context.driver.current_url
```

## Common Pitfalls

1. **Feature file as test script** — Gherkin is for behavior, not step-by-step automation details
2. **Too many scenarios** — one feature file with 40 scenarios becomes unreadable; split up
3. **Brittle step definitions** — CSS selectors in step defs break on UI changes; use Page Objects
4. **No business involvement** — BDD without business collaboration is just automated testing
5. **Overlapping step definitions** — ambiguous step matches cause confusing failures

## Verification Checklist

- [ ] Feature files written in business language (not technical)
- [ ] Scenarios use Given-When-Then format consistently
- [ ] Step definitions use Page Objects or abstraction layer
- [ ] Feature files reviewed by product/business stakeholders
- [ ] Scenarios run in CI/CD pipeline
- [ ] Living documentation generated from feature files
- [ ] Background sections for shared setup (not repeated in each scenario)
