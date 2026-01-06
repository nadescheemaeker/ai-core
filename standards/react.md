# React Standards

## Overview

This document defines coding standards and best practices specific to React development.

## Technology Stack

### Core

- React 18+ with TypeScript
- Modern React features (Hooks, Concurrent Features)
- Functional components only (no class components)

### Recommended Tools

- Build Tool: Vite or Next.js
- State Management: React Context, Zustand, or Redux Toolkit
- Routing: React Router or Next.js routing
- Styling: Tailwind CSS, CSS Modules, or styled-components
- Testing: Vitest + React Testing Library
- Linting: ESLint with react-hooks plugin
- Formatting: Prettier

## Project Structure

### Recommended Directory Layout

```
src/
├── components/           # Reusable UI components
│   ├── common/          # Shared components (Button, Input, etc.)
│   ├── layout/          # Layout components (Header, Footer, etc.)
│   └── features/        # Feature-specific components
├── pages/               # Page components (or use app/ for Next.js)
├── hooks/               # Custom React hooks
├── contexts/            # React Context providers
├── services/            # API calls and external services
├── utils/               # Utility functions
├── types/               # TypeScript type definitions
├── constants/           # Constants and configuration
├── assets/              # Static assets (images, fonts)
└── styles/              # Global styles
```

## Naming Conventions

### Components

- **PascalCase** for component files and names
- Example: `UserProfile.tsx`, `TodoList.tsx`

### Hooks

- **camelCase** starting with "use"
- Example: `useAuth.ts`, `useFetchData.ts`

### Files

- Components: `ComponentName.tsx`
- Hooks: `useHookName.ts`
- Utils: `utilityName.ts`
- Types: `types.ts` or `ComponentName.types.ts`
- Tests: `ComponentName.test.tsx`

### Props and State

- **camelCase** for variables and functions
- Use descriptive names that indicate purpose
- Boolean props should be prefixed with `is`, `has`, `should`, etc.

```typescript
interface UserCardProps {
  userName: string;
  isActive: boolean;
  hasPermission: boolean;
  onUserClick: (userId: string) => void;
}
```

## Component Patterns

### Functional Components with TypeScript

```typescript
import { FC } from "react";

interface ButtonProps {
  label: string;
  variant?: "primary" | "secondary";
  disabled?: boolean;
  onClick: () => void;
}

export const Button: FC<ButtonProps> = ({
  label,
  variant = "primary",
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
};
```

### Component Organization

```typescript
// 1. Imports
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/common";
import type { User } from "@/types";

// 2. Types/Interfaces
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

// 3. Component
export const UserProfile: FC<UserProfileProps> = ({ userId, onUpdate }) => {
  // 3a. Hooks
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);

  // 3b. Effects
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);

  // 3c. Event Handlers
  const handleSave = () => {
    // Implementation
  };

  // 3d. Render helpers (if needed)
  const renderUserDetails = () => {
    // Complex rendering logic
  };

  // 3e. Early returns
  if (!user) return <Loading />;

  // 3f. Main render
  return <div className="user-profile">{/* JSX */}</div>;
};
```

## Hooks

### Custom Hooks

```typescript
// hooks/useLocalStorage.ts
import { useState, useEffect } from "react";

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue] as const;
}
```

### Hook Best Practices

- Keep hooks focused and single-purpose
- Extract complex logic into custom hooks
- Follow React's Rules of Hooks
- Don't call hooks conditionally
- Use dependency arrays correctly in `useEffect` and `useCallback`

### Common Patterns

```typescript
// Fetch data hook
export function useFetchData<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url);
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

## State Management

### Local State (useState)

```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// Update state with callback for computed values
setCount((prevCount) => prevCount + 1);
```

### Context API

```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useState, FC, ReactNode } from "react";

interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: Credentials) => {
    const user = await authenticateUser(credentials);
    setUser(user);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
```

### State Management Guidelines

- Use local state for UI state
- Use Context for shared state that doesn't change often
- Use external libraries (Zustand, Redux Toolkit) for complex global state
- Avoid prop drilling - use Context or composition

## Performance Optimization

### Memoization

```typescript
import { memo, useMemo, useCallback } from "react";

// Memoize expensive components
export const ExpensiveComponent = memo<Props>(({ data }) => {
  return <div>{/* Render data */}</div>;
});

// Memoize expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// Memoize callbacks
const handleClick = useCallback(() => {
  console.log("Clicked with data:", data);
}, [data]);
```

### Code Splitting

```typescript
import { lazy, Suspense } from "react";

const HeavyComponent = lazy(() => import("./HeavyComponent"));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Performance Best Practices

- Use React DevTools Profiler to identify bottlenecks
- Avoid unnecessary re-renders
- Virtualize long lists (react-window, react-virtual)
- Optimize images and assets
- Use proper key props in lists
- Debounce/throttle expensive operations

## TypeScript Best Practices

### Prop Types

```typescript
// Prefer interfaces for props
interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  className?: string;
}

// Use type for unions and intersections
type Status = "idle" | "loading" | "success" | "error";
type ButtonVariant = "primary" | "secondary" | "danger";
```

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string;
}

export function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item) => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

### Type Safety

```typescript
// Avoid 'any' - use 'unknown' or proper types
// Bad
const processData = (data: any) => {};

// Good
const processData = (data: unknown) => {
  if (typeof data === "object" && data !== null) {
    // Process data
  }
};

// Use type guards
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === "object" && obj !== null && "id" in obj && "name" in obj
  );
}
```

## Styling

### CSS Modules

```typescript
import styles from "./Button.module.css";

export const Button: FC<ButtonProps> = ({ label }) => {
  return <button className={styles.button}>{label}</button>;
};
```

### Tailwind CSS

```typescript
export const Button: FC<ButtonProps> = ({ label, variant }) => {
  const baseClasses = "px-4 py-2 rounded font-medium transition";
  const variantClasses = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
  };

  return (
    <button className={`${baseClasses} ${variantClasses[variant]}`}>
      {label}
    </button>
  );
};
```

### Conditional Classes

```typescript
import clsx from "clsx";

<button
  className={clsx(
    "btn",
    isActive && "btn-active",
    isDisabled && "btn-disabled"
  )}
>
  Click me
</button>;
```

## Testing

### Component Testing

```typescript
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("renders with correct label", () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  it("calls onClick when clicked", () => {
    const handleClick = vi.fn();
    render(<Button label="Click me" onClick={handleClick} />);

    fireEvent.click(screen.getByText("Click me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("is disabled when disabled prop is true", () => {
    render(<Button label="Click me" onClick={() => {}} disabled />);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
```

### Hook Testing

```typescript
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("increments counter", () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Accessibility

### ARIA and Semantic HTML

```typescript
export const Modal: FC<ModalProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <h2 id="modal-title">Modal Title</h2>
      <button aria-label="Close modal" onClick={onClose}>
        ×
      </button>
      {children}
    </div>
  );
};
```

### Keyboard Navigation

```typescript
const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
  if (event.key === "Escape") {
    onClose();
  }
};
```

### Accessibility Checklist

- [ ] Use semantic HTML elements
- [ ] Provide alt text for images
- [ ] Ensure keyboard navigation works
- [ ] Use ARIA attributes appropriately
- [ ] Maintain sufficient color contrast
- [ ] Test with screen readers
- [ ] Provide focus indicators

## Error Handling

### Error Boundaries

```typescript
import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}
```

## Security

- Sanitize user input before rendering
- Use `textContent` or libraries like DOMPurify for XSS prevention
- Validate forms on both client and server
- Use HTTPS for all API calls
- Store sensitive data securely (not in localStorage for tokens)
- Implement proper CORS policies
- Keep dependencies updated

## Best Practices Summary

✅ **DO**

- Use functional components and hooks
- Keep components small and focused
- Extract reusable logic into custom hooks
- Use TypeScript for type safety
- Write tests for critical functionality
- Optimize performance when needed
- Follow accessibility guidelines
- Use meaningful component and variable names

❌ **DON'T**

- Use class components (unless maintaining legacy code)
- Mutate state directly
- Over-optimize prematurely
- Ignore TypeScript errors
- Skip error handling
- Nest components deeply
- Use inline functions in render (when it causes performance issues)
- Forget to clean up effects
