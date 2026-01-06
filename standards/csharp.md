# C# Standards

## Overview

This document defines coding standards and best practices specific to C# development.

## Language Version

- Use the latest stable version of C# when possible
- Take advantage of modern language features (pattern matching, nullable reference types, etc.)

## Naming Conventions

### General Rules

- Use **PascalCase** for class names, method names, properties, and public members
- Use **camelCase** for local variables and private fields
- Use **\_camelCase** (underscore prefix) for private instance fields (optional but recommended)
- Use **SCREAMING_CASE** for constants

### Examples

```csharp
public class UserAccount
{
    private readonly IUserService _userService;
    private int _retryCount;

    public const int MAX_LOGIN_ATTEMPTS = 3;

    public string UserName { get; set; }

    public async Task<bool> AuthenticateAsync(string password)
    {
        int attemptCount = 0;
        // ...
    }
}
```

### Interface Naming

- Prefix interfaces with `I`
- Example: `IUserService`, `IRepository<T>`

### Async Method Naming

- Suffix async methods with `Async`
- Example: `GetUserAsync()`, `SaveDataAsync()`

## Code Organization

### File Structure

- One class per file (except for small related classes)
- File name should match the class name
- Organize using folders that reflect namespaces

### Namespace Organization

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
// Blank line
using Microsoft.Extensions.Logging;
using Microsoft.EntityFrameworkCore;
// Blank line
using MyProject.Core.Models;
using MyProject.Core.Interfaces;
```

### Class Member Order

1. Constants
2. Static fields
3. Fields
4. Constructors
5. Properties
6. Methods
7. Nested types

Within each group, order by access level:

- public
- internal
- protected
- private

## Language Features

### Nullable Reference Types

```csharp
#nullable enable

public class User
{
    public string Name { get; set; } = string.Empty; // Non-nullable
    public string? MiddleName { get; set; } // Nullable
}
```

### Pattern Matching

```csharp
// Use pattern matching for type checks
if (obj is User user && user.IsActive)
{
    ProcessUser(user);
}

// Switch expressions
var result = value switch
{
    0 => "Zero",
    > 0 and < 10 => "Single digit",
    _ => "Other"
};
```

### Records (C# 9+)

```csharp
// Use records for immutable data structures
public record UserDto(int Id, string Name, string Email);

// With validation
public record ProductDto
{
    public int Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal Price { get; init; }

    public ProductDto
    {
        if (Price < 0) throw new ArgumentException("Price cannot be negative");
    }
}
```

### String Interpolation

```csharp
// Prefer string interpolation over concatenation
var message = $"User {userName} logged in at {DateTime.Now:yyyy-MM-dd}";

// Use verbatim strings for paths
var path = @"C:\Users\Documents\file.txt";
```

## Best Practices

### LINQ

```csharp
// Use meaningful variable names in LINQ
var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.LastName)
    .Select(u => new UserDto(u.Id, u.FullName, u.Email));

// Avoid excessive method chaining for readability
```

### Async/Await

```csharp
// Always use async/await for I/O operations
public async Task<User> GetUserAsync(int id)
{
    return await _dbContext.Users
        .Include(u => u.Orders)
        .FirstOrDefaultAsync(u => u.Id == id);
}

// Use ConfigureAwait(false) in library code
public async Task<Data> GetDataAsync()
{
    return await _httpClient.GetAsync(url).ConfigureAwait(false);
}

// Don't use async void (except event handlers)
// Bad
public async void ProcessData() { }

// Good
public async Task ProcessDataAsync() { }
```

### Exception Handling

```csharp
// Be specific with exception types
try
{
    await ProcessPaymentAsync(payment);
}
catch (PaymentDeclinedException ex)
{
    _logger.LogWarning(ex, "Payment declined for user {UserId}", userId);
    return PaymentResult.Declined;
}
catch (Exception ex)
{
    _logger.LogError(ex, "Unexpected error processing payment");
    throw;
}

// Use custom exceptions for domain errors
public class InvalidUserOperationException : Exception
{
    public InvalidUserOperationException(string message) : base(message) { }
}
```

### Dependency Injection

```csharp
// Use constructor injection
public class UserService : IUserService
{
    private readonly IUserRepository _repository;
    private readonly ILogger<UserService> _logger;

    public UserService(
        IUserRepository repository,
        ILogger<UserService> logger)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
}

// Register services properly
services.AddScoped<IUserService, UserService>();
services.AddSingleton<ICacheService, CacheService>();
services.AddTransient<IEmailSender, EmailSender>();
```

### Disposal and Resource Management

```csharp
// Use 'using' statements for IDisposable
using var stream = new FileStream(path, FileMode.Open);
var data = await ReadDataAsync(stream);

// Implement IDisposable for classes managing unmanaged resources
public class ResourceManager : IDisposable
{
    private bool _disposed;

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;

        if (disposing)
        {
            // Dispose managed resources
        }

        _disposed = true;
    }
}
```

## Entity Framework Core

### DbContext Configuration

```csharp
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
}
```

### Entity Configuration

```csharp
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.HasKey(u => u.Id);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(256);

        builder.HasIndex(u => u.Email)
            .IsUnique();
    }
}
```

## Testing

### Unit Tests

```csharp
[TestClass]
public class UserServiceTests
{
    private Mock<IUserRepository> _mockRepository;
    private UserService _sut; // System Under Test

    [TestInitialize]
    public void Setup()
    {
        _mockRepository = new Mock<IUserRepository>();
        _sut = new UserService(_mockRepository.Object);
    }

    [TestMethod]
    public async Task GetUserAsync_WithValidId_ReturnsUser()
    {
        // Arrange
        var userId = 1;
        var expectedUser = new User { Id = userId, Name = "John Doe" };
        _mockRepository
            .Setup(r => r.GetByIdAsync(userId))
            .ReturnsAsync(expectedUser);

        // Act
        var result = await _sut.GetUserAsync(userId);

        // Assert
        Assert.IsNotNull(result);
        Assert.AreEqual(expectedUser.Id, result.Id);
        Assert.AreEqual(expectedUser.Name, result.Name);
    }

    [TestMethod]
    public async Task GetUserAsync_WithInvalidId_ThrowsException()
    {
        // Arrange
        var userId = -1;

        // Act & Assert
        await Assert.ThrowsExceptionAsync<ArgumentException>(
            () => _sut.GetUserAsync(userId));
    }
}
```

## Documentation

### XML Documentation Comments

```csharp
/// <summary>
/// Authenticates a user with the provided credentials.
/// </summary>
/// <param name="username">The user's username.</param>
/// <param name="password">The user's password.</param>
/// <returns>True if authentication succeeds; otherwise, false.</returns>
/// <exception cref="ArgumentNullException">
/// Thrown when username or password is null.
/// </exception>
public async Task<bool> AuthenticateAsync(string username, string password)
{
    // Implementation
}
```

## Code Analysis

### Enable Analyzers

```xml
<PropertyGroup>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisMode>All</AnalysisMode>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
</PropertyGroup>
```

### .editorconfig

Use an `.editorconfig` file to enforce consistent coding style across the team.

## Performance Considerations

- Use `StringBuilder` for string concatenation in loops
- Prefer `ValueTask<T>` for frequently called async methods that often complete synchronously
- Use `Span<T>` and `Memory<T>` for high-performance scenarios
- Avoid unnecessary allocations
- Use object pooling for frequently created objects
- Profile performance-critical code paths

## Security

- Validate all inputs
- Use parameterized queries (EF Core does this automatically)
- Implement proper authentication and authorization
- Store sensitive data securely
- Use HTTPS for all communications
- Keep dependencies up-to-date
- Follow OWASP security guidelines
