# Global Standards

## Overview

This document defines coding standards and best practices applicable to ALL projects, regardless of programming language or framework.

## General Principles

### 1. Code Quality

- **Readability First**: Code should be self-explanatory and easy to understand
- **Consistency**: Follow established patterns within the codebase
- **Simplicity**: Prefer simple solutions over complex ones (KISS principle)
- **DRY**: Don't Repeat Yourself - avoid code duplication

### 2. Documentation

#### Code Comments

- Write comments for complex logic or non-obvious decisions
- Keep comments up-to-date with code changes
- Avoid stating the obvious
- Use TODO/FIXME/NOTE tags appropriately

#### README Files

Every project must include:

- Project description and purpose
- Setup/installation instructions
- Usage examples
- Dependencies and requirements
- Contributing guidelines
- License information

### 3. Version Control

#### Git Practices

- **Commit Messages**: Use clear, descriptive commit messages
  - Format: `type: brief description`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
  - Example: `feat: add user authentication module`
- **Branch Naming**: Use descriptive branch names
  - Format: `type/description`
  - Example: `feature/user-authentication`, `bugfix/login-error`
- **Commit Frequency**: Commit small, logical changes frequently
- **Never Commit**: Secrets, credentials, or sensitive data

#### .gitignore

- Always include a comprehensive `.gitignore` file
- Exclude build artifacts, dependencies, IDE files, and environment files

### 4. Security

#### Best Practices

- Never hardcode credentials, API keys, or secrets
- Use environment variables for configuration
- Keep dependencies up-to-date
- Validate and sanitize all inputs
- Follow principle of least privilege
- Implement proper error handling without exposing sensitive information

#### Secrets Management

- Use `.env` files for local development (never commit them)
- Use secret management services for production
- Rotate credentials regularly

### 5. Testing

#### Coverage

- Aim for minimum 80% code coverage
- Write tests for all critical paths
- Include unit, integration, and end-to-end tests where appropriate

#### Test Quality

- Tests should be independent and repeatable
- Use descriptive test names that explain the scenario
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies

### 6. Code Review

#### Review Process

- All code must be reviewed before merging
- Reviews should be constructive and respectful
- Check for functionality, readability, and adherence to standards
- Verify tests are included and passing

#### Checklist

- [ ] Code follows project conventions
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] No performance regressions

### 7. Project Structure

#### Organization

- Use clear, logical directory structure
- Group related files together
- Separate concerns (business logic, UI, data access, etc.)
- Keep configuration files in root directory

#### Naming Conventions

- Use meaningful, descriptive names
- Be consistent across the project
- Avoid abbreviations unless widely known
- Use appropriate case conventions for your language

### 8. Error Handling

#### Principles

- Always handle errors gracefully
- Provide meaningful error messages
- Log errors with sufficient context
- Never expose internal implementation details in error messages
- Use appropriate error levels (debug, info, warn, error)

### 9. Performance

#### Optimization

- Profile before optimizing
- Focus on algorithm efficiency
- Minimize network calls and database queries
- Use caching where appropriate
- Consider scalability from the start

### 10. Accessibility

#### Guidelines

- Design for all users, including those with disabilities
- Follow WCAG guidelines for web applications
- Provide alternative text for images
- Ensure keyboard navigation
- Use semantic HTML and ARIA labels

### 11. Internationalization (i18n)

#### Best Practices

- Externalize all user-facing strings
- Use i18n libraries and frameworks
- Consider cultural differences (dates, numbers, currency)
- Support RTL languages where applicable
- Design with translation expansion in mind

### 12. Continuous Integration/Deployment

#### CI/CD Pipeline

- Automate testing on every commit
- Automate builds and deployments
- Run security scans automatically
- Use staging environments before production
- Implement rollback strategies

## Enforcement

These standards should be:

- Reviewed and updated regularly
- Enforced through code reviews
- Supported by automated tools (linters, formatters)
- Part of onboarding for new team members
